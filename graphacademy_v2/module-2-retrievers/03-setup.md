# Setup your development environment

In this workshop, you will use Neo4j, Python, and LangChain to create retrievers and agents that can interact with Generative AI models.

**Before you start the hands-on exercises**, you need to set up your development environment to run the code examples.

## GitHub Codespaces (Recommended)

The recommended way to work through this workshop is using GitHub Codespaces, which provides a pre-configured development environment.

## Develop on your local machine

You will need:

* [Python](https://python.org).
* [Visual Studio Code](https://code.visualstudio.com/).
* [Jupyter extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter).
* The ability to install packages using `pip`.

You may want to set up a virtual environment using [`venv`](https://docs.python.org/3/library/venv.html) or [`virtualenv`](https://virtualenv.pypa.io/en/latest/) to keep your dependencies separate from other projects.

Clone the [github.com/neo4j-graphacademy/workshop-genai](https://github.com/neo4j-graphacademy/workshop-genai) repository:

```bash
git clone https://github.com/neo4j-graphacademy/workshop-genai
```

Install the required packages using `pip` and download the required data:

```bash
cd workshop-genai
pip install -r requirements.txt
```

You do not need to create a Neo4j database as you will use the provided instance.

The instance uses Neo4j's GenAI functions, you can find out more about how to configure them in the [Neo4j GenAI integration documentation](https://neo4j.com/docs/cypher-manual/current/genai-integrations/).

## Setup the environment

Create a copy of the `.env.example` file and name it `.env`.

```
# Create a copy of this file and name it .env
OPENAI_API_KEY="sk-..."
NEO4J_URI="neo4j://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="password"
NEO4J_DATABASE="neo4j"
```

Update the file to include the Open AI API key (`OPENAI_API_KEY`).

## Test your setup

You can test your setup by running `workshop-genai/test_environment.py` - this will attempt to connect to the Neo4j sandbox and the OpenAI API.

You will see an `OK` message if you have set up your environment correctly. If any tests fail, check the contents of the `.env` file.

## Continue

When you are ready, you can move on to the next lesson.

## Lesson Summary

You have setup your development environment and are ready for hands-on practice.

In the next lesson, you will work hands-on with retrievers using Jupyter notebooks to see how they work in practice.

---

**Navigation:**
- [← Previous: What is a Retriever](02-what-is-a-retriever.md)
- [↑ Back to Module 2](README.md)
- [Next: Working with Retrievers →](04-hands-on-retrievers.md)
