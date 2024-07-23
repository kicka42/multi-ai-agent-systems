<p>Hi Andrew,</p>
<p>Thank you for reaching out! I'm thrilled to assist you with setting up a Crew and adding memory to it. Below is a detailed guide to help you through the process:</p>
<h3>Step 0: Installation</h3>
<p>First, ensure you have Python 3.6+ installed on your machine. You can install CrewAI and any necessary packages using the following commands:
<code>bash
pip install crewai
pip install 'crewai[tools]'</code></p>
<h3>Step 1: Assemble Your Agents</h3>
<p>Define your agents with distinct roles, backstories, and enhanced capabilities. Here's an example of how to create agents with memory enabled:</p>
<p>```python
import os
from langchain.llms import OpenAI
from crewai import Agent, Crew, Memory
from crewai_tools import SerperDevTool, BrowserbaseLoadTool, EXASearchTool</p>
<h1>Set your API keys</h1>
<p>os.environ["OPENAI_API_KEY"] = "Your OpenAI Key"
os.environ["SERPER_API_KEY"] = "Your Serper Key"
os.environ["BROWSERBASE_API_KEY"] = "Your BrowserBase Key"
os.environ["BROWSERBASE_PROJECT_ID"] = "Your BrowserBase Project ID"
os.environ["CREWAI_API_KEY"] = "Your CrewAI Key"</p>
<h1>Initialize tools</h1>
<p>search_tool = SerperDevTool()
browser_tool = BrowserbaseLoadTool()
exa_search_tool = EXASearchTool()</p>
<h1>Create a Crew</h1>
<p>my_crew = Crew(name="DeepLearningAI Crew")</p>
<h1>Create a memory object</h1>
<p>crew_memory = Memory()</p>
<h1>Creating a senior researcher agent with memory enabled</h1>
<p>researcher = Agent(
    role='Senior Researcher',
    goal='Uncover groundbreaking technologies in {topic}',
    backstory=("Driven by curiosity, you're at the forefront of innovation, "
               "eager to explore and share knowledge that could change the world."),
    memory=crew_memory,
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
<h1>Creating a writer agent with memory enabled</h1>
<p>writer = Agent(
    role='Writer',
    goal='Narrate compelling tech stories about {topic}',
    backstory=("With a flair for simplifying complex topics, you craft engaging "
               "narratives that captivate and educate, bringing new discoveries to light."),
    verbose=True,
    allow_delegation=False,
    memory=crew_memory,
    tools=[exa_search_tool],
    function_calling_llm=OpenAI(model_name="gpt-3.5-turbo"),  # Separate LLM for function calling
)</p>
<h1>Adding agents to the Crew</h1>
<p>my_crew.add_agent(researcher)
my_crew.add_agent(writer)</p>
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
my_crew.add_agent(manager)
```</p>
<p>In the above examples:
- Both <code>researcher</code> and <code>writer</code> agents have the <code>memory</code> attribute set, enabling them to retain information over their interactions.
- You can customize each agent's attributes such as <code>goal</code>, <code>backstory</code>, <code>tools</code>, etc., to suit your specific needs.</p>
<h3>Additional Prerequisites and Dependencies</h3>
<ul>
<li><strong>API Key</strong>: Ensure you have your crewAI API key ready, which is required for authentication. You can set it up as follows:
  <code>python
  import os
  os.environ["CREWAI_API_KEY"] = "your_api_key_here"</code></li>
<li><strong>Internet Connection</strong>: A stable internet connection is needed for communication with crewAI servers.</li>
<li><strong>Dependent Libraries</strong>: The crewAI SDK may have dependencies on other libraries such as <code>requests</code> and <code>numpy</code>. These should be installed automatically with the SDK, but you can manually install them if needed:
  <code>bash
  pip install requests numpy</code></li>
</ul>
<h3>Additional Agent Attributes and Features</h3>
<ul>
<li><code>allow_code_execution</code>: Enable or disable code execution capabilities for the agent (default is False).</li>
<li><code>max_execution_time</code>: Set a maximum execution time (in seconds) for the agent to complete a task.</li>
<li><code>function_calling_llm</code>: Specify a separate language model for function calling.</li>
</ul>
<h3>Documentation and Support</h3>
<p>For more detailed instructions, you can always refer to the <a href="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/">crewAI documentation</a>.</p>
<p>This should give you a solid foundation to create a Crew with memory capabilities. If you have any more questions or need further assistance, feel free to reach out. We're here to help!</p>
<p>Best regards,
[Your Name]
Senior Support Representative at crewAI</p>