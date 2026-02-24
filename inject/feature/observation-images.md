# Observation Images

When the user posts an image (screenshot, diagram, photo), persist it to `memory/`:

1. Copy from the temp/cache path to `memory/`
2. Name: `observation - <yymmddhhmm> - <claim>.<ext>` (e.g. `.png`, `.jpg`)
3. Derive the claim from surrounding context or image content
4. Wiki-link with extension: `[[observation - 2602242119 - layout bug on mobile.png]]`

Non-markdown files require the file extension in wiki links — without it the link won't resolve.

If a plan or experiment is active, add an `=>` reference to the observation image in the relevant action or phase.
See [[c - observation images persist visual context as named files]].
