from langchain_community.chat_models import ChatOpenAI
from langsmith import traceable

@traceable(name="Summarize Transcript")
def summarize_transcript(transcript_json, language="en", summary_type="regular"):
    # Join segments into a full string
    full_text = " ".join([seg["text"] for seg in transcript_json["segments"]])

    # Truncate to avoid token limits
    full_text = full_text[:8000]

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    # Language instructions
    language_prompt = {
        "en": "Write the summary in English.",
        "ar": "اكتب الملخص باللغة العربية.",
        "fr": "Rédigez le résumé en français.",
        "es": "Escribe el resumen en español."
    }

    # Style prompt for storytelling (detailed summary)
    if summary_type == "storytelling":
        style_prompt = """
You're a storyteller, and your task is to create a detailed and comprehensive narrative from the video transcript.

Please make sure to include **all** key details and events, focusing on:
- Key characters, actions, and sequences
- Relevant facts, events, or data
- The flow of the video, maintaining context
- Any interactions, moments of importance, and conclusions

Write the summary as a rich and detailed story, capturing the essence of the video, with all the important moments. Avoid skipping over any critical points. Ensure the narrative has a smooth flow and engages the reader, while also making sure that every important detail is included.
"""
    elif summary_type == "tutorial":
        style_prompt = """
You're a subject matter expert helping students learn from video content.

Create a tutorial-style summary that includes:
- Key concepts and their definitions
- Steps, processes, or methods discussed
- Important facts or figures
- Actionable insights or learning tips

Organize the summary with clear sections, bullets, or numbered steps so it can be used as a study guide.
"""
    else:
        style_prompt = """
You're an expert video summarizer.

Write a professional summary that:
- Captures the main themes and ideas
- Highlights essential arguments or insights
- Uses formal, clear, and concise language
- Is structured in 3–5 well-formed paragraphs
"""

    # Build final prompt
    prompt = f"""
{style_prompt.strip()}
{language_prompt.get(language, 'Write the summary in English.')}

--- BEGIN TRANSCRIPT ---
{full_text}
--- END TRANSCRIPT ---
"""

    return llm.predict(prompt.strip())
