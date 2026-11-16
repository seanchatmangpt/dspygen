ADR-0001: Use DSPy as the Core LLM Framework
=============================================

:Status: Accepted
:Date: 2024-09-14
:Deciders: Sean Chatman

Context
-------

dspygen needs a framework for composing LLM calls. Options considered:
LangChain, LlamaIndex, raw OpenAI SDK, and DSPy.

Decision
--------

Use **dspy-ai** as the primary abstraction for all LLM interactions.

Rationale
---------

- **Signatures** separate *what* from *how*, enabling optimizer-based fine-tuning
- **Teleprompters** (optimizers) allow few-shot and fine-tuned prompt generation without code changes
- **Provider-agnostic** — same code runs on OpenAI, Anthropic, Ollama, Groq, etc.
- **Active maintenance** — Stanford NLP group with rapid iteration

Consequences
------------

- All LLM calls go through ``dspy.Predict`` or higher-level modules
- Provider switching requires only ``dspy.settings.configure(lm=...)``
- Optimization workflows (few-shot, BootstrapFewShot) are first-class citizens
