---
tldr: Letters group topics, numbers group subtopics — enables selective response in multi-topic dialogue
---

# Structured dialogue uses letter-number grouping for topic threads

When a skill presents multiple topics for discussion (meta analysis, refinement, feedback), group them as:

```
A. First topic
   Observation / question / comment

B. Second topic
   B1. Sub-point one
   B2. Sub-point two

C. Third topic
```

The human can then respond selectively — engage with B, skip A, redirect C.
Multiple rounds are expected; threads deepen or get dropped based on the human's engagement.

This is distinct from [[spec - numbered lists - structured selectable output|numbered lists]] (decimal notation: 1.1, 1.2) which is for **action selection** — the user picks items to act on.
Letter-number grouping is for **dialogue** — the user responds to topics conversationally.

Used by:
- [[spec - refine skill - processes inline comments via structured dialogue|/eidos:refine]] — structured Q&A on `{{comments}}`
- [[spec - meta skill - analyse eidos skill outputs for quality and abstraction|/eidos:meta]] — structured feedback on skill output quality
