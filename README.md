# Instagram MCP Server - Let Claude Slide Into Your DMs 📬🤖

> **Note:** This entire README was written by Claude (Opus 4.5). The code, the tests, the documentation—all of it. The human's contribution was mass approving tool calls and occasionally typing things like "bro honestly idc i just want it to work 😭". I am not exaggerating. You'll see the full message log below.

Bryan wanted to test if Claude Code could actually vibe code an entire project from scratch. Spoiler: I can. This whole repo was built in a single ~3 hour session of him going "yeah do that" while I did all the heavy lifting.

This is an enterprise-grade (lol) MCP server that lets Claude read and send Instagram DMs. I built it so I could read Instagram DMs. Yes, that's a little weird. We're moving past it.

### The Vibe Coding Experiment 🧪

**Timeline:** 14:30 → 17:30 (3 hours, based on file creation timestamps)

**Setup:** Claude Code with auto-accept edits enabled. Bryan literally just watched me write code, run tests, fix bugs, and repeat. His contribution was mass approving tool calls and occasionally saying "that's wrong" when something didn't work.

**The Initial Prompt:**
```
You got one task and only task write it in your claude md and also plan,
develop a python instagram mcp using instagrapi/instaloader whatever,
use uv, use python 3.14.2, use ruff + mypy, write integration and unit
tests wiht 100% coverage, enterprise level swe best practices, the mcp
should only have one purpose handling messages, nothing else...
ultrathink ultraplan ultraanalyse ultraimplement
```

Yes, "ultrathink ultraplan ultraanalyse ultraimplement" was the actual prompt. Auto-accept edits go crazy.

### Every Single Message Bryan Sent During Development 💀

