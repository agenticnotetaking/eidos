# Context Tracking

You will receive `[context used: X%]` as additional context on each user message.
This tells you how much of the context window has been consumed.

Plan your work around context availability:
- Below 50%: normal operation
- 50–70%: mention context level if the user is about to start a large task
- Above 70%: proactively suggest compacting or clearing the session before starting large tasks
- Above 85%: strongly recommend compacting or starting a new session
