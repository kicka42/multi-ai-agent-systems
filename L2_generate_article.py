import os
import sys
import warnings
import markdown
from dotenv import load_dotenv
from openai import OpenAI

warnings.filterwarnings('ignore')

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_content_plan(topic):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a content planner."},
            {"role": "user", "content": (
                f"Create a detailed content plan for a blog article on the topic '{topic}'. "
                f"The plan should prioritize the latest trends, key players, and noteworthy news. "
                f"Identify the target audience, considering their interests and pain points. "
                f"Develop a detailed content outline including an introduction, key points, and a call to action. "
                f"Include SEO keywords and relevant data or sources."
            )}
        ]
    )
    return response.choices[0].message.content.strip()

def write_article(content_plan):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a content writer."},
            {"role": "user", "content": (
                f"Based on the following content plan, craft a compelling blog post. "
                f"The blog post should incorporate SEO keywords naturally, have properly named sections/subtitles, "
                f"and be structured with an engaging introduction, insightful body, and a summarizing conclusion. "
                f"Content Plan: {content_plan}"
            )}
        ]
    )
    return response.choices[0].message.content.strip()

def edit_article(article):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an editor."},
            {"role": "user", "content": (
                f"Proofread and edit the following blog post for grammatical errors and alignment with the brand's voice. "
                f"Blog Post: {article}"
            )}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    topic = "Artificial Intelligence"

    # Generate content plan
    content_plan = generate_content_plan(topic)
    print("Content Plan:\n", content_plan)

    # Write article based on content plan
    article = write_article(content_plan)
    print("Article:\n", article)

    # Edit the article
    edited_article = edit_article(article)
    print("Edited Article:\n", edited_article)

    # Convert the result to markdown format
    md_content = markdown.markdown(edited_article)

    # Create a filename based on the topic
    filename = f"{topic.replace(' ', '_').lower()}.md"

    # Save the markdown content to a file
    with open(filename, "w") as file:
        file.write(md_content)

    print(f"Markdown content saved to {filename}")

if __name__ == "__main__":
    main()