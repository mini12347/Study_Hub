import spacy
import random
import re
from collections import defaultdict
from typing import List, Dict, Tuple
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

class QuizGenerator:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Please install spaCy model")
            raise
        
        self.struggled_topics = []
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
    
    def extract_key_sentences(self, text: str, difficulty: str = 'medium') :
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        scored_sentences = []
        for sent in sentences:
            sent_doc = self.nlp(sent)
            score = 0
            score += len(sent_doc.ents) * 2
            if any(token.like_num for token in sent_doc):
                score += 1
            word_count = len([t for t in sent_doc if not t.is_punct])
            if 8 <= word_count <= 25:
                score += 2
            if any(pattern in sent.lower() for pattern in ['is', 'are', 'refers to', 'means', 'defined as']):
                score += 3
            scored_sentences.append((sent, score))
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        num_sentences = {
            'easy': min(10, len(sentences)),
            'medium': min(15, len(sentences)),
            'hard': len(sentences)
        }
        
        return [s[0] for s in scored_sentences[:num_sentences[difficulty]]]
    
    def generate_mcq(self, sentence, difficulty = 'medium') :
        doc = self.nlp(sentence)
        candidates = []
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'CARDINAL', 'PRODUCT']:
                candidates.append((ent.text, ent.start, ent.end, 'entity'))
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
                if token.dep_ in ['nsubj', 'dobj', 'pobj']:
                    candidates.append((token.text, token.i, token.i + 1, 'noun'))
        
        if not candidates:
            return None
        if difficulty == 'hard' and len(candidates) > 1:
            answer_text, start, end, ans_type = candidates[-1]
        else:
            answer_text, start, end, ans_type = candidates[0]
        question_tokens = [token.text for token in doc]
        for i in range(start, end):
            question_tokens[i] = "______"
        question = ' '.join(question_tokens)
        question = re.sub(r'\s+([.,!?])', r'\1', question)
        distractors = self.generate_distractors(answer_text, ans_type, doc, difficulty)
        options = [answer_text] + distractors[:3]
        random.shuffle(options)
        
        return {
            'type': 'mcq',
            'question': question,
            'options': options,
            'correct_answer': answer_text,
            'explanation': f"The correct answer is '{answer_text}' based on the original text.",
            'topic': self.extract_topic(doc),
            'difficulty': difficulty
        }
    
    def generate_distractors(self, answer: str, ans_type: str, doc, difficulty: str) -> List[str]:
        distractors = []
        answer_lower = answer.lower()
        if ans_type == 'entity':
            for ent in doc.ents:
                if ent.text.lower() != answer_lower and ent.text not in distractors:
                    distractors.append(ent.text)
        try:
            synsets = wordnet.synsets(answer.replace(' ', '_'))
            for syn in synsets[:3]:
                for lemma in syn.lemmas()[:2]:
                    word = lemma.name().replace('_', ' ')
                    if word.lower() != answer_lower and word not in distractors:
                        distractors.append(word.title())
        except:
            pass
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN']:
                if token.text.lower() != answer_lower and token.text not in distractors:
                    distractors.append(token.text)
        generic_distractors = {
            'PERSON': ['John Smith', 'Jane Doe', 'Dr. Williams'],
            'ORG': ['Global Corporation', 'International Institute', 'National Association'],
            'GPE': ['New York', 'London', 'Tokyo'],
            'DATE': ['1990', '2005', '2020'],
            'CARDINAL': ['100', '500', '1000']
        }
        
        if ans_type == 'entity':
            for ent in doc.ents:
                if ent.label_ in generic_distractors:
                    distractors.extend(generic_distractors[ent.label_])
                    break
        distractors = list(set([d for d in distractors if d.lower() != answer_lower]))
        
        return distractors[:3] if len(distractors) >= 3 else distractors + ['Option A', 'Option B', 'Option C'][:3-len(distractors)]
    
    def generate_truefalse(self, sentence: str, difficulty: str = 'medium') -> Dict:
        doc = self.nlp(sentence)
        if random.random() < 0.5:
            false_statement = self.create_false_statement(sentence, doc, difficulty)
            if false_statement:
                return {
                    'type': 'truefalse',
                    'question': false_statement,
                    'options': ['True', 'False'],
                    'correct_answer': 'False',
                    'explanation': f"This statement is false. The original text states: {sentence}",
                    'topic': self.extract_topic(doc),
                    'difficulty': difficulty
                }
        return {
            'type': 'truefalse',
            'question': sentence,
            'options': ['True', 'False'],
            'correct_answer': 'True',
            'explanation': "This statement is true according to the text.",
            'topic': self.extract_topic(doc),
            'difficulty': difficulty
        }
    
    def create_false_statement(self, sentence: str, doc, difficulty: str) -> str:
        false_sent = sentence
        entities = list(doc.ents)
        
        if entities:
            entity = entities[0]
            distractors = self.generate_distractors(entity.text, 'entity', doc, difficulty)
            if distractors:
                false_sent = sentence.replace(entity.text, distractors[0])
                return false_sent
        for token in doc:
            if token.pos_ == 'VERB':
                antonyms = self.get_antonyms(token.text)
                if antonyms:
                    false_sent = sentence.replace(token.text, antonyms[0])
                    return false_sent
        for token in doc:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                false_sent = sentence.replace(token.text, f"{token.text} not")
                return false_sent
        
        return None
    
    def get_antonyms(self, word) :
        antonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.append(lemma.antonyms()[0].name())
        return antonyms
    
    def generate_fillblank(self, sentence, difficulty= 'medium') :
        doc = self.nlp(sentence)
        candidates = []
        for ent in doc.ents:
            candidates.append((ent.text, ent.start, ent.end, 'high'))
        
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
                if token.dep_ in ['nsubj', 'dobj']:
                    candidates.append((token.text, token.i, token.i + 1, 'medium'))
            elif token.pos_ == 'ADJ' and difficulty == 'hard':
                candidates.append((token.text, token.i, token.i + 1, 'low'))
        
        if not candidates:
            return None
        
        if difficulty == 'easy':
            candidates = [c for c in candidates if c[3] == 'high']
        elif difficulty == 'hard' and any(c[3] == 'low' for c in candidates):
            candidates = [c for c in candidates if c[3] != 'high']
        
        if not candidates:
            candidates = [(token.text, token.i, token.i + 1, 'medium') 
                         for token in doc if token.pos_ == 'NOUN']
        
        if not candidates:
            return None
        
        answer_text, start, end, priority = random.choice(candidates)
        
        question_tokens = [token.text for token in doc]
        for i in range(start, end):
            question_tokens[i] = "___"
        question = ' '.join(question_tokens)
        question = re.sub(r'\s+([.,!?])', r'\1', question)
        
        return {
            'type': 'fillblank',
            'question': question,
            'options': [],
            'correct_answer': answer_text,
            'explanation': f"The missing word is '{answer_text}'.",
            'topic': self.extract_topic(doc),
            'difficulty': difficulty
        }
    
    def extract_topic(self, doc) :
        entities = [ent.text for ent in doc.ents]
        nouns = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]
        
        all_topics = entities + nouns
        if all_topics:
            topic_counts = defaultdict(int)
            for topic in all_topics:
                topic_counts[topic.lower()] += 1
            return max(topic_counts, key=topic_counts.get)
        return "General"
    
    def generate_quiz(self,content,question_type = 'mixed',difficulty = 'medium',num_questions = 5,personalized = False) :
        sentences = self.extract_key_sentences(content, difficulty)
        
        if personalized and self.struggled_topics:
            filtered = []
            for sent in sentences:
                if any(topic.lower() in sent.lower() for topic in self.struggled_topics):
                    filtered.append(sent)
            if filtered:
                sentences = filtered
        
        questions = []
        question_id = 1
        if question_type == 'mixed':
            types = ['mcq', 'truefalse', 'fillblank']
            type_distribution = [types[i % 3] for i in range(num_questions)]
            random.shuffle(type_distribution)
        else:
            type_distribution = [question_type] * num_questions
      
        for qtype in type_distribution:
            if not sentences:
                break
            
            sent = random.choice(sentences)
            sentences.remove(sent)
            
            question = None
            if qtype == 'mcq':
                question = self.generate_mcq(sent, difficulty)
            elif qtype == 'truefalse':
                question = self.generate_truefalse(sent, difficulty)
            elif qtype == 'fillblank':
                question = self.generate_fillblank(sent, difficulty)
            
            if question:
                question['id'] = question_id
                questions.append(question)
                question_id += 1
        
        return {'questions': questions}
    
    def take_quiz(self, quiz) :
        answers = {}
        
        print("\n" + "="*60)
        print("QUIZ TIME!")
        print("="*60 + "\n")
        
        for i, question in enumerate(quiz['questions'], 1):
            print(f"\nQuestion {i} [{question['difficulty'].upper()}] - {question['type'].upper()}:")
            print(f"{question['question']}\n")
            
            if question['type'] == 'mcq':
                for j, option in enumerate(question['options'], 1):
                    print(f"  {j}. {option}")
                answer = input("\nYour answer (1-4): ").strip()
                try:
                    answer_idx = int(answer) - 1
                    if 0 <= answer_idx < len(question['options']):
                        answers[question['id']] = question['options'][answer_idx]
                    else:
                        answers[question['id']] = ""
                except ValueError:
                    answers[question['id']] = ""
                    
            elif question['type'] == 'truefalse':
                print("  1. True")
                print("  2. False")
                answer = input("\nYour answer (1-2): ").strip()
                if answer == '1':
                    answers[question['id']] = "True"
                elif answer == '2':
                    answers[question['id']] = "False"
                else:
                    answers[question['id']] = ""
                    
            elif question['type'] == 'fillblank':
                answer = input("\nYour answer: ").strip()
                answers[question['id']] = answer
        
        return self.grade_quiz(quiz, answers)
    
    def grade_quiz(self, quiz, answers) :
        results = []
        correct_count = 0
        
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60 + "\n")
        
        for question in quiz['questions']:
            user_answer = answers.get(question['id'], "")
            correct_answer = question['correct_answer']
            
            is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
            
            if is_correct:
                correct_count += 1
                status = "✓ CORRECT"
            else:
                status = "✗ INCORRECT"
                if question['topic'] not in self.struggled_topics:
                    self.struggled_topics.append(question['topic'])
            
            results.append({
                'question': question['question'],
                'your_answer': user_answer,
                'correct_answer': correct_answer,
                'correct': is_correct,
                'explanation': question['explanation'],
                'topic': question['topic']
            })
            
            print(f"Q: {question['question']}")
            print(f"Your answer: {user_answer}")
            print(f"Correct answer: {correct_answer}")
            print(f"Status: {status}")
            print(f"Explanation: {question['explanation']}\n")
        
        score = (correct_count / len(quiz['questions'])) * 100
        
        print("="*60)
        print(f"Final Score: {correct_count}/{len(quiz['questions'])} ({score:.1f}%)")
        print("="*60)
        
        if self.struggled_topics:
            print(f"\nTopics to review: {', '.join(set(self.struggled_topics[-5:]))}")
        
        return {
            'results': results,
            'score': correct_count,
            'total': len(quiz['questions']),
            'percentage': score
        }


