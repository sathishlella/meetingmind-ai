# MeetingMind AI — Agent Documentation

> **Day 1 of 100 | 100 Days 100 Startups Challenge**  
> An autonomous AI agent for intelligent meeting preparation.

---

## Project Overview

MeetingMind AI is an AI-powered meeting preparation agent that helps sales executives, founders, and deal-makers walk into any meeting fully prepared. Given a meeting title, type, goal, and attendee information, it autonomously generates:

- **Attendee Profiles** — psychological and professional profiles with interests, pain points, and conversation hooks
- **Strategic Agenda** — time-boxed agenda optimized for the meeting goal
- **Talking Points** — specific phrases and tactics (not generic advice)
- **Predicted Q&A** — the 5 hardest questions + battle-tested word-for-word answers
- **Pre-Meeting Checklist** — prioritized actions with time estimates
- **Readiness Score** — calculated score (0-100) based on preparation completeness

### Files in This Project

| File | Purpose |
|------|---------|
| `agent.py` | Production Python agent code using Claude API (530 lines) |
| `demo.html` | Interactive browser demo with mock data (838 lines) |
| `startup-one-pager.md` | Business model, GTM strategy, and revenue projections |
| `linkedin-post.md` | Marketing content and engagement strategy |

---

## Technology Stack

### Core Technologies
- **Language:** Python 3.8+
- **AI Model:** Anthropic Claude (default: `claude-opus-4-6`)
- **Environment:** Standard Python with `asyncio` support

### Dependencies
```bash
pip install anthropic openai python-dotenv requests
```

| Package | Purpose |
|---------|---------|
| `anthropic` | Claude API client for AI-powered briefing generation |
| `python-dotenv` | Environment variable management |
| `requests` | HTTP requests for optional web research (SERP API) |
| `openai` | Optional alternative LLM backend |

### Demo/Frontend
- **Type:** Static HTML file with embedded JavaScript and CSS
- **No build process required** — open directly in browser
- **Mock data only** — no backend integration in demo

---

## Project Structure

```
Day-01-MeetingMind/
├── agent.py                 # Main production agent
├── demo.html                # Interactive browser demo
├── startup-one-pager.md     # Business documentation
├── linkedin-post.md         # Marketing content
└── AGENTS.md               # This file
```

### Code Organization (`agent.py`)

```
agent.py
├── Data Models (dataclasses)
│   ├── Attendee             # Meeting attendee info
│   ├── MeetingRequest       # Input request structure
│   ├── AttendeeProfile      # Generated attendee analysis
│   ├── AgendaItem           # Time-boxed agenda item
│   ├── QAPair               # Question + answer pair
│   ├── ChecklistItem        # Pre-meeting task
│   └── MeetingBriefing      # Complete output container
│
├── MeetingMindAgent (main class)
│   ├── __init__()           # Initialize Claude client
│   ├── _build_system_prompt() # Elite meeting prep persona
│   ├── _call_claude()       # API communication
│   │
│   ├── research_attendees() # Step 1: Build attendee profiles
│   ├── build_agenda()       # Step 2: Generate strategic agenda
│   ├── generate_talking_points() # Step 3: Craft talking points
│   ├── predict_questions()  # Step 4: Predict Q&A pairs
│   ├── build_checklist()    # Step 5: Create action checklist
│   ├── write_executive_summary() # Step 6: Generate summary
│   ├── calculate_readiness()     # Calculate readiness score
│   │
│   ├── prepare_briefing()   # Main pipeline entry point
│   ├── export_to_markdown() # Output formatter (MD)
│   └── export_to_json()     # Output formatter (JSON)
│
└── main()                   # CLI demo with sample data
```

---

## Environment Setup

### Required Environment Variables

Create a `.env` file in the project root:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional (for live web research)
SERP_API_KEY=...
```

### Running the Application

```bash
# 1. Install dependencies
pip install anthropic python-dotenv requests

