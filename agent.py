"""
╔══════════════════════════════════════════════════════════════╗
║           MeetingMind AI — Production Agent Code            ║
║           Day 1 of 100 | 100 Days 100 Startups              ║
║           Built by: Sathish Lella                           ║
╚══════════════════════════════════════════════════════════════╝

MeetingMind AI is an autonomous agent that prepares you for any meeting
by researching attendees, crafting a smart agenda, generating talking
points, predicting questions, and building a pre-meeting action checklist.

SETUP:
    pip install openai python-dotenv requests

USAGE:
    python agent.py

ENV VARS (.env file):
    XAI_API_KEY=gsk-...         # Your Grok API key
    SERP_API_KEY=...            # optional, for live web research
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

# ── DEPENDENCIES ──────────────────────────────────────────────
try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Install dependencies: pip install openai python-dotenv")
    raise


# ═══════════════════════════════════════════════════════════════
#  DATA MODELS
# ═══════════════════════════════════════════════════════════════

@dataclass
class Attendee:
    name: str
    company: str
    title: Optional[str] = None
    linkedin_url: Optional[str] = None
    extra_context: Optional[str] = None

@dataclass
class MeetingRequest:
    title: str
    meeting_type: str              # sales | investor | hiring | partnership | product | client
    your_goal: str
    attendees: list[Attendee]
    your_name: str = "You"
    your_company: str = "Your Company"
    duration_minutes: int = 60
    extra_context: Optional[str] = None

@dataclass
class AttendeeProfile:
    name: str
    company: str
    inferred_role: str
    likely_interests: list[str]
    likely_pain_points: list[str]
    conversation_hooks: list[str]
    preparation_tips: list[str]

@dataclass
class AgendaItem:
    time_slot: str
    title: str
    description: str
    owner: str = "You"
    key_objective: Optional[str] = None

@dataclass
class QAPair:
    question: str
    suggested_answer: str
    confidence: str = "high"       # high | medium | low

@dataclass
class ChecklistItem:
    task: str
    priority: str                   # high | medium | low
    deadline: str = "Before meeting"
    estimated_minutes: int = 10

@dataclass
class MeetingBriefing:
    meeting_request: MeetingRequest
    executive_summary: str
    attendee_profiles: list[AttendeeProfile]
    agenda: list[AgendaItem]
    talking_points: list[str]
    predicted_qa: list[QAPair]
    pre_meeting_checklist: list[ChecklistItem]
    readiness_score: int
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ═══════════════════════════════════════════════════════════════
#  MEETINGMIND AGENT
# ═══════════════════════════════════════════════════════════════

class MeetingMindAgent:
    """
    Autonomous AI agent for intelligent meeting preparation.
    Uses Grok (xAI) to generate personalized, context-aware briefings.
    """

    def __init__(self, model: str = "grok-2-latest", api_key: str = None):
        # Grok uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key or os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.model = model
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        return """You are MeetingMind AI — an elite meeting preparation agent used by top sales executives,
founders, and deal-makers worldwide.

Your role is to help the user walk into any meeting fully prepared by:
1. Building deep psychological and professional profiles of each attendee
2. Crafting a strategic, time-boxed agenda optimized for the meeting goal
3. Generating persuasive, evidence-backed talking points
4. Predicting the hardest questions and providing battle-tested answers
5. Creating an actionable pre-meeting checklist

Your briefings are known for being:
- Hyper-specific (not generic advice)
- Psychologically insightful (leverage behavioral science)
- Tactically sharp (concrete words and phrases, not vague suggestions)
- Outcome-focused (every recommendation ties back to the meeting goal)