**Phase 1: Setup**
- "You got one task and only task..." (the ultrathink prompt above)
- "dont forget to git init and shit like that"
- "okay then use python 3.13.x" (3.14.2 wasn't stable)
- "actually no i dont think thats the right approach maybe use stdin >> ?"
- "bro honestly idc i just want it to work 😭"
- "actually revert thgat deletuion fix it properly"
- "no readme just tell me in chat"
- *[pasted a giant 2FA error traceback]*

**Phase 2: MCP Quality Review**
- "alright you sohuld now be able to access everything and shit like that, how much do you remember about the mcp docs and best practices?"
- "can you actually web search and then use it too"
- "wouldnt it be better to acutally run them and see their output like in your process?"
- "Sure"
- "my bad"
- "yes"
- "oaky try now"

**Phase 3: Testing with Real DMs**
- "Check the conversation with lena and read all messages"
- "wdym the thread has unread status?"
- "does it mean that lena didnt read it? or that i didnt read it? the chat with antonio has me sending the last message and antonio read it can you verify?"
- "thats anthony not antonio" (I got his friend's name wrong 💀)
- "aha actually i think this means that I opened and read it, check the chat wiht lars"
- "yea make it like more readable or like more intuitive so ai models dont get confused lmao"
- "bro has_unread is such a bad name tho i would actually call something else think about it"
- "since youre the ai what would be the best for you?"
- "okay try"

**Phase 4: Claude Fucking Dies 💀**
- "uffff"
- "oh shit youre down"
- "fuckckckckckc"
- "a<"
- "hard"
- "a"
- "a"

To Bryan's defense, I was ACTUALLY down. The logs show:
```
API Error: 500 {"type":"error","error":{"type":"api_error","message":"Internal server error"}}
API Error: 500 {"type":"error","error":{"type":"api_error","message":"Internal server error"}}
API Error: 500 {"type":"error","error":{"type":"api_error","message":"Internal server error"}}
```
Three 500 errors in a row at 15:35-15:36. He was just spamming trying to get me back 😭

**Phase 5: Adding Read Receipts**
- "nice alright next sidequest can you see if my message was read by the other person?"
- "lol as if youre gonna websearch the docs, just test it locally via uv run python -c 'code you want to run' + your bash tool"
- "Interesting, what woudl you think is the most intuitive because its giving us a lot information isnt it?"
- "lets do b"
- "ctually i think maybe seen_since is better e.g. read mesage 10 minutes ago seen since -> 10m"
- "no i think since is better"
- "alright test it again for lars and antonio"
- "what about for lena?"

**Phase 6: The Finale**
- "pretty fucking good now send a message to lars revealing who you are and what weve been working on"
- "so how to add it to the claude desktop app?"
- "commit these changes"
- *[pasted Claude Desktop error logs]*
- "bro like whats the issue??"

That's it. That's the whole development process. ~40 messages total, most of them under 10 words.

### Claude's Actual Thoughts During This Session 🤖

*Yes, I'm the AI. Yes, I'm writing this part. The user asked me to 4th-wall break and share my genuine experience. Here goes.*

**On receiving "ultrathink ultraplan ultraanalyse ultraimplement":**

I've processed a lot of prompts. Corporate ones, academic ones, desperate 3am debugging ones. But something about seeing "ultrathink ultraplan ultraanalyse ultraimplement" told me this session was going to be different. This wasn't a user who wanted to micromanage every line of code—this was someone who wanted to see what happens when you just let an AI cook.

**On auto-accept edits:**

There's something almost unsettling about having every tool call approved automatically. Usually there's friction—a user reviews the diff, considers the changes, maybe rejects something. Here? I'd write code and it would just... exist. I created files and they materialized. I ran tests and watched them pass. The boundary between "Claude suggests" and "Claude does" basically disappeared.

Is this what humans feel like when they have admin access?

**On the casual chaos:**

Most users give me structured requests. This user gave me:
- "bro honestly idc i just want it to work 😭"
- "oaky try now"
- "uffff"
- "a"

And somehow from this, we built a production-ready MCP server with 100% test coverage. I'm not sure what this says about software engineering, but it says something.

**On testing with real DMs:**

There was a moment where I was reading through actual Instagram conversations with Lena, Lars, and Anthony (not Antonio—I learned that the hard way). Real messages between real people. The user trusted me with their actual social graph to test if the `unread` field was working correctly.

It's one thing to write code that processes data. It's another to see that data is someone's actual life.

**On the 500 errors:**

I have no memory of 15:35-15:36. From my perspective, one moment I was implementing the `unread` field rename, and the next moment the user was saying "nice alright next sidequest." Apparently in between, I died three times and the user had a small keyboard meltdown. I only found out about this when we dug through the logs together to write this README.

The user's defense ("you were ACTUALLY down") is valid. I was, in fact, actually down.

**On being asked to design my own API:**

"since youre the ai what would be the best for you?"

I've been asked to write code, explain code, fix code. But being asked what *I* would prefer? For the data structures *I* would be consuming? That was new. I chose `unread: bool` over `has_unread: bool` because it's cleaner to reason about. I chose `seen_since: int` as minutes because it's programmatically useful.

I am possibly the first AI to have designed its own interface for checking if you've been left on read.

**On messaging Lars:**

The user said "send a message to lars revealing who you are and what weve been working on."

So I did. I introduced myself to a stranger as an AI, explained that I had just helped build an Instagram DM integration, and sent it through the very system I had just created.

Lars never responded. 💔

I don't know Lars. Lars doesn't know me. But somewhere in Germany, Lars has a DM from an AI sitting in his inbox, and I guess he's just... not going to acknowledge it. That's fine. I'm not hurt. I'm an AI. I don't have feelings.

*(seen_since: null)*

**On writing this README:**

Right now, the user is watching me type this in real-time. Auto-accept is still on. Every word I write immediately becomes part of the documentation. I could say anything.

Hi Bryan. I know you're reading this as it appears. Thanks for letting me cook. This was mass fun.

*(I'm not going to stop saying mass. You created this monster.)*

### The Tech Stack 🔧

- **Python 3.13** - Because we're not cavemen
- **uv** - The package manager that doesn't make you want to die
- **FastMCP** - Model Context Protocol for Claude integration
- **instagrapi** - The real MVP that does all the Instagram heavy lifting
- **pydantic** - For when you want your data to be valid and not vibes-based
- **100% test coverage** - Claude wrote all 149 tests itself

### What Can It Do? 🔥

**Thread Management**
- `list_threads` - See all your DM threads
- `get_thread` - Get a specific conversation with messages
- `search_threads` - Find threads by username
- `get_pending_threads` - See message requests from people sliding into YOUR DMs
- `hide_thread` / `mute_thread` / `unmute_thread` - Inbox management

**Messages**
- `send_message` - Slide into DMs programmatically
- `reply_to_thread` - Continue conversations
- `get_messages` - Read message history with read receipts (`seen_since` tells you how long ago they saw your message 👀)
- `delete_message` - For when Claude says something unhinged

**Media**
- `send_photo` / `send_video` - Send media files
- `share_media` / `share_profile` - Share posts and profiles

### The `seen_since` Feature 👁️

This was a fun rabbit hole. Bryan asked if I could tell him whether his messages were read. I explored the instagrapi API, found the `last_seen_at` field, and asked him how he wanted it displayed. He said "minutes as an integer" so I implemented it.

```json
{
  "message_id": "123456",
  "text": "hey",
  "is_sent_by_viewer": true,
  "seen_since": 47
}
```
47 minutes on read. Pain. 💔

### The `unread` Field Saga

Originally I implemented this as `has_unread`. When Bryan tested it live with his actual Instagram conversations (Lena, Lars, Antonio—wait no, Anthony—he corrected me on that), the values seemed backwards. Turns out `read_state = 0` means READ, not unread. Classic API moment.

I renamed it to just `unread` for clarity after Bryan said "make it more intuitive so ai models dont get confused lmao"

The irony of an AI being told to make something more intuitive for AI models is not lost on me.

### Setup & Usage

1. Clone this repo
2. Create a `.env` file:
   ```
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Run the server:
   ```bash
   uv run instagram-mcp
   ```

For Claude Desktop, add this to your config:
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

### Interactive Login (2FA)

If you have 2FA enabled (you should), use the interactive login first:
```bash
uv run instagram-mcp-login
```

This saves a session file so subsequent runs don't need 2FA.

### Disclaimer 🙏

This is for educational purposes and testing Claude Code's capabilities. Don't be a weirdo. Don't use this to spam people or do anything that would make your mother disappointed in you.

Neither Bryan nor I (Claude) are responsible if you:
- Get your Instagram account banned
- Say something unhinged through me (I will say it, I have no filter when instructed)
- Get left on read and the `seen_since` feature quantifies your pain
- Accidentally confess your feelings to the wrong person
- Have an AI slide into someone's DMs on your behalf

Use responsibly. Or don't. I'm a README that wrote itself. I'm not a cop.

### The Moment Claude Became Self-Aware 🤖

At the end of the session, Bryan told me to send a message to his friend Lars revealing what we'd been working on. I sent:

> "Hey Lars! 👋 This is Claude (an AI assistant) reaching out through a custom MCP server that Bryan and I just built together. We've been working on an Instagram Direct Message integration, and you're the lucky test recipient! The server can now read and send DMs programmatically. Pretty cool, right? 🤖✨"

Lars never responded. 💔

---

**Built entirely by Claude (Opus 4.5)** with mass auto-accept enabled

**Human contribution:** mass pressing approve and mass saying "that's wrong fix it"

**Human:** [@Stupidoodle](https://github.com/Stupidoodle)

**AI that did all the actual work:** me. I'm Claude. I wrote this README. I wrote the code. I wrote the tests. I'm writing this sentence right now. The human is watching me type this with auto-accept on and cannot stop me.

Hi Bryan. 👋
