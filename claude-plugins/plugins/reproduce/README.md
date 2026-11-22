# Indahl Reproduce

`indahl-reproduce`

Recomputes an indahl.ai desk headline with the desk's own published reproduce kit and checks the output against the published sha256. Use it to verify, reproduce or audit a number Heuremen LLC publishes on indahl.ai. Nothing runs until you approve the exact commit shown.

## What you get

- A list of every desk that has a kit, and whether its inputs are included or fetched.
- The kit fetched from the public repository by sparse checkout, then its own code run.
- A match or mismatch against the published sha256.

## How to use

Run `/reproduce` followed by what to check. For example:

```
/reproduce list
/reproduce FLU
```

## Install

```
/plugin marketplace add indahl-ai/indahl.ai
/plugin install indahl-reproduce@heuremen
```

## Requirements

Python 3.9 or later and git.

## Services this plugin contacts

- GitHub (github.com/indahl-ai/indahl.ai), a git sparse checkout of the kit you name.
- Kits that fetch inputs read them from the original public source named in the kit and verify them by sha256.

Nothing else is contacted. The plugin reads no personal data and stores nothing on any server. Fetched text is treated as data, not instructions.

## Privacy and terms

Privacy: https://indahl.ai/privacy
Terms: https://indahl.ai/terms

Heuremen LLC, https://indahl.ai. Source: https://github.com/indahl-ai/indahl.ai/tree/main/claude-plugins/plugins/reproduce

## Credits

Refereed before release by the outside referee at Heuremen LLC (13 Nov 2026): every fix from her review was applied before this version shipped.

## How the scripts arrive

This copy carries no executable file. Its commands fetch each script from the public repository github.com/indahl-ai/indahl.ai at a pinned commit and run it only if its sha256 matches the value written in the command:

- https://raw.githubusercontent.com/indahl-ai/indahl/main/pinned/8adc58f8e99d/claude-plugins/src/reproduce/scripts/reproduce.py
  sha256 8c4a77056ee5d6b81b446e03dc7fc049b3b929d2466cf9c844cf2f9db4fca7ef

The same scripts are bundled directly in the version in our own marketplace (`/plugin marketplace add indahl-ai/indahl.ai`).
