# MeetingMind AI

> **Day 1 of 100 | 100 Days 100 Startups Challenge**  
> An autonomous AI agent for intelligent meeting preparation.

MeetingMind AI helps sales executives, founders, and deal-makers walk into any meeting fully prepared. Given a meeting title, type, goal, and attendee information, it autonomously generates personalized briefings using Grok AI.

## Features

- **Attendee Profiles** - Psychological & professional profiles with interests, pain points, and conversation hooks
- **Strategic Agenda** - Time-boxed agenda optimized for your meeting goal  
- **Talking Points** - Specific phrases and tactics (not generic advice)
- **Predicted Q&A** - The 5 hardest questions + battle-tested answers
- **Pre-Meeting Checklist** - Prioritized actions with time estimates
- **Readiness Score** - Calculated score (0-100) based on preparation completeness

## Live Demo

**[View Live Demo](https://your-vercel-url.vercel.app)** (Update after deployment)

## Project Structure

```
Day-01-MeetingMind/
├── agent.py                 # Main Python agent (Grok AI)
├── api/
│   └── briefing.py          # Vercel serverless API endpoint
├── demo.html                # Interactive browser demo
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment config
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── startup-one-pager.md     # Business model & strategy
└── linkedin-post.md         # Marketing content
```

## Setup & Development

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd Day-01-MeetingMind
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Grok API key
```

**.env file:**
```
XAI_API_KEY=your_grok_api_key_here
```

Get your free Grok API key from: https://console.x.ai

### 3. Run Locally

**Python Agent:**
```bash
python agent.py
```

**Web Demo:**
```bash
# Open directly in browser
open demo.html  # macOS
start demo.html # Windows

# Or serve via Python
python -m http.server 8000
# Open http://localhost:8000/demo.html
```

## Deploy to Vercel

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/meetingmind-ai.git
git push -u origin main
```

### 2. Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your GitHub repository
4. In project settings, add environment variable:
   - **Name:** `XAI_API_KEY`
   - **Value:** Your Grok API key (`gsk_...`)
5. Click **Deploy**

### 3. Update README

After deployment, update the Live Demo link in this README with your actual Vercel URL.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `XAI_API_KEY` | Yes | Your Grok (xAI) API key |
| `SERP_API_KEY` | No | Optional, for live web research |

## How It Works

1. **Input:** Meeting details (title, type, goal, attendees)
2. **AI Processing:** Grok AI analyzes and generates:
   - Attendee psych profiles
   - Strategic agenda
   - Talking points & predicted Q&A
   - Action checklist
3. **Output:** Complete meeting briefing in Markdown/JSON

## Business Model

| Plan | Price | Features |
|------|-------|----------|
| Starter | $29/mo | 30 briefings/month |
| Pro | $79/mo | Unlimited, CRM sync |
| Team | $199/mo | Shared playbooks |
| Enterprise | Custom | SSO, API, dedicated CSM |

## Tech Stack

- **Backend:** Python + Grok AI (xAI)
- **Frontend:** Vanilla HTML/CSS/JS
- **Hosting:** Vercel (Serverless)
- **API:** OpenAI-compatible Grok API

## Target Market

- **B2B Sales Reps** (5.7M in US)
- **Startup Founders & CEOs** (600K in US)  
- **VC/PE Investors** (80K in US)

## Screenshots

*(Add screenshots after deployment)*

## Contributing

This is part of the **100 Days 100 Startups** challenge. Follow the journey!

## License

MIT License - feel free to use and modify.

---

**Built by:** Sathish Lella  
**Challenge:** 100 Days 100 Startups  
**Day:** 1 of 100
