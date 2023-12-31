import demjson3
import logging
import re
from service.factories.ContentFactory import ContentFactory


class GoogleGenerativeAIServiceFactory(ContentFactory):
    """
     Factory class for generating educational content using Google Generative AI service.

     This class provides methods to generate stories, exercises, and multiple-choice questions
     tailored to specific age groups, difficulty levels, scenarios, and characters.

     Attributes:
         google_generative_ai_service: An instance of the Google Generative AI service class
                                       used for content generation.
     """

    def __init__(self, google_generative_ai_service):
        """
              Initializes the GoogleGenerativeAIServiceFactory with a Google Generative AI service instance.

              Args:
                  google_generative_ai_service: An instance of a Google Generative AI service class.
              """
        self.google_generative_ai_service = google_generative_ai_service

    def generate_story(self, scenario, characters, genre):
        """
              Generates a story based on the specified scenario, characters, and genre.

              Args:
                  scenario (str): The setting or situation for the story.
                  characters (str): The characters involved in the story.
                  genre (str): The genre of the story.

              Returns:
                  str: The generated story text.
              """
        # Implementation using GoogleGenerativeAIService
        pass

    def generate_exercise(self, age, difficulty, scenario, character):
        """
               Generates an educational exercise suitable for the specified age group,
               with a given difficulty level, scenario, and character.

               The exercise integrates arithmetic problems in an engaging and immersive narrative.

               Args:
                   age (int): The target age group for the exercise.
                   difficulty (str): The difficulty level of the exercise.
                   scenario (str): The setting or theme of the exercise.
                   character (str): The character involved in the exercise.

               Returns:
                   dict: A dictionary containing the exercise text and its answer.
               """
        prompt = GoogleGenerativeAIServiceFactory._create_expanded_age_prompt(age, difficulty, scenario, character)

        # Log the constructed prompt
        logging.info("Constructed Prompt: %s", prompt)

        exercise_text = self.google_generative_ai_service.generate_text(prompt)

        # Log the response
        logging.info("Generated Exercise Text: %s", exercise_text)

        # Process the response to extract exercise and answer
        return GoogleGenerativeAIServiceFactory._extract_exercise_and_answer_using_regex(exercise_text)

    def generate_multiple_choice_question(self, subject, topic, difficulty):
        """
                Generates a multiple-choice question based on the given subject, topic, and difficulty level.

                Args:
                    subject (str): The subject area of the question.
                    topic (str): The specific topic within the subject area.
                    difficulty (str): The difficulty level of the question.

                Returns:
                    str: The generated multiple-choice question.
                """
        # Implementation using GoogleGenerativeAIService
        pass

    @staticmethod
    def _extract_exercise_and_answer_using_regex(response):
        """
              Extracts the exercise and its answer from the given content using regular expressions.

              Args:
                  response (str): The content containing the exercise and answer.

              Returns:
                  dict: A dictionary with keys 'exercise' and 'answer', containing the extracted texts.
              """
        # Case 1: If response is a JSON string, parse it into a dictionary
        if isinstance(response, str):
            try:
                # Try to directly parse the JSON string
                response_dict = demjson3.decode(response)
            except demjson3.JSONDecodeError:
                # If direct parsing fails, try removing extra characters
                cleaned_response = response.replace("```json", "").replace("```", "").strip()
                try:
                    response_dict = demjson3.decode(cleaned_response)
                except demjson3.JSONDecodeError:
                    return {"error": "JSON decode error"}

        # Case 2: If response is already a dictionary
        elif isinstance(response, dict):
            response_dict = response
        else:
            return {"error": "Invalid response type"}

        # Extract exercise and answer from the dictionary
        return {
            "exercise": response_dict.get("exercise", "Exercise not found"),
            "answer": response_dict.get("answer", "Answer not found")
        }

    @staticmethod
    def _create_expanded_age_prompt(age, difficulty, scenario, character):
        # Descriptors and content focus for different age groups
        """
               Creates a detailed and immersive prompt for generating educational content,
               considering the age, difficulty, scenario, and character.

               Args:
                   age (int): The target age group for the content.
                   difficulty (str): The difficulty level of the content.
                   scenario (str): The setting or theme of the content.
                   character (str): The character involved in the content.

               Returns:
                   str: The constructed prompt for content generation.
               """
        age_focus = {
            "1-2": ("colorful and exploratory", "basic shapes, colors, and counting"),
            "3-4": ("fun and playful", "simple counting and easy puzzles"),
            "5-6": ("exciting and adventurous", "simple arithmetic like 1+1 and basic word problems"),
            "7-8": ("creative and imaginative", "addition, subtraction, and simple word problems"),
            "9-10": ("mysterious and challenging", "multiplication, division, and more complex word problems"),
            "11-12": ("intriguing and thought-provoking", "advanced arithmetic, fractions, and problem-solving"),
            "13-18": ("daring and complex", "algebra, geometry, and critical thinking challenges"),
            "19-30": ("sophisticated and abstract", "higher mathematics, statistics, and real-world applications"),
            "31-60": ("practical and relevant", "everyday math, finance, and logic puzzles"),
            "61-90": ("reflective and engaging", "mental exercises, historical math problems, and logic"),
            "91-120": ("wise and timeless", "age-old puzzles, mathematical riddles, and philosophical questions")
        }

        # Determine age group
        age_group = next((k for k in age_focus if int(age) in range(int(k.split('-')[0]), int(k.split('-')[1]) + 1)),
                         "91-120")

        age_descriptor, focus = age_focus[age_group]

        # Crafting a detailed and immersive prompt
        prompt = f"""
                Create a vivid highly detailed story based on this scenario:
                In a {age_descriptor} world of '{scenario}', '{character}' discovers a series 
                of challenges. These tasks involve {focus} and are perfectly suited for someone aged {age}. 
                With a '{difficulty}' level of complexity. {character} navigates these puzzles by 
                applying your knowledge and skills to explore the depths of '{scenario}'. 
                Generate a detailed exercise based on the story in which the {character} has to solve in order to
                advance in the adventure.
                Your response must contain an exercise question followed by 
                an answer that is only numerical or one word.
                Respond with a json formatted {{\"exercise\": exercise, \"answer\": answer}}
            """

        return prompt
