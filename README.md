# Study_Hub

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![Transformers](https://img.shields.io/badge/Transformers-4.0+-yellow.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B.svg)

A comprehensive collection of intelligent educational and productivity tools powered by machine learning, featuring a custom fine-tuned BART model for advanced text summarization.

[Features](#key-features) • [Installation](#getting-started) • [Usage](#usage) • [Model Performance](#model-performance) • [Contributing](#contributing)

</div>

---

## Overview

This project combines multiple AI-driven applications designed to enhance learning efficiency and productivity. The suite includes smart summarization, quiz generation, flashcard creation, study planning, and various visualization tools, all built with modern NLP techniques.

---

## Key Features

### Smart Summarizer (Core Module)

<table>
<tr>
<td>

- **Custom Fine-Tuned BART Model** trained on the BBC News dataset
- **ROUGE-1 Score: 0.61** - demonstrating strong summarization performance
- Efficiently condenses long articles and documents while preserving key information
- Optimized for news articles and general text content

</td>
</tr>
</table>

### Additional Tools

| Tool | Description |
|------|-------------|
| **Quiz Generator** | Automatically creates quizzes from text content |
| **Flashcards Generator** | Transforms study material into interactive flashcards |
| **Study Planner** | Organizes learning schedules and tracks progress |
| **Pomodoro Timer** | Time management tool using the Pomodoro Technique |
| **Streamlit App** | User-friendly web interface for all tools |

---

## Model Performance

The fine-tuned BART model was trained on the BBC News Summary dataset:

<table align="center">
<tr>
<th>Metric</th>
<th>Value</th>
</tr>
<tr>
<td><b>ROUGE-1 Score</b></td>
<td><code>0.61</code></td>
</tr>
<tr>
<td><b>Dataset</b></td>
<td>BBC News Articles</td>
</tr>
<tr>
<td><b>Base Model</b></td>
<td>Facebook BART</td>
</tr>
<tr>
<td><b>Training Method</b></td>
<td>Fine-tuning for extractive and abstractive summarization</td>
</tr>
</table>

---

## Tech Stack

<table>
<tr>
<td align="center" width="20%">
<b>Deep Learning</b><br>
PyTorch<br>
Transformers (Hugging Face)
</td>
<td align="center" width="20%">
<b>NLP Model</b><br>
BART<br>
(fine-tuned)
</td>
<td align="center" width="20%">
<b>Frontend</b><br>
Streamlit
</td>
<td align="center" width="20%">
<b>Data Processing</b><br>
Python<br>
Pandas
</td>
<td align="center" width="20%">
<b>Visualization</b><br>
Matplotlib<br>
Plotly
</td>
</tr>
</table>

---

## Project Structure

```
.
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
```

---

## Getting Started

### Prerequisites

```bash
pip install transformers torch streamlit pandas numpy
```

### Installation

**1. Clone the repository:**

```bash
git clone https://github.com/yourusername/ai-learning-suite.git
cd ai-learning-suite
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Run the Streamlit app:**

```bash
streamlit run Streamlit_app.py
```

---

## Usage

### Smart Summarizer

```python
from SmartSummarizer import summarize_text

text = "Your long article or document here..."
summary = summarize_text(text)
print(summary)
```

### Web Interface

Navigate to the Streamlit app and select your desired tool from the sidebar. Upload or paste your content and let the AI do the work!

---

## Model Training

The BART model was fine-tuned on the BBC News Summary dataset using the following approach:

> **Training Pipeline**
> - Transfer learning from pre-trained BART-base
> - Custom training loop with AdamW optimizer
> - Evaluation using ROUGE metrics
> - Achieved competitive performance with **ROUGE-1: 0.61**

---

## Use Cases

<table>
<tr>
<td width="25%">

**Students**

Summarize textbooks, generate study materials, manage study time

</td>
<td width="25%">

**Researchers**

Quick article summarization and knowledge extraction

</td>
<td width="25%">

**Professionals**

Digest reports, meeting notes, and documentation

</td>
<td width="25%">

**Content Creators**

Extract key points from research materials

</td>
</tr>
</table>

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Acknowledgments

<table>
<tr>
<td>

- BBC News Summary Dataset
- Hugging Face Transformers library
- Facebook AI Research (BART model)
- Streamlit team for the amazing framework

</td>
</tr>
</table>

---

<div align="center">


[⬆ Back to Top](#ai-powered-learning--productivity-suite)

</div>
