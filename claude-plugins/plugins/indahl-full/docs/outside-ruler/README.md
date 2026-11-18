# Indahl Outside Ruler

`indahl-outside-ruler`

Checks your own work against a ruler you did not build, before it goes out. It runs a referee pass with the raw material only and applies ten checks drawn from mistakes that cost real corrections. Use it before publishing a number, shipping a release or sending a claim to someone who will act on it.

## What you get

- A referee pass on the raw material.
- The ten checks, each answered holds, fails or cannot tell:
  1. **Like for like.** The comparison was set up before the result was seen, with the same counting, time window and filters on both sides, and the filter that decides what counts does not depend on the thing being counted.
  2. **No hidden difference.** Items are counted one by one (what changed each way) before any average or net figure, against how much the same setup varies when nothing changes.
  3. **Same quantity.** Each stated figure is named for what it is (an average, a best case, a different definition) before two numbers are compared.
  4. **Numbers from the record.** Every count, date and version is read from the file, log or source, not from memory.
  5. **Quotes verbatim.** Nothing paraphrased sits inside quotation marks.
  6. **Four outcomes kept apart.** Nothing returned, refused, held and answered stay separate, and CANNOT_TELL is not folded into yes or no.
  7. **Labelled when defined after.** Anything chosen after seeing the result says so.
  8. **One source of truth.** The number on the page matches the ledger or data file it came from, everywhere it appears.
  9. **Checked live.** After release, the live page or artifact is read back, not the local copy.
  10. **Cheapest rebuttal tested.** The one-sentence objection the other side would make is checked against data before any line is kept or cut.
- A verdict: STANDS, MOVES (with the exact changes) or HOLD.

## How to use

Run `/outside-ruler` followed by what to check. For example:

```
/outside-ruler the v2.3 release notes and the raw results behind them
```

## Install

```
/plugin marketplace add Heuremen-LLC/indahl.ai
/plugin install indahl-outside-ruler@heuremen
```

## Requirements

None. Runs inside Claude Code.

## Services this plugin contacts

None. It runs inside your session.

## Privacy and terms

Privacy: https://indahl.ai/privacy
Terms: https://indahl.ai/terms

Heuremen LLC, https://indahl.ai. Source: https://github.com/Heuremen-LLC/indahl.ai/tree/main/claude-plugins/src/outside-ruler
