---
tldr: End a session by exporting conversation, reflecting on insights, and offering to merge
---

# /eidos:done

## Target

Sessions end abruptly.
Without a deliberate close, insights stay in chat and branches stay unmerged.
Done provides a structured session end.

## Behaviour

- Exports conversation to markdown (via tomd)
- Offers to reflect on the export (via reflect)
- Shows branch status and offers to merge
- Updates any active plan's Progress Log with session summary

## Design

Done is an orchestrator — it chains other skills (tomd, reflect) and adds merge logic.

{[?] Research whether mono's approach to session export is optimal or if it can be improved}

## Interactions

- [[spec - reflect skill - extract learnings from session or file]] — reflect on session export
- [[spec - plan skill - structured plan for multi step work]] — update active plan's Progress Log
- [[spec - git workflow - branch per task with atomic commits]] — merge offer

## Mapping

> [[skills/done/done.md]]
