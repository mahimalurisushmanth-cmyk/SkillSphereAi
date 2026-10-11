# SkillSphere AI — student learning web app

A responsive light-theme web prototype with:
- Dashboard and progress indicators
- Searchable/filterable learning hub with official resource links
- Study checklist, weekly routine, XP, and local progress persistence
- Editable career profile and milestone roadmap
- AI trends/resource freshness checklist (clearly marked as not live-crawled)
- Project studio with project status progression
- Fictional mentor cards; booking only records a local demo request
- AI study buddy backed by a real Gemini API request through a Python backend
- Responsive navigation and local-browser persistence

## Run on Windows

1. Install Python 3.10+ (3.11/3.12 recommended).
2. Open Command Prompt in the `skillsphere_ai` folder.
3. Create and activate a virtual environment:

   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r backend\requirements.txt
   ```

4. Configure your Gemini API key as a server environment variable. Get a key from Google AI Studio. Do not put it in `index.html` or commit it to Git.

   ```bat
   set GEMINI_API_KEY=YOUR_REAL_API_KEY
   set GEMINI_MODEL=gemini-2.5-flash
   ```

   These `set` values apply to the current Command Prompt only. For persistent setup, use Windows Environment Variables.

5. Start the server from the project root:

   ```bat
   python -m uvicorn backend.server:app --reload --host 127.0.0.1 --port 8000
   ```

6. Open `http://127.0.0.1:8000`. API health: `http://127.0.0.1:8000/api/health`; API docs: `http://127.0.0.1:8000/docs`.

If you start without `GEMINI_API_KEY`, the rest of the app works in demo mode and the AI panel explains that Gemini is not configured. The app does not fabricate an AI reply.

## Gemini integration notes

The backend sends a request to Google's Gemini `generateContent` endpoint and reads `GEMINI_API_KEY` only on the server. If your account does not have access to the default model, set `GEMINI_MODEL` to a model available to your API key. Check current model availability, API restrictions, quotas, and billing in Google AI Studio.

Official docs:
- https://ai.google.dev/gemini-api/docs/get-started
- https://ai.google.dev/gemini-api/docs/api-key

## Current prototype limitations (intentional transparency)

- Authentication is a UI structure only; it is not secure account registration/login.
- Student progress, profile, and resources are stored in `localStorage` in one browser. There is no shared database or cross-device sync.
- Mentor profiles are fictional; booking creates a local demo request and contacts nobody.
- Trend cards are sample topics with official source links, not live news. Freshness checkboxes are manual.
- Resource catalogue links are starter suggestions. Verify source dates, access, and current relevance.
- XP, streak, and progress are prototype gamification values, not verified study time or credentials.

Before production: add real authentication, a database, authorization rules, rate limiting, input/output safety, privacy controls, tests, and deployed HTTPS hosting. Consider Firebase AI Logic or a server-side Gemini integration for production; never expose an API key in browser code.
