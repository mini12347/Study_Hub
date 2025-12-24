import streamlit as st
import time
from datetime import datetime
import json
import Study_planner 
st.set_page_config(
    page_title="StudyHub - Smart Learning Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)
def lazy_import_module(module_name):
    if module_name == 'Study_planner':
        import Study_planner
        return Study_planner
    elif module_name == 'Pamodoro_timer':
        import Pamodoro_timer
        return Pamodoro_timer
    elif module_name == 'SmartSummarizer':
        try:
            import SmartSummarizer
            return SmartSummarizer
        except ImportError:
            return None
    elif module_name == 'Flashcards_generator':
        from Flashcards_generator import FlashcardGenerator, SpacedRepetition
        return FlashcardGenerator, SpacedRepetition
    elif module_name == 'Quiz_generator':
        import Quiz_generator
        return Quiz_generator
@st.cache_data
def load_custom_css():
    return """
<style>
/* Compressed CSS - remove comments and whitespace in production */
:root {
    --bg-primary: #0f1419;
    --bg-secondary: #1a1f2e;
    --bg-tertiary: #252d3d;
    --text-primary: #ffffff;
    --text-secondary: #e0e0e0;
    --border-color: #3a4557;
    --accent-cyan: #00d9ff;
    --accent-emerald: #10b981;
    --accent-orange: #ff8c42;
    --accent-violet: #a78bfa;
    --accent-rose: #f43f5e;
}

.main, .stApp, html, body {
    background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, rgba(26, 31, 46, 0.95) 0%, rgba(37, 45, 61, 0.85) 100%) !important;
    border-right: 1px solid rgba(0, 217, 255, 0.15) !important;
    backdrop-filter: blur(10px);
}

h1, h2, h3, h4, h5, h6 { color: #ffffff !important; font-weight: 700; }
p, span, label { color: #e0e0e0 !important; }

.card {
    background: linear-gradient(135deg, rgba(37, 45, 61, 0.8) 0%, rgba(26, 31, 46, 0.9) 100%) !important;
    border: 1px solid rgba(0, 217, 255, 0.15) !important;
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.stButton > button {
    background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%) !important;
    color: #0f1419 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0, 217, 255, 0.4) !important;
}

.metric-card {
    background: linear-gradient(135deg, rgba(37, 45, 61, 0.8) 0%, rgba(26, 31, 46, 0.9) 100%) !important;
    border: 1px solid rgba(0, 217, 255, 0.15) !important;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.feature-card {
    background: linear-gradient(135deg, rgba(37, 45, 61, 0.7) 0%, rgba(26, 31, 46, 0.85) 100%) !important;
    border: 1px solid rgba(0, 217, 255, 0.15) !important;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
</style>
"""

st.markdown(load_custom_css(), unsafe_allow_html=True)


def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.pomodoro_sessions = 0
        st.session_state.total_study_time = 0
        st.session_state.flashcards = []
        st.session_state.current_flashcard_index = 0
        st.session_state.show_answer = False
        st.session_state.study_subjects = []
        st.session_state.quiz_questions = []
        st.session_state.initialized = True

init_session_state()

def get_flashcard_deck():
    if 'flashcard_deck' not in st.session_state:
        FlashcardGenerator= lazy_import_module('Flashcards_generator')
        st.session_state.flashcard_deck = FlashcardGenerator[0]()
    return st.session_state.flashcard_deck

def get_spaced_repetition():
    if 'spaced_repetition' not in st.session_state:
        FlashcardGenerator = lazy_import_module('Flashcards_generator')
        st.session_state.spaced_repetition = FlashcardGenerator[1]()
    return st.session_state.spaced_repetition

def get_summarizer():
    if 'summarizer' not in st.session_state:
        SmartSummarizer = lazy_import_module('SmartSummarizer')
        if SmartSummarizer:
            st.session_state.summarizer = SmartSummarizer.MultiLevelSummarizer()
        else:
            st.session_state.summarizer = None
    return st.session_state.summarizer


st.sidebar.markdown("""
<div style="text-align: center; padding: 24px 0; border-bottom: 1px solid rgba(0, 217, 255, 0.15); margin-bottom: 20px;">
    <h1 style="color: #00d9ff; font-size: 2.5rem; margin-bottom: 5px;">📚</h1>
    <h2 style="color: #ffffff; margin: 8px 0; font-size: 1.8rem;">StudyHub</h2>
    <p style="color: #a0aabb; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase;">Smart Learning</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📝 Smart Summarizer", "❓ Quiz Generator", "🗂️ Flashcards", 
     "⏱️ Pomodoro Timer", "📅 Study Planner"],
    label_visibility="collapsed"
)

st.sidebar.markdown("<hr style='border: 1px solid rgba(0, 217, 255, 0.15); margin: 20px 0;'>", unsafe_allow_html=True)

st.sidebar.markdown("### 📊 Quick Stats")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Sessions", 2, delta="+2 this week")
with col2:
    st.metric("Minutes", 45, delta="+45 today")

if page == "🏠 Home":
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 4rem; margin-bottom: 10px; color: #ffffff;">📚 StudyHub</h1>
        <h3 style="color: #00d9ff; font-size: 1.5rem; margin: 0;">Your All-in-One Smart Learning Platform</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style="color: #ffffff;">⏱️</h2>
            <h3 style="color: #00d9ff; font-size: 1.1rem;">Pomodoro Sessions</h3>
            <h1 style="color: #00d9ff;">{2}</h1>
            <p style='color: #7a8a9a; font-size: 0.9rem; margin-top: 10px;'>Track your focus sessions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style="color: #ffffff;">📝</h2>
            <h3 style="color: #00d9ff; font-size: 1.1rem;">Flashcards Created</h3>
            <h1 style="color: #00d9ff;">{10}</h1>
            <p style='color: #7a8a9a; font-size: 0.9rem; margin-top: 10px;'>Active recall material</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style="color: #ffffff;">📚</h2>
            <h3 style="color: #00d9ff; font-size: 1.1rem;">Study Minutes</h3>
            <h1 style="color: #00d9ff;">{45}</h1>
            <p style='color: #7a8a9a; font-size: 0.9rem; margin-top: 10px;'>Total focused time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h2>📝 Smart Summarizer</h2>
            <p>Transform lengthy texts into concise, easy-to-understand summaries. Perfect for quick revision!</p>
            <div style='display: flex; justify-content: space-between; margin-top: 20px;'>
                <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #4ade80; border: 1px solid rgba(16, 185, 129, 0.4);'>AI-Powered</span>
                <span style='background: rgba(0, 217, 255, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #22d3ee; border: 1px solid rgba(0, 217, 255, 0.4);'>Quick</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h2>❓ Quiz Generator</h2>
            <p>Generate custom quizzes from any text. Test your knowledge and track your progress!</p>
            <div style='display: flex; justify-content: space-between; margin-top: 20px;'>
                <span style='background: rgba(255, 140, 66, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #ffb366; border: 1px solid rgba(255, 140, 66, 0.4);'>Adaptive</span>
                <span style='background: rgba(167, 139, 250, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #c4b5fd; border: 1px solid rgba(167, 139, 250, 0.4);'>Interactive</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h2>🗂️ Flashcards</h2>
            <p>Create digital flashcards for active recall. The most effective way to memorize!</p>
            <div style='display: flex; justify-content: space-between; margin-top: 20px;'>
                <span style='background: rgba(244, 63, 94, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #ff6b7f; border: 1px solid rgba(244, 63, 94, 0.4);'>Spaced Repetition</span>
                <span style='background: rgba(0, 217, 255, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #22d3ee; border: 1px solid rgba(0, 217, 255, 0.4);'>Customizable</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h2>⏱️ Pomodoro Timer</h2>
            <p>Stay focused with timed work sessions. Includes break reminders and productivity tracking!</p>
            <div style='display: flex; justify-content: space-between; margin-top: 20px;'>
                <span style='background: rgba(244, 63, 94, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #ff6b7f; border: 1px solid rgba(244, 63, 94, 0.4);'>Focus Timer</span>
                <span style='background: rgba(255, 140, 66, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #ffb366; border: 1px solid rgba(255, 140, 66, 0.4);'>Break Alerts</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h2>📅 Study Planner</h2>
            <p>Plan your study sessions with smart scheduling. Never miss an exam deadline again!</p>
            <div style='display: flex; justify-content: space-between; margin-top: 20px;'>
                <span style='background: rgba(6, 182, 212, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.4);'>Calendar</span>
                <span style='background: rgba(0, 217, 255, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #22d3ee; border: 1px solid rgba(0, 217, 255, 0.4);'>Tracker</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        

elif page == "📝 Smart Summarizer":
    st.title("📝 Smart Summarizer")
    st.markdown("<p style='color: #00d9ff; font-size: 1.2rem; margin-bottom: 24px;'>Transform lengthy texts into concise summaries</p>", unsafe_allow_html=True)
    summarizer = get_summarizer()
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_text = st.text_area(
            "Paste your text here", 
            height=300, 
            placeholder="Enter the text you want to summarize..."
        )
    
    with col2:
        st.markdown("### ⚙️ Settings")
        summary_length = st.select_slider(
            "Summary Length", 
            options=["Brief", "Detailed"], 
            value="Brief"
        )
        summary_type = st.selectbox(
            "Summary Type", 
            ["Bullet Points", "Paragraph", "Key Concepts"]
        )
        create_mindmap = st.checkbox("Create MindMap")
        create_flowchart = st.checkbox("Create FlowChart")
        
        if st.button(" Generate Summary", use_container_width=True):
            if input_text:
                with st.spinner("--> Analyzing and generating summary..."):
                    try:
                        summarizer = st.session_state.summarizer
                        results = summarizer.summarize_all(input_text)
                        
                        if summary_length == 'Brief':
                            text = results['ultra_short']
                        else:
                            text = results['detailed']
        
                        if summary_type == 'Bullet Points':
                            text = results['bullet_points']
                        elif summary_type == 'Key Concepts':
                            text = results['key_terms']
                        
                        st.success(" Summary generated successfully!")
                     
                        st.markdown("###  Generated Summary")
                        if isinstance(text, list):
                            for item in text:
                                st.markdown(f"• {item}")
                        else:
                            st.markdown(f"""
                            <div class='feature-card' style='border-color: rgba(16, 185, 129, 0.3) !important;'>
                                <p style='color: #e0e0e0; line-height: 1.8;'>{text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        if create_mindmap:
                            st.markdown("### 🧠 Mind Map")
                            mindmap_path = results['mind_map']
                            try:
                                st.image(mindmap_path, caption="Generated Mind Map")
                            except Exception as e:
                                st.warning(f"Could not display mind map: {str(e)}")
                        if create_flowchart:
                            st.markdown("### 📊 Flowchart")
                            flowchart_path = results['flowchart']
                            try:
                                st.image(flowchart_path, caption="Generated Flowchart")
                            except Exception as e:
                                st.warning(f"Could not display flowchart: {str(e)}")

                        with st.expander("🔑 View Key Terms"):
                            key_terms = results['key_terms']
                            st.markdown("**Extracted Key Terms:**")
                            for term in key_terms:
                                st.markdown(f"• {term}")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating summary: {str(e)}")
                        st.info("Make sure all required dependencies (transformers, spacy, graphviz) are installed.")
            else:
                st.warning("⚠️ Please enter some text to summarize!")

elif page == "❓ Quiz Generator":
    st.title("❓ Quiz Generator")
    st.markdown("<p style='text-align: center; color: #666;'>Generate custom quizzes from your study material</p>", unsafe_allow_html=True)
    Quiz_generator = lazy_import_module('Quiz_generator')
    if 'quiz_generator' not in st.session_state:
        st.session_state.quiz_generator = Quiz_generator.QuizGenerator()
    if 'generated_quiz' not in st.session_state:
        st.session_state.generated_quiz = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'quiz_results' not in st.session_state:
        st.session_state.quiz_results = None
    
    tab1, tab2, tab3 = st.tabs(["📝 Create Quiz", "📊 Take Quiz", "📈 Results"])
    
    with tab1:
        quiz_text = st.text_area("Enter your study material", height=250, 
                                placeholder="Paste your notes, textbook content, or any study material here...")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            num_questions = st.number_input("Number of Questions", min_value=3, max_value=20, value=5)
        with col2:
            difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        with col3:
            question_type = st.selectbox("Question Type", 
                                        ["mixed", "mcq", "truefalse", "fillblank"],
                                        format_func=lambda x: {
                                            "mixed": "Mixed (All Types)",
                                            "mcq": "Multiple Choice",
                                            "truefalse": "True/False",
                                            "fillblank": "Fill in the Blank"
                                        }[x])
        
        personalized = st.checkbox("🎯 Personalized Quiz (Focus on struggled topics)", 
                                  value=False,
                                  help="Generate questions on topics you've struggled with previously")
        
        if st.button("🎯 Generate Quiz", use_container_width=True):
            if quiz_text and len(quiz_text.strip()) > 50:
                with st.spinner("Creating your quiz..."):
                    try:
                        quiz = st.session_state.quiz_generator.generate_quiz(
                            content=quiz_text,
                            question_type=question_type,
                            difficulty=difficulty,
                            num_questions=num_questions,
                            personalized=personalized
                        )
                        
                        if quiz['questions']:
                            st.session_state.generated_quiz = quiz
                            st.session_state.current_question = 0
                            st.session_state.user_answers = {}
                            st.session_state.quiz_submitted = False
                            st.session_state.quiz_results = None
                            st.success(f"✅ Quiz created successfully with {len(quiz['questions'])} questions!")
                            st.info("📝 Your quiz is ready! Switch to 'Take Quiz' tab to start answering questions.")
                        else:
                            st.error("❌ Could not generate questions from this content. Please try with more detailed material.")
                    except Exception as e:
                        st.error(f"❌ Error generating quiz: {str(e)}")
            elif quiz_text:
                st.warning("⚠️ Please enter more study material (at least 50 characters)!")
            else:
                st.warning("⚠️ Please enter study material first!")
        
        # Show struggled topics if any
        if st.session_state.quiz_generator.struggled_topics:
            with st.expander("📚 Topics to Review"):
                unique_topics = list(set(st.session_state.quiz_generator.struggled_topics[-10:]))
                for topic in unique_topics:
                    st.markdown(f"• {topic}")
    
    with tab2:
        if st.session_state.generated_quiz is None:
            st.info("📝 Please generate a quiz first in the 'Create Quiz' tab!")
        elif st.session_state.quiz_submitted:
            st.info("✅ Quiz completed! Check the 'Results' tab to see your score.")
        else:
            quiz = st.session_state.generated_quiz
            questions = quiz['questions']
            current_idx = st.session_state.current_question
            
            if current_idx < len(questions):
                question = questions[current_idx]
                
                # Progress bar
                progress = (current_idx + 1) / len(questions)
                st.progress(progress)
                
                st.markdown(f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 15px; border-radius: 10px; margin: 20px 0;'>
                    <h3 style='color: white; margin: 0;'>Question {current_idx + 1} of {len(questions)}</h3>
                    <p style='color: #f0f0f0; margin: 5px 0 0 0;'>
                        {question['difficulty'].upper()} • {question['type'].upper()}
                    </p>
                </div>""", unsafe_allow_html=True)
                
                st.markdown(f"### {question['question']}")
                
                # Answer input based on question type
                answer_key = f"answer_{current_idx}"
                
                if question['type'] == 'mcq':
                    user_answer = st.radio(
                        "Select your answer:",
                        question['options'],
                        key=answer_key,
                        index=None if answer_key not in st.session_state.user_answers else 
                              question['options'].index(st.session_state.user_answers[answer_key])
                    )
                    if user_answer:
                        st.session_state.user_answers[answer_key] = user_answer
                
                elif question['type'] == 'truefalse':
                    user_answer = st.radio(
                        "Select your answer:",
                        ["True", "False"],
                        key=answer_key,
                        index=None if answer_key not in st.session_state.user_answers else 
                              ["True", "False"].index(st.session_state.user_answers[answer_key])
                    )
                    if user_answer:
                        st.session_state.user_answers[answer_key] = user_answer
                
                elif question['type'] == 'fillblank':
                    user_answer = st.text_input(
                        "Your answer:",
                        key=answer_key,
                        value=st.session_state.user_answers.get(answer_key, "")
                    )
                    if user_answer:
                        st.session_state.user_answers[answer_key] = user_answer
                
                # Navigation buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if current_idx > 0:
                        if st.button("⏮️ Previous", use_container_width=True):
                            st.session_state.current_question -= 1
                            st.rerun()
                
                with col2:
                    if current_idx == len(questions) - 1:
                        if st.button("✓ Submit Quiz", use_container_width=True, type="primary"):
                            # Grade the quiz
                            answers_dict = {}
                            for idx, q in enumerate(questions):
                                answer_key = f"answer_{idx}"
                                answers_dict[q['id']] = st.session_state.user_answers.get(answer_key, "")
                            
                            results = st.session_state.quiz_generator.grade_quiz(quiz, answers_dict)
                            st.session_state.quiz_results = results
                            st.session_state.quiz_submitted = True
                            st.rerun()
                
                with col3:
                    if current_idx < len(questions) - 1:
                        if st.button("Next ⏭️", use_container_width=True):
                            st.session_state.current_question += 1
                            st.rerun()
                
                # Show answer status
                answered = sum(1 for idx in range(len(questions)) if f"answer_{idx}" in st.session_state.user_answers)
                st.markdown(f"**Answered:** {answered}/{len(questions)} questions")
    
    with tab3:
        if st.session_state.quiz_results is None:
            st.info("📊 Complete a quiz to see your results here!")
        else:
            results = st.session_state.quiz_results
            
            # Score display
            score_color = "#4CAF50" if results['percentage'] >= 70 else "#FF9800" if results['percentage'] >= 50 else "#F44336"
            st.markdown(f"""<div style='background: {score_color}; padding: 30px; 
                        border-radius: 15px; text-align: center; margin: 20px 0;'>
                <h1 style='color: white; margin: 0;'>{results['score']}/{results['total']}</h1>
                <h2 style='color: white; margin: 10px 0;'>{results['percentage']:.1f}%</h2>
                <p style='color: white; font-size: 18px; margin: 0;'>
                    {'Excellent!' if results['percentage'] >= 80 else 'Good Job!' if results['percentage'] >= 60 else 'Keep Practicing!'}
                </p>
            </div>""", unsafe_allow_html=True)
            
            # Detailed results
            st.markdown("### 📋 Detailed Results")
            
            for idx, result in enumerate(results['results'], 1):
                status_color = "#4CAF50" if result['correct'] else "#F44336"
                status_icon = "✓" if result['correct'] else "✗"
                
                with st.expander(f"{status_icon} Question {idx} - {result['topic']}", expanded=False):
                    st.markdown(f"**Question:** {result['question']}")
                    st.markdown(f"**Your Answer:** {result['your_answer']}")
                    st.markdown(f"**Correct Answer:** {result['correct_answer']}")
                    st.markdown(f"**Explanation:** {result['explanation']}")
                    st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{status_icon} {'CORRECT' if result['correct'] else 'INCORRECT'}</span>", 
                               unsafe_allow_html=True)
            
            # Reset button
            if st.button("🔄 Take Another Quiz", use_container_width=True):
                st.session_state.generated_quiz = None
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_results = None
                st.rerun()

elif page == "⏱️ Pomodoro Timer":
    st.title("⏱️ Pomodoro Timer")
    st.markdown("<p style='color: #f43f5e; font-size: 1.2rem; margin-bottom: 24px; text-align: center;'>Stay focused with timed study sessions</p>", unsafe_allow_html=True)
    Pamodoro_timer = lazy_import_module('Pamodoro_timer')
    # Initialize Pomodoro Timer and session state
    if 'pomodoro_timer' not in st.session_state:
        st.session_state.pomodoro_timer = Pamodoro_timer.PomodoroTimer()
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'timer_paused' not in st.session_state:
        st.session_state.timer_paused = False
    if 'current_time' not in st.session_state:
        st.session_state.current_time = 25 * 60
    if 'session_type' not in st.session_state:
        st.session_state.session_type = "work"
    if 'cycle_count' not in st.session_state:
        st.session_state.cycle_count = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    
    timer = st.session_state.pomodoro_timer
    
    # Settings section
    st.markdown("### ⚙️ Timer Settings")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        work_duration = st.number_input("Work Duration (min)", min_value=1, max_value=60, 
                                       value=timer.work_duration, key="work_dur",
                                       disabled=st.session_state.timer_running)
        timer.work_duration = work_duration
    
    with col2:
        short_break = st.number_input("Short Break (min)", min_value=1, max_value=30, 
                                     value=timer.short_break, key="short_br",
                                     disabled=st.session_state.timer_running)
        timer.short_break = short_break
    
    with col3:
        long_break = st.number_input("Long Break (min)", min_value=1, max_value=30, 
                                    value=timer.long_break, key="long_br",
                                    disabled=st.session_state.timer_running)
        timer.long_break = long_break
    
    col1, col2 = st.columns(2)
    with col1:
        sessions_goal = st.number_input("Sessions Goal", min_value=1, max_value=20, 
                                       value=timer.sessions_until_long_break,
                                       disabled=st.session_state.timer_running)
        timer.sessions_until_long_break = sessions_goal
    
    with col2:
        st.markdown(f"**Current Progress:** {timer.current_session} / {sessions_goal} sessions")
    
    
    st.markdown("---")
    
    # Timer display
    if st.session_state.timer_running or st.session_state.timer_paused:
        mins = st.session_state.current_time // 60
        secs = st.session_state.current_time % 60
        
        # Calculate progress
        if st.session_state.session_type == "work":
            total_duration = timer.work_duration * 60
        elif st.session_state.session_type == "short_break":
            total_duration = timer.short_break * 60
        else:
            total_duration = timer.long_break * 60
        
        progress = 1 - (st.session_state.current_time / total_duration)
        
        session_names = {
            "work": "🎯 FOCUS SESSION",
            "short_break": "☕ SHORT BREAK",
            "long_break": "🌙 LONG BREAK"
        }
        
        st.markdown(f"""<div style='background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;'>
            <h2 style='color: white; margin: 0;'>{session_names[st.session_state.session_type]}</h2>
            <h1 style='color: white; font-size: 4rem; margin: 20px 0;'>{mins:02d}:{secs:02d}</h1>
        </div>""", unsafe_allow_html=True)
        
      
        st.progress(progress)
        
        
        if st.session_state.session_type != "work" and 'current_suggestion' in st.session_state:
            st.info(f"💡 Suggestion: {st.session_state.current_suggestion}")
    else:
        st.markdown(f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 40px; border-radius: 15px; text-align: center; margin: 20px 0;'>
            <h1 style='color: white; font-size: 4rem; margin: 0;'>{timer.work_duration:02d}:00</h1>
            <p style='color: #f0f0f0; margin: 10px 0 0 0; font-size: 1.2rem;'>Ready to focus?</p>
        </div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not st.session_state.timer_running:
            if st.button("▶️ Start", use_container_width=True, type="primary"):
                st.session_state.timer_running = True
                st.session_state.timer_paused = False
                st.session_state.current_time = timer.work_duration * 60
                st.session_state.session_type = "work"
                st.session_state.start_time = datetime.now()
                st.rerun()
    
    with col2:
        if st.session_state.timer_running:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.timer_running = False
                st.session_state.timer_paused = True
        elif st.session_state.timer_paused:
            if st.button("▶️ Resume", use_container_width=True):
                st.session_state.timer_running = True
                st.session_state.timer_paused = False
                st.rerun()
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.current_time = timer.work_duration * 60
            st.session_state.session_type = "work"
            st.session_state.cycle_count = 0
            st.session_state.selected_music = None
            st.rerun()
    
    if st.session_state.timer_running:
        time.sleep(1)
        st.session_state.current_time -= 1
        
        if st.session_state.current_time <= 0:
            # Session completed
            if st.session_state.session_type == "work":
                # Log work session
                timer.current_session += 1
                timer.total_sessions += 1
                timer.total_focus_time += timer.work_duration
                
                session_log = {
                    'session_number': timer.total_sessions,
                    'type': 'work',
                    'duration': timer.work_duration,
                    'start_time': st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.start_time else '',
                    'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                timer.session_history.append(session_log)
                
                
                if timer.current_session % timer.sessions_until_long_break == 0:
                    st.session_state.session_type = "long_break"
                    st.session_state.current_time = timer.long_break * 60
                else:
                    st.session_state.session_type = "short_break"
                    st.session_state.current_time = timer.short_break * 60
                
          
                st.session_state.current_suggestion = timer.get_break_suggestion()
                st.balloons()
                st.success("🎉 Focus session completed!")
            else:
               
                break_type = st.session_state.session_type
                duration = timer.long_break if break_type == "long_break" else timer.short_break
                
                session_log = {
                    'session_number': timer.total_sessions,
                    'type': break_type,
                    'duration': duration,
                    'start_time': st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.start_time else '',
                    'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'suggestion': st.session_state.get('current_suggestion', '')
                }
                timer.session_history.append(session_log)
                
                st.session_state.session_type = "work"
                st.session_state.current_time = timer.work_duration * 60
                st.success("☕ Break completed! Time to focus again!")
            
            st.session_state.start_time = datetime.now()
        
        st.rerun()
    
    
    st.markdown("---")
    st.markdown("### 📊 Productivity Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🍅 Focus Sessions", timer.total_sessions)
    
    with col2:
        st.metric("⏱️ Total Focus Time", f"{timer.total_focus_time} min")
    
    with col3:
        total_breaks = len([s for s in timer.session_history if s['type'] != 'work'])
        st.metric("☕ Breaks Taken", total_breaks)
    
    with col4:
        hours = timer.total_focus_time / 60
        st.metric("📈 Hours Focused", f"{hours:.1f}h")
 
    if timer.total_focus_time >= 120:
        performance = "🔥 Excellent! You're on fire!"
        color = "#4CAF50"
    elif timer.total_focus_time >= 60:
        performance = "👍 Great work! Keep it up!"
        color = "#FF9800"
    elif timer.total_focus_time >= 25:
        performance = "✨ Good start! Building momentum!"
        color = "#2196F3"
    else:
        performance = "🌱 Just getting started!"
        color = "#9C27B0"
    
    st.markdown(f"""<div style='background: {color}; padding: 15px; border-radius: 10px; 
                text-align: center; margin: 20px 0;'>
        <p style='color: white; font-size: 1.2rem; margin: 0;'>{performance}</p>
    </div>""", unsafe_allow_html=True)
   
    if timer.session_history:
        with st.expander("📜 Session History"):
            for session in reversed(timer.session_history[-10:]):
                session_type = session['type'].replace('_', ' ').title()
                duration = session['duration']
                start = session['start_time'].split()[1][:5] if ' ' in session['start_time'] else session['start_time']
                
                if session['type'] == 'work':
                    icon = "🎯"
                elif 'long' in session['type']:
                    icon = "🌙"
                else:
                    icon = "☕"
                
                st.markdown(f"{icon} **{session_type}** - {duration} min @ {start}")

elif page == "📅 Study Planner":
    st.title("📅 Study Planner")
    st.markdown("<p style='color: #06b6d4; font-size: 1.2rem; margin-bottom: 24px; text-align: center;'>Plan and track your study sessions</p>", unsafe_allow_html=True)
    Study_planner = lazy_import_module('Study_planner')
    # Initialize Study Planner and session state
    if 'study_planner' not in st.session_state:
        st.session_state.study_planner = Study_planner.StudyPlanGenerator()
    if 'daily_goals_generated' not in st.session_state:
        st.session_state.daily_goals_generated = False
    if 'current_daily_goals' not in st.session_state:
        st.session_state.current_daily_goals = []
    
    planner = st.session_state.study_planner
    
    if planner.exam_date:
        days_left = planner.days_until_exam()
        countdown_color = "#f43f5e" if days_left <= 7 else "#ff8c42" if days_left <= 30 else "#06b6d4"
        st.markdown(f"""<div style='background: {countdown_color}; padding: 20px; 
                    border-radius: 15px; text-align: center; margin: 20px 0;'>
            <h2 style='color: white; margin: 0;'>📅 {days_left} Days Until Exam</h2>
            <p style='color: white; margin: 5px 0 0 0;'>Exam Date: {planner.exam_date.strftime('%B %d, %Y')}</p>
        </div>""", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Subjects", "🎯 Daily Goals", "📅 Weekly Plan", "📊 Progress"])
    
    with tab1:
        st.markdown("### 📚 Add Study Subjects")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject_name = st.text_input("Subject Name", placeholder="e.g., Mathematics, Physics, History")
            priority = st.selectbox("Priority Level", ["high", "medium", "low"],
                                   format_func=lambda x: x.capitalize())
        
        with col2:
            hours_needed = st.number_input("Total Hours Needed", min_value=1, max_value=200, value=20)
            exam_date_input = st.date_input("Exam Date")
        
      
        st.markdown("### ⚙️ Study Schedule Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            study_hours_per_day = st.number_input("Study Hours Per Day", 
                                                 min_value=1, max_value=12, 
                                                 value=planner.study_hours_per_day)
            planner.study_hours_per_day = study_hours_per_day
        
        with col2:
            if exam_date_input:
                st.info(f"📅 Exam set for: {exam_date_input.strftime('%B %d, %Y')}")
        
        notes = st.text_area("Notes (Optional)", placeholder="Add any additional notes or study tips...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ Add Subject", use_container_width=True, type="primary"):
                if subject_name and hours_needed:
                    planner.add_subject(subject_name, priority, hours_needed)
                    if exam_date_input:
                        planner.set_exam_date(exam_date_input.strftime('%Y-%m-%d'))
                    st.success(f"✅ {subject_name} added to study plan!")
                    st.balloons()
                else:
                    st.warning("⚠️ Please fill in subject name and hours needed!")
        
        with col2:
            if st.button("🗑️ Clear All Subjects", use_container_width=True):
                st.session_state.study_planner = Study_planner.StudyPlanGenerator()
                st.session_state.daily_goals_generated = False
                st.session_state.current_daily_goals = []
                st.success("All subjects cleared!")
                st.rerun()
        
        if planner.subjects:
            st.markdown("### 📋 Current Subjects")
            for idx, subject in enumerate(planner.subjects):
                priority_colors = {"high": "#f43f5e", "medium": "#ff8c42", "low": "#10b981"}
                completion_pct = (subject['hours_completed'] / subject['hours_needed'] * 100) if subject['hours_needed'] > 0 else 0
                
                st.markdown(f"""<div style='background: rgba(255,255,255,0.05); padding: 15px; 
                            border-radius: 10px; margin: 10px 0; border-left: 4px solid {priority_colors[subject['priority']]}'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h4 style='color: #06b6d4; margin: 0;'>{subject['name']}</h4>
                            <p style='color: #a0aabb; margin: 5px 0;'>
                                Priority: {subject['priority'].upper()} | 
                                Hours: {subject['hours_completed']}/{subject['hours_needed']}h ({completion_pct:.0f}%)
                            </p>
                        </div>
                        <span style='background: {priority_colors[subject['priority']]}; 
                               color: white; padding: 8px 16px; border-radius: 8px; font-weight: bold;'>
                            {subject['priority'].upper()}
                        </span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("📚 No subjects added yet. Add your first subject above!")
    
    with tab2:
        st.markdown("### 🎯 Today's Study Goals")
        
        if not planner.subjects:
            st.info("📚 Add subjects first to generate daily goals!")
        elif not planner.exam_date:
            st.warning("⚠️ Please set an exam date to generate goals!")
        else:
            if st.button("🔄 Generate Today's Goals", use_container_width=True, type="primary"):
                st.session_state.current_daily_goals = planner.generate_daily_goals()
                st.session_state.daily_goals_generated = True
                st.success("✅ Daily goals generated!")
            
            if st.session_state.daily_goals_generated and st.session_state.current_daily_goals:
                today = datetime.now().strftime('%B %d, %Y')
                st.markdown(f"**📅 Goals for {today}**")
                st.markdown(f"**⏰ Total Study Time Today:** {planner.study_hours_per_day} hours")
                
                st.markdown("---")
                
                for goal in st.session_state.current_daily_goals:
                    is_completed = goal['id'] in planner.completed_goals
                    status_icon = "✅" if is_completed else "⭕"
                    
                    with st.expander(f"{status_icon} {goal['subject']} - {goal['hours']}h", expanded=not is_completed):
                        st.markdown(f"**Subject:** {goal['subject']}")
                        st.markdown(f"**Time Allocation:** {goal['hours']} hours")
                        
                        st.markdown("**Tasks:**")
                        for task in goal['tasks']:
                            st.markdown(f"• {task}")
                        
                        col1, col2 = st.columns([3, 1])
                        with col2:
                            if not is_completed:
                                if st.button("✓ Complete", key=f"complete_{goal['id']}", use_container_width=True):
                                    planner.mark_goal_complete(goal['id'])
                                    st.success(f"🎉 Goal completed for {goal['subject']}!")
                                    st.rerun()
                            else:
                                st.success("Done! ✓")
            
                completed_count = sum(1 for g in st.session_state.current_daily_goals if g['id'] in planner.completed_goals)
                total_count = len(st.session_state.current_daily_goals)
                progress_pct = (completed_count / total_count * 100) if total_count > 0 else 0
                
                st.markdown("---")
                st.markdown("### 📈 Today's Progress")
                st.progress(progress_pct / 100)
                st.markdown(f"**{completed_count}/{total_count}** goals completed ({progress_pct:.0f}%)")
            
            elif st.session_state.daily_goals_generated:
                st.info("🎉 All goals completed for today! Great work!")
    
    with tab3:
        st.markdown("### 📅 Weekly Review Plan")
        
        if not planner.subjects:
            st.info("📚 Add subjects first to generate weekly plan!")
        else:
            weekly_plan = planner.generate_weekly_review()
            
            for day in weekly_plan:
                is_weekend = day['day'] in ['Saturday', 'Sunday']
                bg_color = "rgba(244, 63, 94, 0.1)" if is_weekend else "rgba(6, 182, 212, 0.1)"
                icon = "📝" if is_weekend else "📚"
                
                st.markdown(f"""<div style='background: {bg_color}; padding: 20px; 
                            border-radius: 10px; margin: 15px 0; border-left: 4px solid #06b6d4;'>
                    <h3 style='color: #06b6d4; margin: 0 0 10px 0;'>
                        {icon} {day['day']} - {day['date']}
                    </h3>
                    <p style='color: #e0e0e0; margin: 5px 0;'>
                        <strong>Activity:</strong> {day['activity']}
                    </p>
                    <p style='color: #a0aabb; margin: 5px 0;'>
                        <strong>Focus:</strong> {day['focus']}
                    </p>
                </div>""", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📊 Progress Summary")
        
        if not planner.subjects:
            st.info("📚 Add subjects to track progress!")
        else:
            progress_summary = planner.get_progress_summary()
            
            # Overall statistics
            total_hours_needed = sum(s['hours_needed'] for s in planner.subjects)
            total_hours_completed = sum(s['hours_completed'] for s in planner.subjects)
            overall_progress = (total_hours_completed / total_hours_needed * 100) if total_hours_needed > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📚 Total Subjects", len(planner.subjects))
            
            with col2:
                st.metric("⏰ Hours Completed", f"{total_hours_completed:.1f}h")
            
            with col3:
                st.metric("📖 Hours Remaining", f"{total_hours_needed - total_hours_completed:.1f}h")
            
            with col4:
                st.metric("📈 Overall Progress", f"{overall_progress:.1f}%")
            
            st.markdown("---")
            
           
            st.markdown("### 📋 Subject-wise Progress")
            
            for item in progress_summary:
                # Color based on completion
                if item['completion'] >= 80:
                    color = "#10b981"
                    status = "🔥 Almost Done!"
                elif item['completion'] >= 50:
                    color = "#ff8c42"
                    status = "👍 On Track"
                elif item['completion'] >= 25:
                    color = "#06b6d4"
                    status = "✨ Making Progress"
                else:
                    color = "#f43f5e"
                    status = "🌱 Getting Started"
                
                st.markdown(f"""<div style='background: rgba(255,255,255,0.05); padding: 20px; 
                            border-radius: 10px; margin: 15px 0;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                        <h4 style='color: {color}; margin: 0;'>{item['subject']}</h4>
                        <span style='color: {color}; font-size: 0.9rem;'>{status}</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 5px; overflow: hidden; margin: 10px 0;'>
                        <div style='background: {color}; width: {item['completion']}%; 
                             height: 24px; border-radius: 5px; transition: width 0.3s; 
                             display: flex; align-items: center; justify-content: center;'>
                            <span style='color: white; font-weight: bold; font-size: 0.85rem;'>
                                {item['completion']:.1f}%
                            </span>
                        </div>
                    </div>
                    <p style='color: #a0aabb; margin: 5px 0;'>
                        {item['hours_completed']:.1f} of {item['hours_total']}h completed | 
                        {item['hours_total'] - item['hours_completed']:.1f}h remaining
                    </p>
                </div>""", unsafe_allow_html=True)
     
            if overall_progress >= 75:
                message = "🔥 Excellent progress! Keep up the great work!"
                msg_color = "#10b981"
            elif overall_progress >= 50:
                message = "👍 Good progress! Stay focused!"
                msg_color = "#ff8c42"
            elif overall_progress >= 25:
                message = "✨ Making progress! Keep going!"
                msg_color = "#06b6d4"
            else:
                message = "🌱 Just getting started! You can do it!"
                msg_color = "#f43f5e"
            
            st.markdown(f"""<div style='background: {msg_color}; padding: 15px; 
                        border-radius: 10px; text-align: center; margin: 20px 0;'>
                <p style='color: white; font-size: 1.2rem; margin: 0;'>{message}</p>
            </div>""", unsafe_allow_html=True)
            
            if st.button("📥 Export Study Plan", use_container_width=True):
                export_data = {
                    "subjects": planner.subjects,
                    "exam_date": planner.exam_date.strftime('%Y-%m-%d') if planner.exam_date else None,
                    "study_hours_per_day": planner.study_hours_per_day,
                    "overall_progress": overall_progress,
                    "progress_summary": progress_summary
                }
                st.download_button(
                    label="💾 Download as JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"study_plan_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                st.success("📥 Study plan ready for download!")
elif page == "🗂️ Flashcards":
    st.title("🗂️ Flashcards")
    st.markdown("<p style='color: #a78bfa; font-size: 1.2rem; margin-bottom: 24px;'>Create and review flashcards with spaced repetition</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Create Cards", "🎴 Review Cards", "📊 Statistics", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### Create New Flashcards")
        
        f = get_flashcard_deck()
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Method 1: Manual Entry")
            front = st.text_input("Front of Card", placeholder="Enter question or term...")
            back = st.text_area("Back of Card", placeholder="Enter answer or definition...", height=150)
            
            if st.button("➕ Add Card", use_container_width=True):
                if front and back:
                    f.add_manual_card(front, back)
                    st.success("✅ Card added successfully!")
                    st.balloons()
                else:
                    st.warning("⚠️ Please fill both front and back!")
        
        with col2:
            st.markdown("#### Method 2: Import from Text")
            notes_text = st.text_area(
                "Paste your notes here", 
                height=200,
                placeholder="""Format examples:
Q: What is photosynthesis?
A: Process by which plants convert light to energy

- Mitochondria: Powerhouse of the cell
- Ribosomes: Protein synthesis

# Biology Chapter 1
The study of living organisms..."""
            )
            
            if st.button("📥 Generate Cards from Text", use_container_width=True):
                if notes_text:
                    with st.spinner("Parsing notes and generating cards..."):
                        count = f.generate_flashcards(notes_text)
                        st.success(f"✅ Generated {count} new flashcards!")
                else:
                    st.warning("⚠️ Please enter some text!")

        all_cards = f.get_all_cards()
        if all_cards:
            st.markdown("### Recent Cards")
            recent_cards = all_cards[-5:]
            for card in recent_cards:
                with st.expander(f"📄 {card['front'][:50]}..." if len(card['front']) > 50 else f"📄 {card['front']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Front:** {card['front']}")
                    with col2:
                        st.markdown(f"**Back:** {card['back']}")
                    st.caption(f"Created: {card['created'][:10]}")

    with tab2:
        st.markdown("### Review Flashcards")
        f = get_flashcard_deck()
        s = get_spaced_repetition()
        due_cards = s.get_due_cards()
        all_cards = f.get_all_cards()

        if not all_cards:
            st.info("📚 No flashcards created yet! Create some cards first.")
        elif not due_cards:
            st.success("🎉 All cards mastered! No reviews due.")
            st.info("Create more cards or wait for next review cycle.")
        else:
            if 'review_cards' not in st.session_state:
                st.session_state.review_cards = due_cards
                st.session_state.current_review_index = 0
                st.session_state.review_quality = None
            
            if 'review_cards' in st.session_state and st.session_state.review_cards:
                current_idx = st.session_state.current_review_index
                current_card = st.session_state.review_cards[current_idx]
                
                progress = (current_idx + 1) / len(st.session_state.review_cards)
                st.progress(progress)
                st.markdown(f"**Card {current_idx + 1} of {len(st.session_state.review_cards)}**")
                
                st.markdown(f"""
                <div class='feature-card' style='border-color: rgba(167, 139, 250, 0.3) !important; text-align: center; padding: 40px;'>
                    <h2 style='color: #a78bfa;'>{current_card['front']}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                if not st.session_state.get('show_review_answer', False):
                    if st.button("🔍 Reveal Answer", use_container_width=True):
                        st.session_state.show_review_answer = True
                        st.rerun()
                else:
                    st.markdown(f"""
                    <div class='feature-card' style='border-color: rgba(16, 185, 129, 0.3) !important; text-align: center; padding: 40px;'>
                        <h3 style='color: #10b981;'>{current_card['back']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### How well did you recall?")
                    
                    col1, col2, col3, col4, col5, col6 = st.columns(6)
                    
                    with col1:
                        if st.button("0️⃣", use_container_width=True, help="Complete blackout"):
                            st.session_state.review_quality = 0
                    with col2:
                        if st.button("1️⃣", use_container_width=True, help="Incorrect, but familiar"):
                            st.session_state.review_quality = 1
                    with col3:
                        if st.button("2️⃣", use_container_width=True, help="Incorrect, but easy to recall"):
                            st.session_state.review_quality = 2
                    with col4:
                        if st.button("3️⃣", use_container_width=True, help="Correct, but difficult"):
                            st.session_state.review_quality = 3
                    with col5:
                        if st.button("4️⃣", use_container_width=True, help="Correct, with hesitation"):
                            st.session_state.review_quality = 4
                    with col6:
                        if st.button("5️⃣", use_container_width=True, help="Perfect recall"):
                            st.session_state.review_quality = 5
                    
                    if st.session_state.review_quality is not None:
                        quality = st.session_state.review_quality
                        updated_card = s.review_card(current_card, quality)
                        
                        if current_idx < len(st.session_state.review_cards) - 1:
                            st.session_state.current_review_index += 1
                            st.session_state.show_review_answer = False
                            st.session_state.review_quality = None
                            st.rerun()
                        else:
                            st.success("✅ Review session complete!")
                            if st.button("🔄 Start New Review Session", use_container_width=True):
                                del st.session_state.review_cards
                                del st.session_state.current_review_index
                                del st.session_state.show_review_answer
                                del st.session_state.review_quality
                                st.rerun()
            
            elif not st.session_state.get('review_cards'):
                st.markdown(f"**{len(due_cards)} cards due for review**")
                if st.button("▶️ Start Review Session", use_container_width=True, type="primary"):
                    st.session_state.review_cards = due_cards
                    st.session_state.current_review_index = 0
                    st.session_state.show_review_answer = False
                    st.rerun()

    with tab3:
        st.markdown("### 📊 Flashcard Statistics")
        
        f = get_flashcard_deck()
        s = get_spaced_repetition()
        stats = f.get_card_stats()
        sr_stats = s.get_card_stats()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Cards", stats["total"])
        
        with col2:
            st.metric("Due for Review", stats["due"])
        
        with col3:
            st.metric("Mastered", stats["mastered"])
        
        with col4:
            st.metric("Mastery", f"{stats['mastery_percentage']:.1f}%")
        
        st.markdown("### Progress Overview")
        if stats["total"] > 0:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(stats["mastery_percentage"] / 100)
            
            with col2:
                mastery_color = "#10b981" if stats["mastery_percentage"] >= 70 else "#ff8c42" if stats["mastery_percentage"] >= 40 else "#f43f5e"
                st.markdown(f"<p style='color: {mastery_color}; font-weight: bold; font-size: 1.2rem;'>{stats['mastery_percentage']:.1f}%</p>", unsafe_allow_html=True)
        
        st.markdown("### Recent Activity")
        all_cards = f.get_all_cards()
        if all_cards:
            recent = sorted(all_cards, key=lambda x: x.get('next_review', ''), reverse=True)[:5]
            for card in recent:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.text(card['front'][:50] + "..." if len(card['front']) > 50 else card['front'])
                with col2:
                    next_review = datetime.fromisoformat(card['next_review']).strftime('%b %d')
                    st.text(f"Review: {next_review}")
                with col3:
                    st.text(f"Ease: {card['ease_factor']:.2f}")

    with tab4:
        st.markdown("### ⚙️ Flashcard Settings")
        
        f = get_flashcard_deck()
        s = get_spaced_repetition()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Deck Management")
            
            if st.button("🔄 Reload from File", use_container_width=True):
                f = get_flashcard_deck()
                s = get_spaced_repetition()
                st.success("✅ Deck reloaded!")
            
            if st.button("💾 Save to File", use_container_width=True):
                f.save_deck()
                st.success("✅ Deck saved!")
            
            if st.button("🗑️ Clear All Cards", use_container_width=True, type="secondary"):
                if st.checkbox("I'm sure I want to delete all cards"):
                    f.deck["cards"] = []
                    f.save_deck()
                    s.deck["cards"] = []
                    s.save_deck()
                    st.success("✅ All cards cleared!")
        
        with col2:
            st.markdown("#### Export/Import")
            
            if st.button("📥 Export as JSON", use_container_width=True):
                deck_data = f.deck
                st.download_button(
                    label="💾 Download JSON",
                    data=json.dumps(deck_data, indent=2),
                    file_name=f"flashcards_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            
            uploaded_file = st.file_uploader("Import JSON file", type=['json'])
            if uploaded_file is not None:
                try:
                    imported_deck = json.load(uploaded_file)
                    if st.button("📤 Import Cards", use_container_width=True):
                        existing_cards = f.get_all_cards()
                        existing_fronts = {card["front"] for card in existing_cards}
                        
                        added = 0
                        for card in imported_deck.get("cards", []):
                            if card["front"] not in existing_fronts:
                                f.deck["cards"].append(card)
                                added += 1
                        
                        if added > 0:
                            f.save_deck()
                            s.deck["cards"] = f.deck["cards"]
                            s.save_deck()
                            st.success(f"✅ Imported {added} new cards!")
                except Exception as e:
                    st.error(f"Error importing file: {str(e)}")