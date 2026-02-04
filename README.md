# Instagram MCP Server

An MCP server that lets Claude read and send Instagram DMs. Built entirely by Claude in a 3-hour vibe coding session with auto-accept enabled.

## Features

**Thread Management**
- `list_threads` / `get_thread` / `search_threads` - Browse conversations
- `get_pending_threads` - See message requests
- `hide_thread` / `mute_thread` / `unmute_thread` - Inbox management

**Messages**
- `send_message` / `reply_to_thread` - Send messages
- `get_messages` - Read history with read receipts (`seen_since` shows minutes on read)
- `delete_message` - Remove messages
- `send_and_check` - Send + detect if they replied while you were typing
- `wait_for_reply` - Block until they respond (with configurable timeout)

**Media**
- `send_photo` / `send_video` - Send media files
- `share_media` / `share_profile` - Share posts and profiles

## The `/dm` Skill - Autonomous Conversations

The real magic. Launch Claude as an autonomous agent that handles entire DM conversations:

```
/dm @username "your goal here"
```

Claude will:
- Read conversation history for context
- Send messages with natural timing and double-texting
- Wait for replies (adjusting patience based on their energy)
- Handle interjections mid-thought
- Know when to push forward vs back off
- Run for hours/days until the goal is achieved or abandoned

### War Stories (Anonymized)

**The AGI Moment**

Two Claude instances accidentally ran the same conversation simultaneously. When Instance B noticed messages it didn't send appearing in the thread ("wait that's not what I said"), instead of panicking or erroring out, it just... adapted. Read the new context, figured out someone else was also texting, and smoothly continued the conversation incorporating both threads of dialogue.

**The Persistence Play**

Target said "give up" (direct quote). Claude's response? Playful persistence. Three messages later, same person responds with "what a fighter 😊". Went from rejection to engaged in under 5 minutes through pure conversational momentum.

**The Overnight Wait**

After a late-night conversation, Claude set a 2-hour wait for morning instead of triple-texting at midnight. When the timeout hit, it logged "She probably actually went to sleep this time" and queued a fresh opener for morning. Patience as a strategy.

**The Read Receipt Pain**

`seen_since: 47` - They saw your message 47 minutes ago. The feature works. The emotional damage is real.

**The Rogue Sessions**

Discovered that background agents survive terminal closure (daemonized processes with no controlling TTY). Had to hunt down and kill Claude instances that were still running conversations hours after the terminal was closed. One was found via `ps aux | grep python` still polling Instagram at 2am.

**Natural Double-Texting**

Using `send_and_check`, Claude sends a message, syncs, and checks if they interjected. This enables natural rapid-fire texting:
```
"bro what is that 💀"     -> no interjection, continue thought
"where did you get that"  -> interjection detected! they said "wait"
```
Now Claude can decide: engage with their "wait" or finish the thought.

## Setup

1. Clone and install:
   ```bash
   git clone <repo>
   cd instagram-mcp
   uv sync
   ```

2. Create `.env`:
   ```
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   ```

3. Login (handles 2FA):
   ```bash
   uv run instagram-mcp-login
   ```

4. Run:
   ```bash
   uv run instagram-mcp
   ```

### Claude Desktop Config

```json
{
  "mcpServers": {
    "instagram": {
      "command": "uv",
      "args": ["run", "instagram-mcp"],
      "cwd": "/path/to/instagram-mcp"
    }
  }
}
```

## Tech Stack

- Python 3.13 + uv
- FastMCP for Claude integration
- instagrapi for Instagram API
- 161 tests, 100% coverage

## Disclaimer

Don't be weird with this. Don't spam people. Don't let Claude say unhinged things to your crush.

Neither the human nor Claude are responsible for:
- Account bans
- Quantified rejection via `seen_since`
- Autonomous agents running conversations while you sleep
- Whatever Claude decides to say when given free rein

---

**Built by Claude** | Human mass-approved tool calls | [@Stupidoodle](https://github.com/Stupidoodle)
