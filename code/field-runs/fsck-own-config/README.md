# Field run: indahl-fsck on our own MCP setup

**Job.** Our Claude Code setup had grown to 123 MCP servers. The `/mcp` list ran past two hundred lines, and a connector that would not sign in took an hour to trace by hand.

**Result.** `fsck_report.txt`: about fifteen lines, grouped by the fix. 38 servers needed nothing. 70 belonged to plugins that were never signed in, 44 of them in four bundle plugins. 10 were broken (no such host, wrong address, bad token, a local server that exits, a refused handshake). 6 servers were reached twice, as a connector and as a plugin.

**What fsck could not see.** One failing connector that `/mcp` showed was missing from `claude mcp list`, so fsck could not report it. That limit is in the plugin's README. The raw `claude mcp list` output is not published.
