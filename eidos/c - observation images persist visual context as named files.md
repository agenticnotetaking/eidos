# Observation images persist visual context as named files

Images posted during sessions are ephemeral — they live only in `.claude/image-cache/` and disappear with the session.
Visual observations deserve the same externalisation treatment as text.

## Convention

When the user posts an image (screenshot, diagram, photo), persist it:

1. Copy from the temp/cache path to `memory/`
2. Name it `observation - <yymmddhhmm> - <claim>.<ext>` (e.g. `.png`, `.jpg`)
3. Derive the claim from surrounding context or image content
4. Wiki-link it where relevant: `[[observation - 2602242119 - layout bug on mobile.png]]`

Non-markdown files require the file extension in wiki links — without it the link won't resolve.

## Linking

If a plan or experiment is active, add an `=>` reference to the observation image in the relevant action or phase.
The image becomes part of the project's documented history, not just chat ephemera.

## Interactions

- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — `observation` is an existing procedural prefix; images extend it to non-markdown
- [[spec - externalise - persist insights beyond the conversation]] — images are insights too
