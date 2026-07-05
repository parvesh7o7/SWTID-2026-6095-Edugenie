import os
import google.generativeai as genai

# extracting the api key from the .env file
api_key = os.getenv("GOOGLE_API_KEY")

# configuring the genai
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Gemini Api not configured. Environment Variable not found")

import functools

# main function
@functools.lru_cache(maxsize=100)
def get_summary(text: str) -> str:

    # if no text is provided - edge case
    if not text.strip():
        return "You need to provide a string to get the summary"


    try:
        # initializing the model - used gemini 2.5 flash model
        model = genai.GenerativeModel("gemini-1.5-pro") 

        # prompt for summary generation
        prompt = f"""
            You are an expert educational assistant. Summarize the following long paragraphs into a concise, easy-to-understand version, making it ideal for quick revision. Ensure the core information is retained while eliminating redundancy. Format the output using clear, clean bullet points where appropriate.

            Text to summarize:{text}
        """

        # obtaining the response - temp = 0.5
        response = model.generate_content(prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5
            )
        )

        # returning the generated summary
        return response.text.strip()

    # error handling
    except Exception as e:
        return f"Error while generating the summary:\n{str(e)}"
