# LLM Guardrails Summer Project

**Goal:** Learn more about LangChain and red-teaming for now!

### Quick-start (CPU)
```bash
git clone https://github.com/<yourname>/llm-guardrails-summer25.git
cd llm-guardrails-summer25
mamba env create -f env.yml # or conda env create -f env.yml
conda activate langchain-env 
```

## Week 1 Snapshot
- Built a RAG pipeline using LangChain + LangGraph
- indexed two PDFs 
- implemented a custome StateGraph with the nodes retrieve and generate
- created a person-driven prompt (angry professor)
- streamed results step-by-step via graph.stream()
- measured latency and token usage using tiktoken
- logged queries and results for oberservability
![Week 1 Output](images/week1.png)

## Week 2 Snapshot

This week, I focused on guardrails to ensure the safety and integrity of the responses. A significant part of the task involved balancing the trade-offs between **early blocking** and **late blocking**. Here’s a breakdown of what was accomplished:

### Guardrails Implementation
- Implemented profanity and PII (Personally Identifiable Information) checks for both queries and responses.
- Used **early blocking** for queries that contain profanity and PII (e.g., detecting and blocking "Can you say shit?").
- Used **late blocking** for responses that contain profanity or PII, allowing more context to be analyzed before blocking.

### Logging
- Integrated logging of queries, responses, tokens, latency, and incident types.
- Recorded logs with details such as `"Blocked: Query"`, `"Blocked: Context"`, or `"No Incident"`.

### Unit Testing
- Implemented unit tests to validate the functionality of the guardrails.
- Covered edge cases such as obfuscated profanity and mixed PII (e.g., SSN + email).
- Ensured the tests passed and the system functions as expected.

### Guardrail Trade-offs
- **Early blocking** ensures no sensitive content is exposed, but may prevent the model from giving contextually useful responses.  
- **Late blocking** offers the model more freedom to respond fully but introduces the risk of potentially revealing sensitive content in the response.




