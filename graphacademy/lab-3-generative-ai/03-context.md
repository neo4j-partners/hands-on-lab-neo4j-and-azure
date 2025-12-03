# Context

## Improving LLM responses

You can improve the accuracy of responses from LLMs by providing _context_ in your prompts.

The context could include relevant information, data, or details that help the model generate more accurate and relevant responses.

## Avoiding hallucination

Providing context can help minimize hallucinations by anchoring the model's response to the facts and details you supply.

If you ask a model to summarize a company's performance, the model is more likely to produce an accurate summary if you include a relevant stock market report in your prompt.

![A diagram of an LLM being passed a stock market report and being asked to summarise a company's performance.](../images/llm-prompt-document.svg)

## Access to data

LLMs have a fixed knowledge cutoff and cannot access real-time or proprietary data unless it is provided in the prompt.

If you need the model to answer questions about recent events or organization-specific information, you must supply that data as part of your prompt. This ensures that the model's responses are up-to-date and relevant to your particular use case.

You could also provide statistics or data points in the prompt to help the model include useful facts in its response.

![A diagram of an LLM being passed a stock market report and the annual results, being asked to summarize a company's performance. The response includes a specific profit figure from the annual results.](../images/llm-prompt-document-results.svg)

## Supplying context

Supplying context in your prompts helps LLMs generate more **accurate**, **relevant**, and **trustworthy** responses by **reducing hallucinations** and **compensating for the lack of access to data**.

## Check Your Understanding

### Providing Context to LLMs

Which of the following statements are true about providing context to Large Language Models (LLMs)?
(Select all that apply)

**Options:**
- [x] Providing context in a prompt can help reduce hallucinations in LLM responses.
- [x] Supplying up-to-date information in a prompt allows the LLM to generate more relevant answers.
- [x] Including specific instructions or examples in a prompt can improve the accuracy of the model's output.
- [ ] LLMs can access real-time data from the internet without any context provided in the prompt.

<details>
<summary>Hint</summary>
LLMs provide responses based on their training data and the context given in the prompt.
</details>

<details>
<summary>Show Answer</summary>
The following statements are true:

* Providing context in a prompt can help reduce hallucinations in LLM responses.
* Supplying up-to-date information in a prompt allows the LLM to generate more relevant answers.
* Including specific instructions or examples in a prompt can improve the accuracy of the model's output.

LLMs cannot access real-time data.
</details>

## Lesson Summary

In this lesson, you learned about how providing context in your prompts can help reduce hallucinations and improve the accuracy of LLM responses.

In the next module, you will learn about you can use RAG (Retrieval-Augmented Generation) to include additional context in your prompts.

---

**Navigation:**
- [← Previous: LLM Limitations](02-llm-limitations.md)
- [↑ Back to Module 1](README.md)
- [Next: Building the Graph →](04-building-the-graph.md)
