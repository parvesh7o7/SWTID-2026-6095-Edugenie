import os
import json
from google import genai
import functools

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
def get_learning_path(topic: str, level: str = "beginner") -> dict:

    # if no topic is provided - edge case
    if not topic.strip():
        return {"error": "Please provide a topic to generate a learning path."}

    try:
        if not client:
            return {"error": "Gemini API key is missing."}

        # prompt for learning path generation
        prompt = f"""
            You are an expert educational advisor. Create a personalized and structured learning roadmap for the topic: "{topic}".
            The student's current level is: {level}.

            IMPORTANT: Return ONLY valid JSON in this exact format, no other text:
            {{
                "topic": "The exact topic",
                "level": "The level",
                "roadmap": [
                    {{
                        "phase": "Phase 1: Foundations",
                        "description": "Brief description of this phase.",
                        "topics": ["Topic 1", "Topic 2", "Topic 3"],
                        "estimated_time": "e.g., 2 weeks",
                        "resources": ["Resource 1", "Resource 2"]
                    }},
                    {{
                        "phase": "Phase 2: Intermediate Concepts",
                        "description": "Brief description...",
                        "topics": ["Topic A", "Topic B"],
                        "estimated_time": "e.g., 4 weeks",
                        "resources": ["Resource 3", "Resource 4"]
                    }}
                ]
            }}

            Rules:
            - Create 4 to 6 logical sequential phases from start to finish
            - Keep the descriptions concise and motivating
            - List 2 to 4 key topics per phase
            - Provide 1 to 2 realistic resources per phase
            - Return ONLY the JSON, no markdown, no code blocks
        """

        # obtaining the response - temp = 0.6
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.6
            )
        )

        # parse the JSON response
        raw_text = response.text.strip()

        # clean up if wrapped in code blocks
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]  # remove first line
            raw_text = raw_text.rsplit("```", 1)[0]  # remove last ```
            raw_text = raw_text.strip()

        roadmap_data = json.loads(raw_text)
        return roadmap_data

    # error handling
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse roadmap data. Please try again.\n{str(e)}"}
    except Exception as e:
        return {"error": f"Error while generating the learning path:\n{str(e)}"}
