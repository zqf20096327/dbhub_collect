# claude-tidbits

Useful customizations and scripts for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## statusline-command.sh

A custom status line script for Claude Code that displays:

```
[Claude Opus 4.6] 📁 my-project | 🌿 main
████░░░░░░ 42% | $1.25 | ⏱️ 5m 45s
```

**Line 1:** Model name, project directory (clickable link to GitHub repo), git branch

**Line 2:** Context window usage bar, session cost, elapsed time

### Features

- Bold ANSI colors that work on both light and dark terminal themes
- Context bar changes color: green < 70%, yellow 70-89%, red 90%+
- Project folder name is a clickable terminal hyperlink to the GitHub repo (OSC 8)
- Git info (branch + remote URL) cached for 5 seconds to keep the status line fast

### Setup

1. Copy the script:

```bash
cp statusline-command.sh ~/.claude/statusline-command.sh
chmod +x ~/.claude/statusline-command.sh
```

2. Add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline-command.sh"
  }
}
```

3. Restart Claude Code.
