/**
 * Vercel Serverless Function - Node.js version
 * Calls Grok API directly
 */

const { OpenAI } = require('openai');

const SYSTEM_PROMPT = `You are MeetingMind AI — an elite meeting preparation agent.

Generate a complete meeting briefing with the following sections:
1. Attendee Profiles - psychological/professional profiles with interests, pain points, conversation hooks, preparation tips
2. Strategic Agenda - time-boxed agenda items
3. Talking Points - specific tactics and phrases
4. Predicted Q&A - 5 hard questions with battle-tested answers
5. Pre-Meeting Checklist - 8-10 actionable tasks

Return valid JSON matching this structure:
{
  "executive_summary": "3-sentence summary",
  "readiness_score": 85,
  "attendee_profiles": [
    {
      "name": "...",
      "company": "...",
      "inferred_role": "...",
      "likely_interests": [...],
      "likely_pain_points": [...],
      "conversation_hooks": [...],
      "preparation_tips": [...]
    }
  ],
  "agenda": [
    {
      "time_slot": "0:00-5m",
      "title": "...",
      "description": "...",
      "owner": "You/Them/Both",
      "key_objective": "..."
    }
  ],
  "talking_points": ["point 1", "point 2", ...],
  "predicted_qa": [
    {
      "question": "...",
      "suggested_answer": "...",
      "confidence": "high|medium|low"
    }
  ],
  "pre_meeting_checklist": [
    {
      "task": "...",
      "priority": "high|medium|low",
      "deadline": "...",
      "estimated_minutes": 15
    }
  ]
}`;

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { title, meeting_type, your_goal, attendees, extra_context } = req.body;

    if (!process.env.XAI_API_KEY) {
      return res.status(500).json({ error: 'XAI_API_KEY not configured' });
    }

    // Initialize Grok client (OpenAI compatible)
    const client = new OpenAI({
      apiKey: process.env.XAI_API_KEY,
      baseURL: 'https://api.x.ai/v1'
    });

    // Build type-specific guidance
    const typeGuidance = {
      'sales': 'Focus on closing strategies, objection handling, competitor differentiation, and ROI proof points.',
      'investor': 'Focus on traction, market size, team credentials, financial projections, and exit potential.',
      'hiring': 'Focus on candidate assessment, company culture selling, role expectations, and career growth.',
      'partnership': 'Focus on mutual benefits, collaboration models, resource sharing, and long-term value.',
      'product': 'Focus on user needs, feature prioritization, technical feasibility, and roadmap alignment.',
      'client': 'Focus on relationship building, understanding pain points, delivering value, and renewal/expansion.'
    };

    const userPrompt = `Generate a meeting briefing for:

Title: ${title || 'Untitled Meeting'}
Type: ${meeting_type || 'sales'}
Goal: ${your_goal || 'Not specified'}
Attendees: ${attendees?.map(a => `${a.name} (${a.company})`).join(', ') || 'None'}
Context: ${extra_context || 'None provided'}

IMPORTANT: This is a ${meeting_type || 'general'} meeting. ${typeGuidance[meeting_type] || typeGuidance['sales']}

Make the Q&A specifically relevant to this meeting type. Do NOT use generic sales questions for interviews - use interview-appropriate questions instead.

Return ONLY valid JSON.`;

    const response = await client.chat.completions.create({
      model: 'grok-2-latest',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: userPrompt }
      ],
      max_tokens: 4000,
      temperature: 0.7
    });

    const content = response.choices[0].message.content;
    
    // Extract JSON from response
    let jsonStr = content;
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      jsonStr = jsonMatch[0];
    }
    
    const briefingData = JSON.parse(jsonStr);

    // Add metadata
    const result = {
      meeting_request: {
        title: title || 'Untitled Meeting',
        meeting_type: meeting_type || 'sales',
        your_goal: your_goal || '',
        attendees: attendees || [],
        extra_context: extra_context || ''
      },
      ...briefingData,
      generated_at: new Date().toISOString()
    };

    return res.status(200).json(result);

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({
      error: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
};
