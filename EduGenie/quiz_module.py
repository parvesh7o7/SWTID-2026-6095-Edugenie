import os
import json
import functools
from google import genai

# extracting the api key from the .env file
api_key = os.getenv("GOOGLE_API_KEY")

# configuring the genai client
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None
    print("Gemini API not configured. GOOGLE_API_KEY environment variable not found.")

# main function
@functools.lru_cache(maxsize=100)
def generate_quiz(topic: str, num_questions: int = 5, difficulty: str = "Easy") -> dict:

    # if no topic is provided - edge case
    if not topic.strip():
        return {"error": "Please provide a topic to generate a quiz."}

    try:
        if not client:
            return {"error": "Gemini API key is missing."}

        # prompt for structured quiz generation
        prompt = f"""
            You are an expert educational quiz generator. Create exactly {num_questions} multiple-choice questions on the topic: "{topic}".
            Difficulty level: {difficulty}.

            IMPORTANT: Return ONLY valid JSON in this exact format, no other text:
            {{
                "questions": [
                    {{
                        "question": "The question text here?",
                        "options": {{
                            "A": "First option",
                            "B": "Second option",
                            "C": "Third option",
                            "D": "Fourth option"
                        }},
                        "correct": "A",
                        "explanation": "Brief explanation of why this is correct."
                    }}
                ]
            }}

            Rules:
            - Generate exactly {num_questions} questions
            - Each question must have exactly 4 options: A, B, C, D
            - "correct" must be one of: "A", "B", "C", "D"
            - Adjust complexity based on difficulty: {difficulty}
            - Return ONLY the JSON, no markdown, no code blocks
        """

        # obtaining the response - temp = 0.7
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.7
            )
        )

        # parse the JSON response
        raw_text = response.text.strip()

        # clean up if wrapped in code blocks
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]  # remove first line
            raw_text = raw_text.rsplit("```", 1)[0]  # remove last ```
            raw_text = raw_text.strip()

        quiz_data = json.loads(raw_text)
        return quiz_data

    # error handling
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse quiz data. Please try again.\n{str(e)}"}
    except Exception as e:
        return {"error": f"Error while generating the quiz:\n{str(e)}"}
