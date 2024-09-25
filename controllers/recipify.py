import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv
import typing_extensions as typing
import json

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "../.env")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class Recipe(typing.TypedDict):
    name: str
    description: str
    diet: str
    servings: int
    calories: int  
    allergies: list[str]
    ingredients: list[str]
    preparation_steps: list[str]

def recipify(text: str, tries= 0, max_retries = 3) -> str:
    
    tries = 0
    
    try:
        prompt = f"""
        Based on the following recipe essay, create a structured recipe with the following information:
        1. A brief description of the dish
        2. The diet type (e.g., vegetarian, vegan, omnivore)
        3. Number of servings (integer)
        4. Estimated calories per serving (integer)
        5. A link (use a placeholder like 'https://example.com/pancake-recipe')
        6. A list of potential allergies
        7. A list of ingredients with quantities
        8. Step-by-step instructions (Ignore useless information that isn't part of the recipe)

        Recipe essay:
        {text}

        Please format your response as a JSON object with the following keys:
        "name", "description", "diet", "servings", "calories", "allergies", "ingredients", "preparation_steps".
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        content = response.text
        content = content.replace("```json", "").replace("```", "").strip()
        
        parsed_result = json.loads(content)

        return Recipe(
            name=parsed_result["name"],
            description=parsed_result["description"],
            diet=parsed_result["diet"],
            servings=parsed_result["servings"],
            calories=parsed_result["calories"],
            allergies=parsed_result["allergies"],
            ingredients=parsed_result["ingredients"],
            preparation_steps=parsed_result["preparation_steps"],
        )
    except Exception as e:
        if tries < max_retries:
            print(f"Attempt {tries + 1} failed. Retrying...")
            return recipify(text, tries=tries + 1, max_retries=max_retries)
        raise e