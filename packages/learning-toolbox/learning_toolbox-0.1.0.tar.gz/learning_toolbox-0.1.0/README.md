# Learning Toolbox Library

A Python library for generating learning resources like notes, quizzes, YouTube summaries, and mind maps using the Gemini AI and other tools.

## Installation

1.  **Install via pip (recommended):**

    If you create a `setup.py` (see below), you can install the library using pip:

    ```bash
     pip install learning-toolbox
     npm install -g @mermaid-js/mermaid-cli
    ```

2.  **Manual Installation:**

    Copy the `learning_toolbox` directory into your Python project's directory or somewhere in your Python path.

    **Dependencies:**

    *   `google-generativeai`
    *   `pdfkit`
    *   `markdown2`
    *   `youtube-transcript-api`
    *   `mermaid-cli` (must be installed separately on your system for mind maps)
     ```bash
     npm install -g @mermaid-js/mermaid-cli
    ```

    Install dependencies using pip:

    ```bash
    pip install google-generativeai pdfkit markdown2 youtube-transcript-api
    ```

## Usage

Here's how to use the `learning_toolbox` library in your Python project:

```python
from learning_toolbox import generate_content, save_files

# Set your Gemini API key (replace with your actual key or set as environment variable)
api_key = 'YOUR_GEMINI_API_KEY'

# Example 1: Generate study notes
topic_notes = "Quantum Physics"
notes_content = generate_content(topic_notes, content_type="notes", api_key=api_key)
if notes_content and not notes_content.startswith("Error"):
    md_notes_file, pdf_notes_file = save_files(topic_notes, notes_content, content_type="notes", base_dir="./output_resources")
    print(f"Notes saved to: {md_notes_file}, {pdf_notes_file}")
else:
    print(f"Error generating notes: {notes_content}")


# Example 2: Generate a quiz
topic_quiz = "Python Programming Basics"
quiz_content = generate_content(topic_quiz, content_type="quiz", api_key=api_key)
if quiz_content and not quiz_content.startswith("Error"):
    md_quiz_file, pdf_quiz_file = save_files(topic_quiz, quiz_content, content_type="quiz", base_dir="./output_resources")
    print(f"Quiz saved to: {md_quiz_file}, {pdf_quiz_file}")
else:
    print(f"Error generating quiz: {quiz_content}")

# Example 3: Summarize a YouTube video
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Replace with a real video URL
summary_content = generate_content(youtube_url, content_type="youtube_summary", api_key=api_key)
if summary_content and not summary_content.startswith("Error"):
    md_summary_file, pdf_summary_file = save_files(youtube_url, summary_content, content_type="youtube_summary", base_dir="./output_resources")
    print(f"YouTube summary saved to: {md_summary_file}, {pdf_summary_file}")
else:
    print(f"Error generating YouTube summary: {summary_content}")

# Example 4: Generate a mind map
topic_mindmap = "Web Development Fundamentals"
mindmap_content = generate_content(topic_mindmap, content_type="mindmap", api_key=api_key)
if mindmap_content and not mindmap_content.startswith("Error"):
    mindmap_image_file, _ = save_files(topic_mindmap, mindmap_content, content_type="mindmap", base_dir="./output_resources") # pdf_file will be None for mindmap
    print(f"Mind map saved to: {mindmap_image_file}")
else:
    print(f"Error generating mind map: {mindmap_content}")