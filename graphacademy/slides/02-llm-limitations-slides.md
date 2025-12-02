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


# LLM Limitations

---

## Caution

While GenAI and LLMs provide a lot of potential, you should also be cautious.

At their core, LLMs are highly complex predictive text machines. LLM's don't know or understand the information they output; they simply predict the next word in a sequence.

The words are based on the patterns and relationships from other text in the training data.

---

## Access to Data

The sources for this training data are often the internet, books, and other publicly available text. The data could be of questionable quality or even incorrect.

Training happens at a point in time, the data is static, and may not reflect the current state of the world or include any private information.

---

## Access to Data

When prompted to provide a response, relating to new or data not in the training set, the LLM may provide a response that is not accurate.

![A diagram of an LLM returning out of data information.](images/llm-missing-data.svg)

---

## Accuracy

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">

<div>

LLMs are designed to create human-like text and are often fine-tuned to be as helpful as possible, even if that means occasionally generating misleading or baseless content, a phenomenon known as **hallucination**.

For example, when asked to _"Describe the moon."_ an LLM may respond with _"The moon is made of cheese."_. While this is a common saying, it is not true.

</div>

<div>

![A diagram of a confused LLM with a question mark thinking about the moon and cheese.](images/confused-llm.svg)

</div>

</div>

While LLMs can represent the essence of words and phrases, they don't possess a genuine understanding or ethical judgment of the content.

---

## Temperature

LLMs have a _temperature_, corresponding to the amount of randomness the underlying model should use when generating the text.

The higher the temperature value, the more random the generated result will become, and the more likely the response will contain false statements.

A higher temperature may be appropriate when configuring an LLM to respond with more diverse and creative outputs, a lower temperature required when responses should be consistent and precise.

How temperature affects the output is dependent on the model due to differences in design and training data.

---

## Temperature

**Consider the correct temperature**

In June 2023, [A US judged sanctioned two US lawyers for submitting an LLM-generated legal brief](https://www.reuters.com/legal/new-york-lawyers-sanctioned-using-fake-chatgpt-cases-legal-brief-2023-06-22/) that contained six fictitious case citations.

A quick fix _may_ be to reduce the temperature. But more likely, the LLM is hallucinating because it hasn't got the information required.

---

## Transparency

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">

<div>

GenAI Models are often considered "black boxes" due to the difficulty deciphering their decision-making processes.

The LLM is also unable to provide the sources for its output or explain its reasoning.

</div>

<div>

![An LLM as a black box, responding to the question 'How did you determine that answer?' with 'I don't know.'](images/llm-blackbox.svg)

</div>

</div>

---

## Lesson Summary

In this lesson, you learned about the limitations of GenAI models, including hallucination, and access to data, and how these factors can lead to outputs that might be biased, devoid of context, or lack logical coherence.

In the next lesson, you will learn about how to provide context to GenAI models to improve the accuracy of their responses.
