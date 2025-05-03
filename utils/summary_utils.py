from langchain_community.chat_models import ChatOpenAI

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

    # Style prompt
    if summary_type == "tutorial":
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
