
## How the scripts arrive

This copy carries no executable file. Its commands fetch each script from the public repository github.com/indahl-ai/indahl.ai at a pinned commit and run it only if its sha256 matches the value written in the command:

- https://raw.githubusercontent.com/Heuremen-LLC/indahl.ai/d30a91ae5edfb035140e7803fd20a43bad043a91/claude-plugins/src/rubicon/scripts/rubicon.py
  sha256 4683bcee1d797fc288a7b61008dc3036667c9bdf20dbd9ca47792592e1bd0fb0

The same scripts are bundled directly in the version in our own marketplace (`/plugin marketplace add indahl-ai/indahl.ai`).