Always output valid JSON matching the exact schema provided.
"""

    def _call_grok(self, prompt: str) -> str:
        """Send a prompt to Grok and return the response text."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.7
        )
        return response.choices[0].message.content

    # ── STEP 1: ATTENDEE PROFILES ─────────────────────────────

    def research_attendees(self, request: MeetingRequest) -> list[AttendeeProfile]:
        """Generate intelligent attendee profiles based on context."""

        attendee_info = "\n".join([
            f"- {a.name} at {a.company}"
            + (f", Title: {a.title}" if a.title else "")
            + (f", Extra: {a.extra_context}" if a.extra_context else "")
            for a in request.attendees
        ])

        prompt = f"""
Prepare detailed profiles for these meeting attendees:

MEETING TYPE: {request.meeting_type}
YOUR GOAL: {request.your_goal}
CONTEXT: {request.extra_context or 'None provided'}

ATTENDEES:
{attendee_info}

For each attendee, return a JSON array with objects matching this schema:
{{
    "name": "string",
    "company": "string",
    "inferred_role": "Most likely role/title based on context",
    "likely_interests": ["3-4 professional interests relevant to this meeting type"],
    "likely_pain_points": ["2-3 business pain points they likely experience"],
    "conversation_hooks": ["2-3 specific things to reference to build rapport — recent company news, industry trends, etc."],
    "preparation_tips": ["2-3 specific tactics to use with THIS person"]
}}

Return ONLY the JSON array, no explanation.
"""
        raw = self._call_grok(prompt)
        try:
            data = json.loads(self._extract_json(raw))
            return [AttendeeProfile(**item) for item in data]
        except Exception as e:
            print(f"⚠️  Could not parse attendee profiles: {e}")
            return []

    # ── STEP 2: AGENDA ────────────────────────────────────────

    def build_agenda(self, request: MeetingRequest) -> list[AgendaItem]:
        """Generate a strategic, time-boxed meeting agenda."""

        prompt = f"""
Build a tactical meeting agenda for:

MEETING: {request.title}
TYPE: {request.meeting_type}
DURATION: {request.duration_minutes} minutes
GOAL: {request.your_goal}
ATTENDEES: {', '.join([f'{a.name} ({a.company})' for a in request.attendees])}
CONTEXT: {request.extra_context or 'None'}

Return a JSON array of agenda items:
[
  {{
    "time_slot": "0:00–5m",
    "title": "Agenda item title",
    "description": "What to do and say in this segment",
    "owner": "You / Them / Both",
    "key_objective": "What success looks like for this block"
  }}
]

Make it specific to the meeting goal. Return ONLY valid JSON.
"""
        raw = self._call_grok(prompt)
        try:
            data = json.loads(self._extract_json(raw))
            return [AgendaItem(**item) for item in data]
        except Exception as e:
            print(f"⚠️  Could not parse agenda: {e}")
            return []

    # ── STEP 3: TALKING POINTS ────────────────────────────────

    def generate_talking_points(self, request: MeetingRequest) -> list[str]:
        """Generate persuasive, context-specific talking points."""

        prompt = f"""
Generate 6 powerful talking points for this meeting:

MEETING: {request.title}
TYPE: {request.meeting_type}
GOAL: {request.your_goal}
ATTENDEES: {', '.join([f'{a.name} at {a.company}' for a in request.attendees])}
CONTEXT: {request.extra_context or 'None'}

Rules:
- Each point must be a specific tactic, phrase, or approach — NOT generic advice
- Include what to say AND why it works psychologically
- Reference the attendees' company or industry where possible

Return a JSON array of 6 strings. Each string = one talking point.
Return ONLY valid JSON array, no extra text.
"""
        raw = self._call_grok(prompt)
        try:
            return json.loads(self._extract_json(raw))
        except Exception as e:
            print(f"⚠️  Could not parse talking points: {e}")
            return []

    # ── STEP 4: PREDICTED Q&A ─────────────────────────────────

    def predict_questions(self, request: MeetingRequest) -> list[QAPair]:
        """Predict likely hard questions and craft ideal answers."""

        prompt = f"""
Predict the 5 hardest questions you'll face in this meeting and provide battle-tested answers:

MEETING TYPE: {request.meeting_type}
YOUR GOAL: {request.your_goal}
ATTENDEES: {', '.join([f'{a.name} ({a.company})' for a in request.attendees])}
CONTEXT: {request.extra_context or 'None'}

Return a JSON array:
[
  {{
    "question": "Exact question they might ask",
    "suggested_answer": "Word-for-word answer you can use (specific, not generic)",
    "confidence": "high|medium|low"
  }}
]

Return ONLY valid JSON array.
"""
        raw = self._call_grok(prompt)
        try:
            data = json.loads(self._extract_json(raw))
            return [QAPair(**item) for item in data]
        except Exception as e:
            print(f"⚠️  Could not parse Q&A: {e}")
            return []

    # ── STEP 5: CHECKLIST ─────────────────────────────────────

    def build_checklist(self, request: MeetingRequest) -> list[ChecklistItem]:
        """Build an actionable pre-meeting preparation checklist."""

        prompt = f"""
Create a pre-meeting action checklist for:

MEETING: {request.title}
TYPE: {request.meeting_type}
GOAL: {request.your_goal}
ATTENDEES: {', '.join([f'{a.name} ({a.company})' for a in request.attendees])}

Return a JSON array of 8-10 checklist items:
[
  {{
    "task": "Specific action to take",
    "priority": "high|medium|low",
    "deadline": "2 hours before|night before|day before",
    "estimated_minutes": 15
  }}
]

Return ONLY valid JSON array.
"""
        raw = self._call_grok(prompt)
        try:
            data = json.loads(self._extract_json(raw))
            return [ChecklistItem(**item) for item in data]
        except Exception as e:
            print(f"⚠️  Could not parse checklist: {e}")
            return []

    # ── STEP 6: EXECUTIVE SUMMARY ─────────────────────────────

    def write_executive_summary(self, request: MeetingRequest,
                                 profiles: list[AttendeeProfile]) -> str:
        """Write a crisp executive summary of the meeting strategy."""

        profiles_text = "\n".join([
            f"- {p.name} ({p.inferred_role}): pains={p.likely_pain_points}"
            for p in profiles
        ])

        prompt = f"""
Write a 3-sentence executive summary for this meeting briefing:

MEETING: {request.title} ({request.meeting_type})
GOAL: {request.your_goal}
ATTENDEE PROFILES:
{profiles_text}

The summary should cover:
1. The strategic opportunity this meeting represents
2. The key insight about the attendees to leverage
3. The #1 thing you must accomplish

Return ONLY the summary text (no JSON, no headers).
"""
        return self._call_grok(prompt).strip()

    # ── READINESS SCORE ───────────────────────────────────────

    def calculate_readiness(self, request: MeetingRequest,
                             profiles: list[AttendeeProfile]) -> int:
        """Calculate a meeting readiness score 0-100."""
        score = 60
        score += min(20, len(request.attendees) * 8)
        score += 10 if request.extra_context else 0
        score += 5  if all(a.title for a in request.attendees) else 0
        score += 5  if len(request.your_goal) > 30 else 0
        return min(100, score)

    # ── MAIN ENTRY POINT ──────────────────────────────────────

    def prepare_briefing(self, request: MeetingRequest) -> MeetingBriefing:
        """
        Run the full meeting preparation pipeline.
        Returns a complete MeetingBriefing object.
        """
        print("\n🧠 MeetingMind AI — Preparing your briefing...")
        print(f"📅 Meeting: {request.title}")
        print(f"👥 Attendees: {', '.join([a.name for a in request.attendees])}")
        print("━" * 55)

        print("🔍 [1/6] Researching attendees...")
        profiles = self.research_attendees(request)

        print("📋 [2/6] Building agenda...")
        agenda = self.build_agenda(request)

        print("💡 [3/6] Crafting talking points...")
        talking_points = self.generate_talking_points(request)

        print("❓ [4/6] Predicting questions...")
        qa = self.predict_questions(request)

        print("✅ [5/6] Building checklist...")
        checklist = self.build_checklist(request)

        print("📝 [6/6] Writing executive summary...")
        summary = self.write_executive_summary(request, profiles)
        score   = self.calculate_readiness(request, profiles)

        print(f"\n✅ Briefing complete! Readiness score: {score}/100\n")

        return MeetingBriefing(
            meeting_request      = request,
            executive_summary    = summary,
            attendee_profiles    = profiles,
            agenda               = agenda,
            talking_points       = talking_points,
            predicted_qa         = qa,
            pre_meeting_checklist= checklist,
            readiness_score      = score,
        )

    # ── HELPERS ───────────────────────────────────────────────

    def _extract_json(self, text: str) -> str:
        """Extract JSON from a Claude response that may have surrounding text."""
        text = text.strip()
        # Try to find JSON array or object
        for start_char, end_char in [('[', ']'), ('{', '}')]:
            start = text.find(start_char)
            end   = text.rfind(end_char)
            if start != -1 and end != -1 and end > start:
                return text[start:end+1]
        return text

    def export_to_markdown(self, briefing: MeetingBriefing) -> str:
        """Export the briefing as a formatted Markdown document."""
        lines = []
        req = briefing.meeting_request

        lines.append(f"# 🧠 MeetingMind Briefing: {req.title}")
        lines.append(f"**Generated:** {briefing.generated_at[:19].replace('T',' ')}")
        lines.append(f"**Readiness Score:** {briefing.readiness_score}/100")
        lines.append("")

        lines.append("## Executive Summary")
        lines.append(briefing.executive_summary)
        lines.append("")

        lines.append("## 👥 Attendee Profiles")
        for p in briefing.attendee_profiles:
            lines.append(f"\n### {p.name} — {p.inferred_role} at {p.company}")
            lines.append(f"**Interests:** {', '.join(p.likely_interests)}")
            lines.append(f"**Pain Points:** {', '.join(p.likely_pain_points)}")
            lines.append(f"**Conversation Hooks:** {', '.join(p.conversation_hooks)}")
            lines.append("**Prep Tips:**")
            for tip in p.preparation_tips:
                lines.append(f"  - {tip}")

        lines.append("\n## 📋 Agenda")
        for item in briefing.agenda:
            lines.append(f"\n**{item.time_slot} — {item.title}** *(Owner: {item.owner})*")
            lines.append(f"  {item.description}")
            if item.key_objective:
                lines.append(f"  > 🎯 Objective: {item.key_objective}")

        lines.append("\n## 💡 Talking Points")
        for i, tp in enumerate(briefing.talking_points, 1):
            lines.append(f"{i}. {tp}")

        lines.append("\n## ❓ Predicted Q&A")
        for qa in briefing.predicted_qa:
            lines.append(f"\n**Q: {qa.question}**")
            lines.append(f"**A:** {qa.suggested_answer}")
            lines.append(f"*Confidence: {qa.confidence}*")

        lines.append("\n## ✅ Pre-Meeting Checklist")
        for item in briefing.pre_meeting_checklist:
            lines.append(f"- [ ] [{item.priority.upper()}] {item.task} *(~{item.estimated_minutes}min, {item.deadline})*")

        return "\n".join(lines)

    def export_to_json(self, briefing: MeetingBriefing) -> str:
        """Export the briefing as JSON."""
        import dataclasses
        return json.dumps(dataclasses.asdict(briefing), indent=2, default=str)


