# Multi-agent system for customer support automation

# We create here multi-agent system for customer support automation
# which help supporting customers that might have inquiries about the product

# The six key elements which help make Agents perform even better:
# Role Playing, Focus, Tools, Cooperation, Guardrails, Memory

import os
import sys
import warnings

import markdown
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from IPython.display import Markdown
from crewai_tools import SerperDevTool, \
    ScrapeWebsiteTool, \
    WebsiteSearchTool

warnings.filterwarnings('ignore')

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# Support agent
support_agent = Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful "
         "support representative in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and "
        " are now working on providing "
        "support to {customer}, a super important customer "
        " for your company."
        "You need to make sure that you provide the best support!"
        "Make sure to provide full complete answers, "
        " and make no assumptions."
    ),
    allow_delegation=False,
    verbose=True
)

# Support QA agent
# By not setting allow_delegation=False,
# it defaults to True, allowing the agent to delegate tasks to a more suitable agent.
support_quality_assurance_agent = Agent(
    role="Support Quality Assurance Specialist",
    goal="Get recognition for providing the "
         "best support quality assurance in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and "
        "are now working with your team "
        "on a request from {customer} ensuring that "
        "the support representative is "
        "providing the best support possible.\n"
        "You need to make sure that the support representative "
        "is providing full"
        "complete answers, and make no assumptions."
    ),
    verbose=True
)

# Tools
# SerperDevTool - allows search google
# ScrapeWebsiteTool - simple scraper, allows access url and extract content
# WebsiteSearchTool - semantic search on a website

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
)

# Assign tools
# Agents can be given tools either at the agent level for all tasks or at the task level for specific tasks,
# with task tools overriding agent tools.

# Tasks
# Pass the Tool on the Task Level
inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
        "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
        "Make sure to use everything you know "
        "to provide the best support possible."
        "You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
    ),
    expected_output=(
        "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
        "leaving no questions unanswered, and maintain a helpful and friendly "
        "tone throughout."
    ),
    tools=[docs_scrape_tool],
    agent=support_agent,
)

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
        "high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
        "thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
        "ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
        "relevant feedback and improvements.\n"
        "Don't be too formal, we are a chill and cool company "
        "but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent,
)

# Create the Crew
crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    verbose=2,
    memory=True
)

# Run the Crew
inputs = {
    "customer": "DeepLearningAI",
    "person": "Andrew Ng",
    "inquiry": "I need help with setting up a Crew "
               "and kicking it off, specifically "
               "how can I add memory to my crew? "
               "Can you provide guidance?"
}
result = crew.kickoff(inputs=inputs)

# Convert result to markdown format
md_content = markdown.markdown(result)

# Create a filename based on the topic
filename = f"L3_customer_support_response_with_crewai.md"

# Save the markdown content to a file
with open(filename, "w") as file:
    file.write(md_content)

print(f"Markdown content saved to {filename}")

Markdown(result)
