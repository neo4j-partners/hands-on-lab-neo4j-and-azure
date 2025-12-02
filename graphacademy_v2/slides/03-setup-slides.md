---
marp: true
theme: default
paginate: true
---

# Setup your development environment

In this workshop, you will use Neo4j, Python, and LangChain to create retrievers and agents that can interact with Generative AI models.

**Before you start the hands-on exercises**, you need to set up your development environment to run the code examples.

---

## Setup the environment

Create a copy of the `.env.example` file and name it `.env`.

```
# Create a copy of this file and name it .env
OPENAI_API_KEY="sk-..."
NEO4J_URI="neo4j://..."
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="..."
NEO4J_DATABASE="neo4j"
```

Update the file to include the Open AI API key (`OPENAI_API_KEY`).

---

## Test your setup

You can test your setup by running `workshop-genai/test_environment.py` - this will attempt to connect to the Neo4j sandbox and the OpenAI API.

You will see an `OK` message if you have set up your environment correctly. If any tests fail, check the contents of the `.env` file.

---

## Continue

When you are ready, you can move on to the next lesson.

---

## Lesson Summary

You have setup your development environment and are ready for hands-on practice.

In the next lesson, you will work hands-on with retrievers using Jupyter notebooks to see how they work in practice.
