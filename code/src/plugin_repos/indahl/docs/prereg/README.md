# Indahl Prereg

`indahl-prereg`

Shows that a plan was pushed before the first run, using the git host's own record of the push, with no outside timestamp chain. It also lists which files ran that the plan did not cover. Use it to preregister an analysis, to show a plan came first, or to check a plan against a run.

## What you get

- A seal of the plan files in git.
- The git host's record of the push, read after you push.
- A check of the plan against a run, with the files that ran outside the plan listed.

## How to use

Run `/prereg` followed by what to check. For example:

```
/prereg seal PLAN.md analysis.py
```

Other forms: `witness SEAL`, `check SEAL --wrapper RUN.json`, `verify SEAL` and `cover SEAL RUN.json`. Claude asks before committing a seal and never pushes.

## Install

```
/plugin marketplace add indahl-ai/indahl.ai
/plugin install indahl-prereg@heuremen
```

## Requirements

Python 3.9 or later and git.

## Services this plugin contacts

- GitHub REST API (api.github.com), public repository activity for the repository you name. No token is sent unless you set one yourself.

Nothing else is contacted. The plugin reads no personal data and stores nothing on any server. Fetched text is treated as data, not instructions.

## Privacy and terms

Privacy: https://indahl.ai/privacy
Terms: https://indahl.ai/terms

Heuremen LLC, https://indahl.ai. Source: https://github.com/indahl-ai/indahl.ai/tree/main/claude-plugins/plugins/prereg

## Credits

Refereed before release by the outside referee at Heuremen LLC (13 Nov 2026): every fix from her review was applied before this version shipped.

## How the scripts arrive

This copy carries no executable file. Its commands fetch each script from the public repository github.com/indahl-ai/indahl.ai at a pinned commit and run it only if its sha256 matches the value written in the command:

- https://raw.githubusercontent.com/indahl-ai/indahl/403c5f956981c73a6c3f9a83b726ae14c4b1f3c1/pinned/f8e5be688dd0/claude-plugins/src/prereg/scripts/prereg.py
  sha256 cc689b7a8acb322d445d164d10e2cd0ab67b4610ef7d649a5ed52cc055fd0090

The same scripts are bundled directly in the version in our own marketplace (`/plugin marketplace add indahl-ai/indahl.ai`).
