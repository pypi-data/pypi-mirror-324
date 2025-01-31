# learning_toolbox/content_generator.py

import google.generativeai as genai
import time
import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id.group(1) if video_id else None

def get_transcript(video_id):
    """Retrieves the transcript from a YouTube video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error getting transcript: {str(e)}"

def generate_content(topic, content_type="notes", api_key=None):
    """Generates content using the Gemini API based on the topic and content type."""
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    prompts = {
        "notes": f"""Create detailed study notes about {topic} in markdown format.
                    Include:
                    # {topic}
                    ## Overview
                    ## Key concepts
                    ## Examples
                    ## Summary
                    ## Five Practice Questions """,

        "quiz": f"""Generate 10 MCQs about {topic} in markdown format. And Options should be provided vertically (one option in one line) and include the anser key at last.""",

        "youtube_summary": lambda transcript: f""" Length of whole content should be at leat 50 percent of total transcrip lenth.

                  Create a detailed summary of this video transcript in markdown format:
                    # Detailed Video Summary
                    ## Key Points
                    ## Main Ideas
                    ## Important Details
                    ## Conclusion

                    Transcript: {transcript}""",

        "mindmap": f"""Create a hierarchical mind map for: {topic}
                Format exactly as:
                {topic}
                - Key Concept 1
                  - Subtopic 1.1
                    - Detail 1.1.1
                  - Subtopic 1.2
                - Key Concept 2
                  - Subtopic 2.1
                  - Subtopic 2.2
                Include 3-4 main concepts with subtopics."""
    }

    try:
        if api_key:
            genai.configure(api_key=api_key)  # Allow API key to be passed as argument
        else:
            # Assuming API_KEY is set as environment variable or in other config
            genai.configure(api_key=api_key) # Or you can raise an error if API key is absolutely required here.
        model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')  # Use more stable model

        for attempt in range(MAX_RETRIES):
            try:
                if content_type == "youtube_summary":
                    video_id = get_video_id(topic)
                    if not video_id:
                        return "Error: Invalid YouTube URL"

                    transcript = get_transcript(video_id)
                    if transcript.startswith("Error"):
                        return transcript
                    response = model.generate_content(prompts[content_type](transcript))

                elif content_type == "mindmap":
                    response = model.generate_content(prompts["mindmap"])

                else:
                    response = model.generate_content(prompts[content_type])

                # Validate response
                if not response or not response.text:
                    raise Exception("Empty response from API")

                return response.text.encode('ascii', 'ignore').decode()

            except Exception as e:
                error_msg = str(e).lower()

                # Handle specific errors
                if "429" in error_msg or "quota" in error_msg:
                    return "Error: API quota exceeded. Please try again later."
                elif "400" in error_msg:
                    return "Error: Invalid request. Please check your input."
                elif "500" in error_msg:
                    return "Error: Server error. Please try again later."

                # Retry on other errors
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue

                return f"Error: Failed after {MAX_RETRIES} attempts. {str(e)}"

    except Exception as e:
        return f"Error: Configuration failed - {str(e)}"