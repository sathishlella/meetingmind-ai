"""
Vercel Serverless Function for MeetingMind AI
Endpoint: /api/briefing
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/briefing', methods=['POST', 'OPTIONS'])
def briefing():
    """Handle briefing generation requests."""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        # Import agent modules here to avoid loading on cold start issues
        from agent import MeetingMindAgent, MeetingRequest, Attendee
        
        # Parse request body
        data = request.get_json() or {}
        
        # Build attendees
        attendees = []
        for a in data.get("attendees", []):
            attendees.append(Attendee(
                name=a.get("name", ""),
                company=a.get("company", ""),
                title=a.get("title"),
                extra_context=a.get("extra_context")
            ))
        
        # Build meeting request
        meeting_request = MeetingRequest(
            title=data.get("title", "Untitled Meeting"),
            meeting_type=data.get("meeting_type", "sales"),
            your_goal=data.get("your_goal", ""),
            your_name=data.get("your_name", "You"),
            your_company=data.get("your_company", "Your Company"),
            duration_minutes=data.get("duration_minutes", 60),
            attendees=attendees,
            extra_context=data.get("extra_context")
        )
        
        # Generate briefing
        agent = MeetingMindAgent()
        briefing_result = agent.prepare_briefing(meeting_request)
        
        # Convert to dict
        import dataclasses
        result = dataclasses.asdict(briefing_result)
        
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        import traceback
        error_response = jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        })
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500
