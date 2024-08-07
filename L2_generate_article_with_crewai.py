# Agents to research and write an article

# with CrewAI framework
# We're going to build 3 AI agents: a planner, a writer and an editor to help us write an article.
# The planner will help us to decide what
# to write, the writer will write the article and the editor will help us to edit the article.

# The planner will be a simple agent that
# will take a topic and a list of keywords and will return a list of sentences to write.
# The writer will be a simple agent that will take a list of sentences and will return a list of sentences to write.
# The editor will be a simple agent that will take a list of sentences and will return a list of sentences to edit.

# We're going to use the OpenAI API to create the agents.

import os
import sys
import warnings

import markdown
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from IPython.display import Markdown

warnings.filterwarnings('ignore')

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# agent planner
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    verbose=True
)

# agent writer
writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    verbose=True
)

# agent editor
editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    allow_delegation=False,
    verbose=True
)

# task: plan
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
        "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
        "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
        "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
                    "with an outline, audience analysis, "
                    "SEO keywords, and resources.",
    agent=planner,
)

# task: write
write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
        "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
        "3. Sections/Subtitles are properly named "
        "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
        "engaging introduction, insightful body, "
        "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
        "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
                    "in markdown format, ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

# task: edit
edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)

# crew
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

# ---- #

# run the crew
result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})

# print(result)

# Markdown(result)

# Convert result to markdown format
md_content = markdown.markdown(result)

# Extract the topic
topic = "Artificial Intelligence"  # You can get this dynamically if needed

# Create a filename based on the topic
filename = f"{topic.replace(' ', '_')}_with_crewai.md"

# Save the markdown content to a file
with open(filename, "w") as file:
    file.write(md_content)

print(f"Markdown content saved to {filename}")
