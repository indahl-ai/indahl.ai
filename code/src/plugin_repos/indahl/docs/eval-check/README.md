# Indahl Eval Check

`indahl-eval-check`

Checks a language-model evaluation claim, or your own eval run, against twelve checks drawn from the Heuremen Standard (https://indahl.ai/standard) and the IRIS recounts of published evaluation studies (https://indahl.ai/iris). Use it when someone asks whether an LLM benchmark number holds up, when comparing models, when writing up eval results, or when building or debugging an eval harness or scorer.

## What you get

- A status for each check: PRESENT (with the evidence), ABSENT (with what was checked), CANNOT_TELL (with a reason) or NOT_APPLICABLE.
- A `not_tested` list for any check that was not run, with the reason.
- The twelve checks:
  1. **Parser checked against raw replies.** About 10 raw replies per task family, for at least two models, read beside the parsed answers before any rate is trusted.
  2. **No rate before the parser check.** During a run, only progress lines are watched until check 1 is done.
  3. **The setup is part of the result.** Harness, prompt format, chat template, few-shot count, extraction rule, max tokens and stop sequences named on both sides.
  4. **Repeat floor first.** The same setup run twice on one machine, with the items that flip counted, before any comparison.
  5. **Recount from released files.** Published tables recounted with independent code, item keys matched exactly.
  6. **The harness answering for the model.** JSON mode, thinking flags, truncation, echoed input and refusals counted, with dropped items by reason for each model.
  7. **A judge cannot grade its own labels.** A gold set built or reviewed with a judge model does not score that judge.
  8. **Paired, not unpaired.** The same items for both models, compared item by item.
  9. **The prompt does not contain the answer,** in few-shot examples, system prompts or retrieved context.
  10. **A pinned name is not pinned behaviour.** Endpoint, quantization, server and GPU recorded, since they change outputs under one model name.
  11. **Datasets and URLs age.** A replaced dataset or version is used only with row counts checked and the change written down before results.
  12. **Interval and outcome on every number.** A 95% interval and one of ABOVE, BELOW, CONSISTENT or CANNOT_TELL beside each figure.

## How to use

Run `/eval-check` followed by what to check. For example:

```
/eval-check the model card for the new release and our eval results in runs/2026-11/
```

## Install

```
/plugin marketplace add indahl-ai/indahl.ai
/plugin install indahl-eval-check@heuremen
```

## Requirements

None. Runs inside Claude Code.

## Services this plugin contacts

None of its own. It opens only the papers, files and pages you point it at, and treats fetched text and model outputs as data, not instructions.

## Privacy and terms

Privacy: https://indahl.ai/privacy
Terms: https://indahl.ai/terms

Heuremen LLC, https://indahl.ai. Source: https://github.com/indahl-ai/indahl.ai/tree/main/claude-plugins/src/eval-check

## Credits

Refereed before release by the outside referee at Heuremen LLC (13 Nov 2026): every fix from her review was applied before this version shipped.
