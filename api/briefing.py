"""
Vercel Serverless Function for MeetingMind AI
Endpoint: /api/briefing
"""

import os
import json
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import MeetingMindAgent, MeetingRequest, Attendee


def handler(request):
    """Handle HTTP requests for briefing generation."""
    
    # Handle CORS
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }
    
    if request.get("method") == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}
    
    if request.get("method") != "POST":
        return {
            "statusCode": 405,
            "headers": headers,
            "body": json.dumps({"error": "Method not allowed"})
        }
    
    try:
        # Parse request body
        body = json.loads(request.get("body", "{}"))
        
        # Build meeting request
        attendees = [
            Attendee(
                name=a["name"],
                company=a["company"],
                title=a.get("title"),
                extra_context=a.get("extra_context")
            )
            for a in body.get("attendees", [])
        ]
        
        meeting_request = MeetingRequest(
            title=body.get("title", "Untitled Meeting"),
            meeting_type=body.get("meeting_type", "sales"),
            your_goal=body.get("your_goal", ""),
            your_name=body.get("your_name", "You"),
            your_company=body.get("your_company", "Your Company"),
            duration_minutes=body.get("duration_minutes", 60),
            attendees=attendees,
            extra_context=body.get("extra_context")
        )
        
        # Generate briefing using Grok
        agent = MeetingMindAgent()
        briefing = agent.prepare_briefing(meeting_request)
        
        # Convert to dict for JSON serialization
        import dataclasses
        result = dataclasses.asdict(briefing)
        
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(result, default=str)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }


# Vercel serverless function entry point
def POST(request):
    return handler(request)


def OPTIONS(request):
    return handler(request)
