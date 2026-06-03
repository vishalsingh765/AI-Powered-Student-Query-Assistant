import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

cache = {}

def get_response(query):

    if query in cache:
        return cache[query]

    try:
        prompt = f"""
        You are a Student AI Assistant.

        Answer questions related to:
        - Programming
        - AI/ML
        - Career Guidance
        - Interview Preparation

        Question:
        {query}
        """

        response = model.generate_content(prompt)

        answer = response.text

        cache[query] = answer

        return answer

    except Exception as e:
        return f"Error: {str(e)}"