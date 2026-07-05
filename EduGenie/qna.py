import os
import google.generativeai as genai

# extracting the api key from the .env file
api_key = os.getenv("GOOGLE_API_KEY")

# configuring the genai
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Gemini API not configured. GOOGLE_API_KEY environment variable not found.")

import functools

# main function
@functools.lru_cache(maxsize=100)
def get_answer(question: str) -> str:

    # if no question is provided - edge case
    if not question.strip():
        return "Please provide a question to get an answer."

    try:
        # initializing the model - used gemini 2.5 flash model
        model = genai.GenerativeModel("gemini-1.5-pro")

        # prompt for question answering
        prompt = f"""
            You are an expert educational assistant. Answer the following question clearly and accurately. Provide additional educational context, interesting facts, and related concepts to help the student learn more about the topic.

            Question: {question}
        """

        # obtaining the response - temp = 0.5
        response = model.generate_content(prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5
            )
        )

        # returning the generated answer
        return response.text.strip()

    # error handling
    except Exception as e:
        return f"Error while generating the answer:\n{str(e)}"
