# LLM Configuration

You can modify which large language model (LLM) you use to suit your own needs.

You may want to:

- Use a different LLM provider for cost or feature reasons.
- Adjust model parameters to control the output.
- Run a local LLM for data privacy or latency reasons.
- Modify the prompt to cater to your specific domain.

## LLM Provider

The LLM you use is configurable in the `SimpleKGPipeline` via the `llm` parameter.

The `neo4j_graphrag` package includes [adapters for several popular LLM providers](https://neo4j.com/docs/neo4j-graphrag-python/current/api.html#openaillm), including OpenAI, Azure OpenAI, and Ollama.

For example, you could run the OpenAI open source model [`openai/gpt-oss-20b`](https://huggingface.co/openai/gpt-oss-20b) locally using a application such as [LM Studio](https://lmstudio.ai/):

```python
llm = OpenAILLM(
    model_name="openai/gpt-oss-20b",
    model_params={
       "temperature": 0
    },
    base_url = "http://localhost:1234/v1"
)
```

> **Model parameters**
>
> Through `model_params` you can change how the model responds by adjusting model parameters such as `temperature` and `response_format`.
>
> The parameters available will depend on the specific LLM you are using.

You can also create your own LLM adapter by inheriting from the [LLMInterface](https://neo4j.com/docs/neo4j-graphrag-python/current/api.html#llminterface) class.

## Prompt Customization

The prompt used for entity extraction and other tasks can also be customized by modifying the `prompt_template` parameter of the `SimpleKGPipeline`.

You can provide an entirely new prompt, but it is often easier to add to the existing.

If you wanted to restrict entity extraction to a specific domain, such as technology companies, you could modify the prompt as follows:

**Custom prompt:**

The `domain_instructions` are added to the start of the default entity extraction prompt to guide the LLM to only extract relevant entities.

The custom prompt can then be used in the `SimpleKGPipeline` by setting the `prompt_template` parameter.

When you're ready you can continue.

## Lesson Summary

In this lesson, you learned about the options for configuring the LLM used in the knowledge graph pipeline, including selecting different LLM providers and customizing prompts.

In the next lesson, you will use what you have learned to create your own knowledge graph from your documents.

---

**Navigation:**
- [← Previous: Questions](06-questions.md)
- [↑ Back to Module 3](README.md)
- [Next: Congratulations →](08-congratulations.md)
