---
tldr: Copy relevant content to the system clipboard
category: utility
---

# /eidos:clip

Copy something to the system clipboard so the user can paste it elsewhere.

## Usage

```
/eidos:clip [what to copy]
```

## Instructions

1. Determine what to copy:
   - If the user specifies what (e.g. "clip that command", "clip the file path"), copy that.
   - If context makes it obvious (e.g. just generated a command, a snippet, a URL), copy the relevant thing.
   - If ambiguous, ask.
2. Detect the platform and use the appropriate clipboard command:
   - **macOS:** `pbcopy`
   - **Linux (X11):** `xclip -selection clipboard`
   - **Linux (Wayland):** `wl-copy`
   - **WSL/Windows:** `clip.exe`
3. Pipe the content into the clipboard command via `echo` or `printf`.
4. Confirm briefly: "Copied to clipboard."
