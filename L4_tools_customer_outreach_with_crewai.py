import sys
import warnings

import markdown

warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew

import os
# from utils import get_openai_api_key, pretty_print_result
# from utils import get_serper_api_key
from dotenv import load_dotenv

from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from crewai_tools import BaseTool

from IPython.display import Markdown

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    print("Warning: SERPER_API_KEY not found in environment variables.")

# Sales representative agent
sales_rep_agent = Agent(
    role="Sales Representative",
    goal="Identify high-value leads that match "
         "our ideal customer profile",
    backstory=(
        "As a part of the dynamic sales team at CrewAI, "
        "your mission is to scour "
        "the digital landscape for potential leads. "
        "Armed with cutting-edge tools "
        "and a strategic mindset, you analyze data, "
        "trends, and interactions to "
        "unearth opportunities that others might overlook. "
        "Your work is crucial in paving the way "
        "for meaningful engagements and driving the company's growth."
    ),
    allow_delegation=False,
    verbose=True
)

# Lead sales representative agent
lead_sales_rep_agent = Agent(
    role="Lead Sales Representative",
    goal="Nurture leads with personalized, compelling communications",
    backstory=(
        "Within the vibrant ecosystem of CrewAI's sales department, "
        "you stand out as the bridge between potential clients "
        "and the solutions they need."
        "By creating engaging, personalized messages, "
        "you not only inform leads about our offerings "
        "but also make them feel seen and heard."
        "Your role is pivotal in converting interest "
        "into action, guiding leads through the journey "
        "from curiosity to commitment."
    ),
    allow_delegation=False,
    verbose=True
)

# Create tools
# DirectoryReadTool - allows your agent to read any directory that it wants,
# here read only local instructions directory folder. So in this directory, there are a series of instructions
# as markdown files on how to handle companies from different sizes (big, medium and small companies).
# Here in instructions folder we have markdown files on how to hande:
# Small Businesses, Enterprise Solutions and Tech Startups
directory_read_tool = DirectoryReadTool(directory='./instructions')
# FileReadTool - allows your agent to read any file that it wants
file_read_tool = FileReadTool()
# SerperDevTool - allows search internet and google and return results back
search_tool = SerperDevTool()

# Create custom tool
class SentimentAnalysisTool(BaseTool):
    name: str ="Sentiment Analysis Tool"
    description: str = ("Analyzes the sentiment of text "
                        "to ensure positive and engaging communication.")

    def _run(self, text: str) -> str:
        # Your custom code tool goes here
        return "positive"

sentiment_analysis_tool = SentimentAnalysisTool()

# Create tasks
lead_profiling_task = Task(
    description=(
        "Conduct an in-depth analysis of {lead_name}, "
        "a company in the {industry} sector "
        "that recently showed interest in our solutions. "
        "Utilize all available data sources "
        "to compile a detailed profile, "
        "focusing on key decision-makers, recent business "
        "developments, and potential needs "
        "that align with our offerings. "
        "This task is crucial for tailoring "
        "our engagement strategy effectively.\n"
        "Don't make assumptions and "
        "only use information you absolutely sure about."
    ),
    expected_output=(
        "A comprehensive report on {lead_name}, "
        "including company background, "
        "key personnel, recent milestones, and identified needs. "
        "Highlight potential areas where "
        "our solutions can provide value, "
        "and suggest personalized engagement strategies."
    ),
    tools=[directory_read_tool, file_read_tool, search_tool],
    agent=sales_rep_agent,
)

personalized_outreach_task = Task(
    description=(
        "Using the insights gathered from "
        "the lead profiling report on {lead_name}, "
        "craft a personalized outreach campaign "
        "aimed at {key_decision_maker}, "
        "the {position} of {lead_name}. "
        "The campaign should address their recent {milestone} "
        "and how our solutions can support their goals. "
        "Your communication must resonate "
        "with {lead_name}'s company culture and values, "
        "demonstrating a deep understanding of "
        "their business and needs.\n"
        "Don't make assumptions and only "
        "use information you absolutely sure about."
    ),
    expected_output=(
        "A series of personalized email drafts "
        "tailored to {lead_name}, "
        "specifically targeting {key_decision_maker}."
        "Each draft should include "
        "a compelling narrative that connects our solutions "
        "with their recent achievements and future goals. "
        "Ensure the tone is engaging, professional, "
        "and aligned with {lead_name}'s corporate identity."
    ),
    tools=[sentiment_analysis_tool, search_tool],
    agent=lead_sales_rep_agent,
)

# Create the Crew
crew = Crew(
    agents=[sales_rep_agent,
            lead_sales_rep_agent],

    tasks=[lead_profiling_task,
           personalized_outreach_task],

    verbose=2,
    memory=True
)

# Run the Crew
inputs = {
    "lead_name": "DeepLearningAI",
    "industry": "Online Learning Platform",
    "key_decision_maker": "Andrew Ng",
    "position": "CEO",
    "milestone": "product launch"
}

result = crew.kickoff(inputs=inputs)

# Convert result to markdown format
md_content = markdown.markdown(result)

# Create a filename based on the topic
filename = f"L4_tools_customer_outreach_with_crewai.md"

# Save the markdown content to a file
with open(filename, "w") as file:
    file.write(md_content)

print(f"Markdown content saved to {filename}")

Markdown(result)