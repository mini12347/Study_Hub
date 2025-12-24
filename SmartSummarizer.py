from transformers import BartForConditionalGeneration, BartTokenizer
import spacy
from collections import Counter
from graphviz import Digraph
import torch
class MultiLevelSummarizer:
    def __init__(self, model_path="./fine_tuned_bart_model/fine_tuned_bart_model.pkl"):
        self.model_path = model_path
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
        self.model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
        state_dict = torch.load(self.model_path, map_location="cpu")
        self.model.load_state_dict(state_dict)
        self.model.eval()
        self.nlp = spacy.load("en_core_web_sm")

    def generate_summary(self, text, max_length, min_length):
        inputs = self.tokenizer(text, max_length=1024, truncation=True,
                                return_tensors="pt")
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def ultra_short_summary(self, text):
        summary = self.generate_summary(text, max_length=50, min_length=20)
        if len(summary) > 280:
            summary = summary[:277] + "..."

        return summary

    def bullet_point_summary(self, text):
        summary = self.generate_summary(text, max_length=200, min_length=80)
        doc = self.nlp(summary)
        sentences = [sent.text.strip() for sent in doc.sents]
        bullet_points = sentences[:5] if len(sentences) > 5 else sentences
        return bullet_points

    def detailed_summary(self, text):
        return self.generate_summary(text, max_length=300, min_length=100)

    def extract_key_terms(self, text, top_n=10):
        doc = self.nlp(text)

        entities = [ent.text for ent in doc.ents
                   if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'PRODUCT']]

        nouns = [chunk.text for chunk in doc.noun_chunks]

        all_terms = entities + nouns
        term_freq = Counter(all_terms)

        key_terms = [term for term, _ in term_freq.most_common(top_n)]

        return key_terms

    def create_mind_map(self, text, output_file="mindmap"):
        main_summary = self.ultra_short_summary(text)

        bullets = self.bullet_point_summary(text)

        key_terms = self.extract_key_terms(text, top_n=6)

        dot = Digraph(comment='Summary Mind Map')
        dot.attr(rankdir='LR', size='10,8')
        dot.attr('node', shape='box', style='rounded,filled',
                fillcolor='lightblue')

        dot.node('main', main_summary[:50] + '...',
                fillcolor='lightcoral', fontsize='14')

        for i, bullet in enumerate(bullets):
            node_id = f'bullet_{i}'
            dot.node(node_id, bullet[:60] + '...', fillcolor='lightyellow')
            dot.edge('main', node_id)

        dot.node('terms', 'Key Terms', fillcolor='lightgreen', fontsize='12')
        dot.edge('main', 'terms')

        for i, term in enumerate(key_terms):
            term_id = f'term_{i}'
            dot.node(term_id, term, fillcolor='lightgray', fontsize='10')
            dot.edge('terms', term_id)

        dot.render(output_file, format='png', cleanup=True)
        return f"{output_file}.png"

    def create_flowchart(self, text, output_file="flowchart"):
        bullets = self.bullet_point_summary(text)

        dot = Digraph(comment='Summary Flowchart')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='box', style='rounded,filled',
                fillcolor='lightblue')

        dot.node('start', 'Summary', shape='ellipse', fillcolor='lightgreen')

        prev_node = 'start'
        for i, bullet in enumerate(bullets):
            node_id = f'point_{i}'
            dot.node(node_id, bullet[:80] + '...')
            dot.edge(prev_node, node_id)
            prev_node = node_id

        dot.node('end', 'Conclusion', shape='ellipse', fillcolor='lightcoral')
        dot.edge(prev_node, 'end')

        dot.render(output_file, format='png', cleanup=True)
        return f"{output_file}.png"

    def summarize_all(self, text):
        return {
            'ultra_short': self.ultra_short_summary(text),
            'bullet_points': self.bullet_point_summary(text),
            'detailed': self.detailed_summary(text),
            'key_terms': self.extract_key_terms(text),
            'mind_map': self.create_mind_map(text),
            'flowchart': self.create_flowchart(text)
        }
