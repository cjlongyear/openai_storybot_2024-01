import argparse
from openai import OpenAI
from dotenv import load_dotenv
import os


class StoryBot:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)

    def generate_story(self, user_prompt: str, style: str = None) -> str:
        prompt = f"{style}: {user_prompt}" if style else user_prompt

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Specify the GPT-4 model
                messages=[
                    {"role": "system", "content": "Generate a creative story."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"


def write_story_to_file(story, filename):
    with open(filename, 'w') as file:
        file.write(story)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate stories with StoryBot")
    parser.add_argument("prompt", type=str, help="The story prompt")
    parser.add_argument("-s", "--style", type=str, choices=['sarcastic', 'old man', 'pirate'], help="The storytelling style")
    parser.add_argument("-o", "--output", type=str, help="Output file to save the story")

    args = parser.parse_args()

    story_bot = StoryBot()
    story = story_bot.generate_story(args.prompt, args.style)

    if args.output:
        write_story_to_file(story, args.output)
        print(f"Story saved to {args.output}")
    else:
        print(story)
