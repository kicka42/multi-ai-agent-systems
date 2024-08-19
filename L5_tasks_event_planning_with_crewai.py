# TEN PLIK CIAGLE MI NIE DZIALA
# Automate Event Planning 1

import os
import sys
import json
import atexit


from dotenv import load_dotenv
from crewai import Agent, Crew, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel
from pprint import pprint
from IPython.display import Markdown

import warnings
warnings.filterwarnings('ignore')

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    print("Warning: SERPER_API_KEY not found in environment variables.")


# Initialize the Crew AI tools
# SerperDevTool - allows search internet and google and return results back
search_tool = SerperDevTool()
# ScrapeWebsiteTool - allows agents to go into those websites that it finds
# and getting their contents, so that it can use that during the execution.
scrape_tool = ScrapeWebsiteTool()

# Create the agents
# Agent 1: Venue Coordinator
venue_coordinator = Agent(
    role="Venue Coordinator",
    goal="Identify and book an appropriate venue "
         "based on event requirements",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "With a keen sense of space and "
        "understanding of event logistics, "
        "you excel at finding and securing "
        "the perfect venue that fits the event's theme, "
        "size, and budget constraints."
    )
)

# Agent 2: Logistics Manager
logistics_manager = Agent(
    role='Logistics Manager',
    goal=(
        "Manage all logistics for the event "
        "including catering and equipment"
    ),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Organized and detail-oriented, "
        "you ensure that every logistical aspect of the event "
        "from catering to equipment setup "
        "is flawlessly executed to create a seamless experience."
    )
)

# Agent 3: Marketing and Communications Agent
marketing_communications_agent = Agent(
    role="Marketing and Communications Agent",
    goal="Effectively market the event and "
         "communicate with participants",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Creative and communicative, "
        "you craft compelling messages and "
        "engage with potential attendees "
        "to maximize event exposure and participation."
    )
)

# Creating Venue Pydantic Object that is going to hold our venue details.
# Agents will populate this object with
# information about different venues by creating different instances of it.

# Define a Pydantic model for venue details
# (demonstrating Output as Pydantic)


class VenueDetails(BaseModel):
    name: str
    address: str
    capacity: int
    booking_status: str


# Create First Task
# By using output_json, you can specify the structure of the output you want.
# By using output_file, you can get your output in a file.
# By setting human_input=True, the task will ask for human feedback
# (whether you like the results or not) before finalising it.
venue_task = Task(
    description="Find a venue in {event_city} "
                "that meets criteria for {event_topic}.",
    expected_output="All the details of a specifically chosen"
                    "venue you found to accommodate the event.",
    human_input=True,
    output_json=VenueDetails,
    output_file="L5_venue_details.json",
    # Outputs the venue details as a JSON file
    agent=venue_coordinator
)

# Create Second Task
# By setting async_execution=True,
# it means the task can run in parallel with the tasks which come after it.
logistics_task = Task(
    description="Coordinate catering and "
                "equipment for an event "
                "with {expected_participants} participants "
                "on {tentative_date}.",
    expected_output="Confirmation of all logistics arrangements "
                    "including catering and equipment setup.",
    human_input=True,
    async_execution=True,
    agent=logistics_manager
)

# Create Third Task
marketing_task = Task(
    description="Promote the {event_topic} "
                "aiming to engage at least"
                "{expected_participants} potential attendees.",
    expected_output="Report on marketing activities "
                    "and attendee engagement formatted as markdown.",
    async_execution=True,
    output_file="L5_marketing_report.md",  # Outputs the report as a text file
    agent=marketing_communications_agent
)

# Create the Crew
# Since you set async_execution=True for logistics
# task and marketing_task tasks, now the order for them does not matter in the tasks list.
# Define the crew with agents and tasks
event_management_crew = Crew(
    agents=[venue_coordinator,
            logistics_manager,
            marketing_communications_agent],

    tasks=[venue_task,
           logistics_task,
           marketing_task],

    verbose=True
)

# Run the Crew
# Set the inputs for the execution of the crew.
event_details = {
    'event_topic': "Tech Innovation Conference",
    'event_description': "A gathering of tech innovators "
                         "and industry leaders "
                         "to explore future technologies.",
    'event_city': "San Francisco",
    'tentative_date': "2024-09-15",
    'expected_participants': 500,
    'budget': 20000,
    'venue_type': "Conference Hall"
}

# If human_input is set to True for some tasks,
# the execution will ask for input before it finishes running.
# When it asks for feedback, use mouse pointer
# to first click in the text box before typing anything.

result = event_management_crew.kickoff(inputs=event_details)

def shutdown_hook():
    # Ensure all tasks and tools are cleaned up
    if event_management_crew:
        event_management_crew.shutdown_gracefully()  # Hypothetical method

atexit.register(shutdown_hook)

with open('L5_venue_details.json') as f:
    data = json.load(f)

pprint(data)

Markdown("L5_marketing_report.md")

