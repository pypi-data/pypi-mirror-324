# learning_toolbox/file_handler.py

import os
import pdfkit
import markdown2

def create_mermaid_mindmap(content):
    """Creates Mermaid markdown content for a mind map."""
    lines = content.split('\n')
    mermaid_content = ["mindmap"]
    root = lines[0].strip()
    mermaid_content.append(f"  root((%s))" % root)

    for line in lines[1:]:
        if not line.strip():
            continue

        level = line.count('  ') + line.count('- ')
        node = line.strip('- ').strip()
        if not node:
            continue

        indent = "  " * (level + 1)
        mermaid_content.append(f"{indent}{node}")

    return "\n".join(mermaid_content)


def save_mindmap(content, filename):
    """Saves a mind map as a PNG image using Mermaid CLI."""
    try:
        # Create temporary mermaid file
        temp_md = filename.replace('.png', '.mmd')
        with open(temp_md, 'w') as f:
            f.write(content)

        # Convert to PNG using mermaid-cli
        os.system(f'mmdc -i "{temp_md}" -o "{filename}" -b white')

        # Cleanup temporary file
        os.remove(temp_md)
        return True
    except Exception as e:
        print(f"Error creating mind map: {e}")
        return False


def markdown_to_pdf(markdown_text, output_filename, wkhtmltopdf_path=None):
    """Converts markdown text to PDF using wkhtmltopdf."""
    try:
        # Use provided path or try to find wkhtmltopdf in the library's wkhtmltopdf/bin folder
        if wkhtmltopdf_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            wkhtmltopdf_path_default = os.path.join(current_dir, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe') # Go up one level to library root
            if os.path.exists(wkhtmltopdf_path_default):
                wkhtmltopdf_path = wkhtmltopdf_path_default
            else:
                print("Warning: wkhtmltopdf not found in default library path. Ensure it's in your system PATH or provide wkhtmltopdf_path argument.")
                config = pdfkit.configuration() # Try system path if not found in library, user might have it installed globally.
                pdfkit.from_string(markdown2.markdown(markdown_text), output_filename, configuration=config) # Attempt to generate PDF even if default path fails.
                return os.path.exists(output_filename) # Return success status based on file creation.


        if wkhtmltopdf_path and not os.path.exists(wkhtmltopdf_path):
            print(f"Error: wkhtmltopdf not found at {wkhtmltopdf_path}")
            return False


        # Convert markdown to HTML
        html = markdown2.markdown(markdown_text)

        # HTML template with styling
        html_content = f"""
          <html>
            <head>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #3498db; }}
            code {{ background: #f8f9fa; padding: 2px 5px; }}
            pre {{ background: #f8f9fa; padding: 15px; }}
        </style>
    </head>
    <body>{html}</body>
        </html>
"""

        # Configure pdfkit with correct wkhtmltopdf path
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Generate PDF with config
        pdfkit.from_string(html_content, output_filename, configuration=config)

        return os.path.exists(output_filename)

    except Exception as e:
        print(f"PDF conversion error: {e}")
        return False


def save_files(topic, content, content_type="notes", base_dir=None):
    """Saves content to files outside the learning_toolbox directory.
    
    Args:
        topic (str): The topic of the content.
        content (str): The content to save.
        content_type (str): Type of content ('notes', 'quiz', 'youtube_summary', 'mindmap').
        base_dir (str, optional): Base directory to save the 'output_resource' folder in.
                                If None, 'output_resource' is created in parent directory.
    """
    output_resource_name = 'output_resource'

    # Get the learning_toolbox directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # If base_dir is not provided, create output_resource in parent directory
    if base_dir is None:
        # Go up one level from learning_toolbox directory
        output_base_path = os.path.dirname(current_dir)
    else:
        output_base_path = base_dir

    output_root_dir = os.path.join(output_base_path, output_resource_name)

    # Rest of your existing directory creation code...
    notes_dir = os.path.join(output_root_dir, 'notes')
    mindmap_dir = os.path.join(output_root_dir, 'mindmaps')
    youtube_dir = os.path.join(output_root_dir, 'youtube')
    markdown_dir = os.path.join(output_root_dir, 'markdown')

    directories_to_create = [output_root_dir, notes_dir, mindmap_dir, youtube_dir, markdown_dir]
    for directory in directories_to_create:
        if not os.path.exists(directory):
            os.makedirs(directory)

    md_filename, pdf_filename = None, None

    if content_type == "mindmap":
        try:
            base_name = topic.replace(' ', '_').lower()
            mindmap_filename = os.path.join(mindmap_dir, f"{base_name}_mindmap.png")
            mermaid_content = create_mermaid_mindmap(content)
            mindmap_saved_successfully = save_mindmap(mermaid_content, mindmap_filename)

            if mindmap_saved_successfully and os.path.exists(mindmap_filename):
                print(f"MINDMAP:{mindmap_filename}")
                return mindmap_filename, None
            else:
                print("Failed to generate mind map image in save_files.")
                return None, None

        except Exception as e:
            print(f"Error: Failed to create mind map - {str(e)}")
            return None, None

    elif content_type == "youtube_summary":
        from .content_generator import get_video_id
        video_id = get_video_id(topic)
        base_name = f"youtube_{video_id}" if video_id else "youtube_summary"
        md_filename = os.path.join(youtube_dir, f"{base_name}_summary.md")
        pdf_filename = os.path.join(youtube_dir, f"{base_name}_summary.pdf")

        try:
            with open(md_filename, "w", encoding='utf-8') as f:
                f.write(content)
            if markdown_to_pdf(content, pdf_filename):
                print(f"MARKDOWN:{md_filename}")
                print(f"PDF:{pdf_filename}")
            else:
                print(f"Failed to generate PDF for youtube summary")

        except Exception as e:
            print(f"Error saving youtube summary files: {e}")
            md_filename, pdf_filename = None, None


    else: # "notes" or "quiz"
        base_name = topic.replace(' ', '_').lower()
        md_filename = os.path.join(notes_dir, f"{base_name}_notes.md") # Default to notes
        pdf_filename = os.path.join(notes_dir, f"{base_name}_notes.pdf") # Default to notes
        if content_type == "quiz": # Adjust filenames if it's a quiz
            md_filename = os.path.join(notes_dir, f"{base_name}_quiz.md")
            pdf_filename = os.path.join(notes_dir, f"{base_name}_quiz.pdf")

        try:
            with open(md_filename, "w", encoding='utf-8') as f:
                f.write(content)
            if markdown_to_pdf(content, pdf_filename):
                print(f"MARKDOWN:{md_filename}")
                print(f"PDF:{pdf_filename}")
            else:
                print(f"Failed to generate PDF for notes/quiz")

        except Exception as e:
            print(f"Error saving notes/quiz files: {e}")
            md_filename, pdf_filename = None, None

    return md_filename, pdf_filename