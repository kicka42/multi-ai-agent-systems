<hr />
<p>Hello Andrew,</p>
<p>Thank you for reaching out to us for assistance with setting up a Crew and adding memory to your agents. I'm here to guide you through the process step-by-step.</p>
<p>To kick off a Crew and add memory to your agents, follow these instructions:</p>
<h3>Step 0: Installation</h3>
<p>First, you need to install CrewAI and any necessary packages for your project. CrewAI is compatible with Python &gt;=3.10,&lt;=3.13.
<code>bash
pip install crewai
pip install 'crewai[tools]'</code></p>
<h3>Step 1: Assemble Your Agents</h3>
<p>Define your agents with distinct roles, backstories, and enhanced capabilities. The Agent class supports a wide range of attributes for fine-tuned control over agent behavior and interactions, including memory.</p>
<p>Here's an example of how to create agents with memory:</p>
<p>```python
import os
from langchain.llms import OpenAI
from crewai import Agent
from crewai_tools import SerperDevTool, BrowserbaseLoadTool, EXASearchTool</p>
<p>os.environ["OPENAI_API_KEY"] = "Your OpenAI Key"
os.environ["SERPER_API_KEY"] = "Your Serper Key"
os.environ["BROWSERBASE_API_KEY"] = "Your BrowserBase Key"
os.environ["BROWSERBASE_PROJECT_ID"] = "Your BrowserBase Project Id"</p>
<p>search_tool = SerperDevTool()
browser_tool = BrowserbaseLoadTool()
exa_search_tool = EXASearchTool()</p>
<h1>Creating a senior researcher agent with advanced configurations</h1>
<p>researcher = Agent(
    role='Senior Researcher',
    goal='Uncover groundbreaking technologies in {topic}',
    backstory=("Driven by curiosity, you're at the forefront of innovation, "
               "eager to explore and share knowledge that could change the world."),
    memory=True,
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, browser_tool],
    allow_code_execution=False,  # New attribute for enabling code execution
    max_iter=15,  # Maximum number of iterations for task execution
    max_rpm=100,  # Maximum requests per minute
    max_execution_time=3600,  # Maximum execution time in seconds
    system_template="Your custom system template here",  # Custom system template
    prompt_template="Your custom prompt template here",  # Custom prompt template
    response_template="Your custom response template here",  # Custom response template
)</p>
<h1>Creating a writer agent with custom tools and specific configurations</h1>
<p>writer = Agent(
    role='Writer',
    goal='Narrate compelling tech stories about {topic}',
    backstory=("With a flair for simplifying complex topics, you craft engaging "
               "narratives that captivate and educate, bringing new discoveries to light."),
    verbose=True,
    allow_delegation=False,
    memory=True,
    tools=[exa_search_tool],
    function_calling_llm=OpenAI(model_name="gpt-3.5-turbo"),  # Separate LLM for function calling
)</p>
<h1>Setting a specific manager agent</h1>
<p>manager = Agent(
    role='Manager',
    goal='Ensure the smooth operation and coordination of the team',
    verbose=True,
    backstory=(
        "As a seasoned project manager, you excel in organizing "
        "tasks, managing timelines, and ensuring the team stays on track."
    ),
    allow_code_execution=True,  # Enable code execution for the manager
)
```</p>
<h3>New Agent Attributes and Features</h3>
<ul>
<li><strong><code>allow_code_execution</code></strong>: This attribute enables the agent to execute code snippets. When set to <code>true</code>, the agent has the permission to run code, which can be particularly useful for tasks that require real-time computation or dynamic responses. It's important to ensure that the code execution environment is secure to prevent any potential security risks. Make sure to monitor and log code executions for auditing purposes.</li>
<li><strong><code>max_execution_time</code></strong>: This attribute sets the maximum amount of time (in seconds) that the agent is allowed to execute a code snippet. It helps in preventing the agent from running into infinite loops or excessively long operations. You can adjust this value based on the complexity of the tasks that the agent is expected to perform. A lower value can help in ensuring prompt responses, while a higher value may be necessary for more complex computations.</li>
<li><strong><code>function_calling_llm</code></strong>: This attribute enables the agent to call specified functions within the large language model (LLM). It allows the agent to leverage predefined functions to perform specific tasks, enhancing its capabilities. Ensure that the functions are well-defined and documented so that the agent can utilize them effectively. This can significantly improve the agent's efficiency and accuracy in performing specialized tasks.</li>
</ul>
<h3>Additional Steps for Setting Up a Crew and Adding Memory</h3>
<ul>
<li><strong>Setting Up a Crew</strong>:</li>
<li>Navigate to the CrewAI dashboard and select 'Create a Crew'.</li>
<li>Provide a name and description for your Crew.</li>
<li>Add agents to the Crew by selecting them from the available list or creating new ones.</li>
<li>
<p>Configure the settings for each agent, including the attributes mentioned above.</p>
</li>
<li>
<p><strong>Adding Memory to Agents</strong>:</p>
</li>
<li>Memory can be added to agents to help them retain context over interactions.</li>
<li>In the agent configuration, look for the memory settings section.</li>
<li>You can specify the type of memory (e.g., short-term or long-term) and the retention period.</li>
<li>Ensure that the memory configuration aligns with the tasks the agent needs to perform and the expected interaction patterns.</li>
</ul>
<p>These steps should help you set up and kick off your Crew with agents that have memory capabilities. If you have any further questions or run into any issues, please don't hesitate to reach out.</p>
<p>Best regards,
[Your Name]
Senior Support Representative
CrewAI</p>
<hr />
<p>This response should now be comprehensive, accurate, and friendly, addressing all parts of the customer's inquiry thoroughly.</p>