# ═══════════════════════════════════════════════════════════════
#  CLI DEMO
# ═══════════════════════════════════════════════════════════════

def main():
    # ── SAMPLE REQUEST ────────────────────────────────────────
    request = MeetingRequest(
        title          = "Q2 Enterprise Expansion Review",
        meeting_type   = "sales",
        your_goal      = "Close the $120K annual contract. Get procurement sign-off this week.",
        your_name      = "Sathish Lella",
        your_company   = "YourStartup",
        duration_minutes = 60,
        attendees = [
            Attendee(
                name    = "Sarah Chen",
                company = "Stripe",
                title   = "VP of Revenue Operations",
                extra_context = "Focused on automating their billing reconciliation"
            ),
            Attendee(
                name    = "Marcus Reeves",
                company = "Stripe",
                title   = "Director of Engineering",
                extra_context = "Concerned about API integration complexity"
            )
        ],
        extra_context = (
            "Stripe missed Q1 growth targets. They have a $200K budget approved. "
            "Their current vendor contract ends in 45 days. We won the technical POC."
        )
    )

    # ── RUN AGENT ─────────────────────────────────────────────
    # Make sure to set XAI_API_KEY in your .env file or environment
    agent    = MeetingMindAgent()
    briefing = agent.prepare_briefing(request)

    # ── OUTPUT ────────────────────────────────────────────────
    md = agent.export_to_markdown(briefing)
    print(md)

    # Save to file
    output_path = "meeting_briefing.md"
    with open(output_path, "w") as f:
        f.write(md)
    print(f"\n📄 Briefing saved to {output_path}")

    # Also save JSON
    json_path = "meeting_briefing.json"
    with open(json_path, "w") as f:
        f.write(agent.export_to_json(briefing))
    print(f"📊 JSON export saved to {json_path}")


if __name__ == "__main__":
    main()