# 2. Set up environment variables
# Create .env file with ANTHROPIC_API_KEY

# 3. Run the agent
python agent.py
```

### Running the Demo

```bash
# Open directly in browser (no server required)
open demo.html        # macOS
start demo.html       # Windows
xdg-open demo.html    # Linux
```

Or serve via simple HTTP server:
```bash
python -m http.server 8000
# Then open http://localhost:8000/demo.html
```

---

## Code Style Guidelines

### Python Conventions

1. **Imports:** Group in order: stdlib, third-party, local
2. **Type Hints:** Use `typing` module for all function signatures
3. **Docstrings:** Use triple quotes for module, class, and function docs
4. **Dataclasses:** Prefer `@dataclass` for data containers
5. **Comments:** Use section dividers with box-drawing characters:
   ```python
   # ═══════════════════════════════════════════════════════════════
   #  SECTION NAME
   # ═══════════════════════════════════════════════════════════════
   ```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `MeetingMindAgent` |
| Functions | snake_case | `prepare_briefing()` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_MODEL` |
| Private methods | _leading_underscore | `_call_claude()` |

### Error Handling

All parsing operations wrap in try/except and return empty collections on failure:
```python
try:
    data = json.loads(self._extract_json(raw))
    return [AttendeeProfile(**item) for item in data]
except Exception as e:
    print(f"⚠️  Could not parse attendee profiles: {e}")
    return []
```

---

## Output Files

When running `agent.py`, two files are generated:

| File | Format | Content |
|------|--------|---------|
| `meeting_briefing.md` | Markdown | Human-readable briefing document |
| `meeting_briefing.json` | JSON | Machine-readable structured data |

---

## Security Considerations

1. **API Keys:** Never commit `.env` files. Add to `.gitignore`:
   ```
   .env
   meeting_briefing.md
   meeting_briefing.json
   ```

2. **Data Privacy:** Meeting briefings may contain sensitive business information. Consider:
   - Local-only processing (no cloud storage)
   - Encryption at rest for generated briefings
   - PII scrubbing before LLM API calls

3. **Rate Limits:** Claude API has rate limits. Implement backoff for production use.

---

## Extension Points

To add new functionality:

### Adding a New Meeting Type

Edit `demo.html` → Add to `roles` object:
```javascript
const roles = {
    sales: [...],
    investor: [...],
    your_new_type: ['Role 1', 'Role 2', ...]
};
```

### Adding a New Output Section

1. Add dataclass in `agent.py` for the new data type
2. Add generation method to `MeetingMindAgent`
3. Update `MeetingBriefing` to include new field
4. Update `export_to_markdown()` formatter

### Adding Web Research Integration

Uncomment/implement SERP API calls in `research_attendees()`:
```python
# Optional: Add web search for attendee context
if os.getenv("SERP_API_KEY"):
    # Implement SERP API query
    pass
```

---

## Business Context

This project is part of the **100 Days 100 Startups Challenge** where the founder builds 100 AI agent startups in 100 days.

### Target Market
- B2B Sales Reps (5.7M in US)
- Startup Founders & CEOs (600K in US)
- VC/PE Investors (80K in US)

### Pricing Model
| Plan | Price | Features |
|------|-------|----------|
| Starter | $29/mo | 30 briefings/month |
| Pro | $79/mo | Unlimited, CRM sync |
| Team | $199/mo | Shared playbooks |
| Enterprise | Custom | SSO, API, dedicated CSM |

---

## Development Notes

- **No formal tests** — This is a rapid-prototype project
- **No CI/CD** — Manual deployment
- **Demo uses mock data** — Production version requires Claude API key
- **Single-file architecture** — Entire agent fits in one 530-line Python file

---

## Related Resources

- **Project:** Day 1 of 100 — 100 Days 100 Startups
- **Built by:** Sathish Lella
- **Challenge:** Building 100 AI agent startups in 100 days

---

*Last updated: 2026-04-01*
