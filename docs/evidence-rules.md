# Evidence rules

The table is only useful if a row means the same thing to everyone reading it.

## What a row must carry

1. **The claim, in the source's own words.** Not a paraphrase that rounds "under 20 minutes" into "minutes".
2. **The hardware the source used.** If the source does not name a GPU/CPU model, say `not pinned` — do not guess.
3. **The version or commit.** Simulation throughput changes between releases; an unversioned number is an anecdote.
4. **A link to the exact place.** Paper section, README anchor, release note. A repo root link is not enough.
5. **A label.** `UPSTREAM`, `3P`, or `MEASURED` (definitions in the README).

## What disqualifies a row

| pattern | why it fails |
| --- | --- |
| "10× faster than before" with no "before" | unfalsifiable |
| throughput with no hardware | not reproducible |
| benchmark over a model the source does not name | not comparable |
| cherry-picked best-of-one | see the spread discussion in [sim-dt-pareto](https://github.com/cccjj55/sim-dt-pareto) |
| vendor launch page with no version | marketing, not measurement |

## What counts as `3P`

Someone other than the author publishes the number **with their own hardware, version and command**. A blog post
that repeats the author's number is still `UPSTREAM`.

## What counts as `MEASURED`

The artifact is committed to the repo that produced it: raw samples, the exact command, the environment fingerprint.
A screenshot is not an artifact.

## On disagreeing

If your `3P` number contradicts an `UPSTREAM` row, that row gets *both* numbers and a note on what differs
(hardware class, version, scene complexity). Deleting the inconvenient row is the one thing this repo will not do.
