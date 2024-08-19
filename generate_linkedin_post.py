import os
import sys
import requests
import warnings
from bs4 import BeautifulSoup

from crewai import Agent, Task, Crew
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

if not OPENAI_API_KEY:
    print("OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

if not PERPLEXITY_API_KEY:
    print("PERPLEXITY_API_KEY not found in environment variables.")
    sys.exit(1)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# Function to fetch top recent news from Perplexity Discover
def fetch_top_news():
    url = "https://www.perplexity.ai/discover"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the first news item with the class 'col-span-3'
        first_article = soup.find('div', class_='col-span-3')
        news_title = first_article.find('a').get_text(strip=True)
        news_url = "https://www.perplexity.ai" + first_article.find('a')['href']

        return {"title": news_title, "url": news_url}
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        sys.exit(1)
    except Exception as err:
        print(f"Other error occurred: {err}")
        sys.exit(1)

# agent news_reader
news_reader = Agent(
    role="News Reader",
    goal="Read the latest news and provide a brief summary.",
    backstory="You're an AI agent tasked with reading the latest news articles and summarizing their content.",
    allow_delegation=False,
    verbose=True
)

# agent opinion_writer
opinion_writer = Agent(
    role="Opinion Writer",
    goal="Write a short, insightful opinion on the latest news for a LinkedIn post.",
    backstory="You're an AI agent tasked with writing a short opinion piece based on the latest news articles. This opinion piece will be posted on LinkedIn.",
    allow_delegation=False,
    verbose=True
)

# task: read news
read_news = Task(
    description=("Read the latest news and provide a brief summary."),
    expected_output="A brief summary of the latest news.",
    agent=news_reader,
)

# task: write opinion
write_opinion = Task(
    description=("Write a short, insightful opinion on the latest news for a LinkedIn post."),
    expected_output="A LinkedIn post containing a brief opinion on the latest news.",
    agent=opinion_writer,
)

# crew
crew = Crew(
    agents=[news_reader, opinion_writer],
    tasks=[read_news, write_opinion],
    verbose=2
)

# Fetch top news
top_news = fetch_top_news()

# Prepare inputs for the tasks
inputs = {
    "news_title": top_news['title'],
    "news_url": top_news['url']
}

# Run the crew
result = crew.kickoff(inputs=inputs)

# Print the LinkedIn post content
linkedin_post = f"{result}\n\nRead more here: {top_news['url']}"
print(linkedin_post)
