 ##AI-Powered Learning & Productivity Suite 
A comprehensive collection of intelligent educational and productivity tools powered by machine learning, featuring a custom fine-tuned BART model for advanced text summarization.
#Overview
This project combines multiple AI-driven applications designed to enhance learning efficiency and productivity. The suite includes smart summarization, quiz generation, flashcard creation, study planning, and various visualization tools, all built with modern NLP techniques.
#Key Features
Smart Summarizer (Core Module)

Custom Fine-Tuned BART Model trained on the BBC News dataset
ROUGE-1 Score: 0.61 - demonstrating strong summarization performance
Efficiently condenses long articles and documents while preserving key information
Optimized for news articles and general text content

#Additional Tools

Quiz Generator - Automatically creates quizzes from text content
Flashcards Generator - Transforms study material into interactive flashcards
Study Planner - Organizes learning schedules and tracks progress
Pomodoro Timer - Time management tool using the Pomodoro Technique
Streamlit App - User-friendly web interface for all tools

#Model Performance
The fine-tuned BART model was trained on the BBC News Summary dataset:

ROUGE-1 Score: **0.61**
Dataset: BBC News articles
Base Model: Facebook BART (Bidirectional and Auto-Regressive Transformers)
Training: Custom fine-tuning for extractive and abstractive summarization

#Tech Stack

Deep Learning: PyTorch, Transformers (Hugging Face)
NLP Model: BART (fine-tuned)
Frontend: Streamlit
Data Processing: Python, Pandas
Visualization: Matplotlib/Plotly (flowchart.png, mindmap.png)

📁 Project Structure
├── fine_tuned_bart_model/      # Custom trained BART model
├── SmartSummarizer.py          # Main summarization module
├── Streamlit_app.py            # Web application interface
├── Quiz_generator.py           # Automated quiz creation
├── Flashcards_generator.py     # Flashcard generation tool
├── Study_planner.py            # Study schedule organizer
├── Pomodoro_timer.py           # Productivity timer
├── text_summarization_ba...    # Training/evaluation scripts
├── flashcards.json             # Flashcard data storage
└── BBC News Summary/           # Training dataset
#Getting Started
Prerequisites
bashpip install transformers torch streamlit pandas numpy
Installation

Clone the repository:

bashgit clone https://github.com/yourusername/ai-learning-suite.git
cd ai-learning-suite

Install dependencies:

bashpip install -r requirements.txt

Run the Streamlit app:

bashstreamlit run Streamlit_app.py
#Usage
Smart Summarizer
pythonfrom SmartSummarizer import summarize_text
text = "Your long article or document here..."
summary = summarize_text(text)
print(summary)
Web Interface
Navigate to the Streamlit app and select your desired tool from the sidebar. Upload or paste your content and let the AI do the work!
#Model Training
The BART model was fine-tuned on the BBC News Summary dataset using the following approach:
Transfer learning from pre-trained BART-base
Custom training loop with AdamW optimizer
Evaluation using ROUGE metrics
Achieved competitive performance with ROUGE-1: 0.61

#Use Cases

Students: Summarize textbooks, generate study materials, manage study time
Researchers: Quick article summarization and knowledge extraction
Professionals: Digest reports, meeting notes, and documentation
Content Creators: Extract key points from research materials

 library
Facebook AI Research (BART model)
Streamlit team for the amazing framework
