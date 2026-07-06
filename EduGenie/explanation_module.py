import os
import functools

# Try to load LaMini-Flan-T5 locally; fall back to Gemini API on cloud (Render free tier has limited RAM)
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    # AutoTokenizer for tokenization process. AutoModelForSeq2SeqLM for loading the main architectural model of lamini
    LAMINI_AVAILABLE = True
except ImportError:
    LAMINI_AVAILABLE = False

tokenizer = None
model = None
# initialize the global variable with none

# Cache directory for Render persistent disk (avoids re-downloading on every deploy)
CACHE_DIR = os.environ.get("TRANSFORMERS_CACHE", None)


def _explain_with_lamini(topic: str) -> str:
    """Explain using the local LaMini-Flan-T5-248M model."""
    global tokenizer, model
    # For using the global variables (not creating new ones)

    if model is None:
        # for the startup only, when the application loads for the first time
        print("Lamini model is loading...")
        tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-248M", cache_dir=CACHE_DIR)
        model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-248M", cache_dir=CACHE_DIR)

    prompt = f"Explain the following topic in very simple terms for a student: {topic}"
    # Prompt creation

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    # Converts the prompt into tokens

    outputs = model.generate(**inputs, max_length=256, do_sample=True, temperature=0.7)
    # generate the output

    text_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # number to text generation

    return text_output.strip()


def _explain_with_gemini(topic: str) -> str:
    """Fallback: Explain using Google Gemini API when LaMini can't be loaded (e.g., on Render free tier)."""
    from google import genai
    import os

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Gemini API key is missing."

    client = genai.Client(api_key=api_key)

    prompt = f"""You are a friendly teacher. Explain the following topic in very simple, 
    easy-to-understand terms for a student. Use analogies and examples where helpful.
    
    Topic: {topic}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=0.7
        )
    )
    return response.text.strip()


@functools.lru_cache(maxsize=100)
def get_explanation(topic: str) -> str:
    """Get an explanation - uses LaMini locally, Gemini on cloud."""

    if not topic.strip():
        return "Please provide a topic to get an explanation."

    try:
        if LAMINI_AVAILABLE:
            return _explain_with_lamini(topic)
        else:
            print("LaMini not available, using Gemini API fallback.")
            return _explain_with_gemini(topic)
    except Exception as e:
        # If LaMini fails (e.g., out of memory), try Gemini as fallback
        try:
            print(f"LaMini failed ({e}), falling back to Gemini API.")
            return _explain_with_gemini(topic)
        except Exception as gemini_error:
            return f"Error while generating the explanation:\n{str(gemini_error)}"
