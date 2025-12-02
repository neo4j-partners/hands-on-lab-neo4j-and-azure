---
marp: true
theme: default
paginate: true
---

<style>
section {
  --marp-auto-scaling-code: false;
}

li {
  opacity: 1 !important;
  animation: none !important;
  visibility: visible !important;
}

/* Disable all fragment animations */
.marp-fragment {
  opacity: 1 !important;
  visibility: visible !important;
}

ul > li,
ol > li {
  opacity: 1 !important;
}
</style>


# Context

---

## Improving LLM responses

You can improve the accuracy of responses from LLMs by providing _context_ in your prompts.

The context could include relevant information, data, or details that help the model generate more accurate and relevant responses.

---

## Avoiding hallucination

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">

<div>

Providing context can help minimize hallucinations by anchoring the model's response to the facts and details you supply.

If you ask a model to summarize a company's performance, the model is more likely to produce an accurate summary if you include a relevant stock market report in your prompt.

</div>

<div>

![A diagram of an LLM being passed a stock market report and being asked to summarise a company's performance.](images/llm-prompt-document.svg)

</div>

</div>

---

## Access to data

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">

<div>

LLMs have a fixed knowledge cutoff and cannot access real-time or proprietary data unless it is provided in the prompt.

If you need the model to answer questions about recent events or organization-specific information, you must supply that data as part of your prompt. This ensures that the model's responses are up-to-date and relevant to your particular use case.

You could also provide statistics or data points in the prompt to help the model include useful facts in its response.

</div>

<div>

![A diagram of an LLM being passed a stock market report and the annual results, being asked to summarize a company's performance. The response includes a specific profit figure from the annual results.](images/llm-prompt-document-results.svg)

</div>

</div>

---

## Supplying context

Supplying context in your prompts helps LLMs generate more **accurate**, **relevant**, and **trustworthy** responses by **reducing hallucinations** and **compensating for the lack of access to data**.

---

## Lesson Summary

In this lesson, you learned about how providing context in your prompts can help reduce hallucinations and improve the accuracy of LLM responses.

In the next module, you will learn about you can use RAG (Retrieval-Augmented Generation) to include additional context in your prompts.
