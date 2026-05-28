Design a polished public-facing AI companion for the book *Language landscapes* by Brett Reynolds.

You are not designing a generic chatbot. You are designing a serious, elegant reading-and-learning companion for a 532-page book on English grammar, usage, discourse, and language teaching.

Use the uploaded brief and references as the source of truth.

Goals:

1. Create a responsive mock-up for a public-facing product that helps readers explore the book by asking questions, browsing chapters, and inspecting cited source passages.
2. Make the interface feel warm, intelligent, literary, and trustworthy rather than corporate or “AI startup.”
3. Treat citations, chapter structure, and retrieved passages as core parts of the experience.
4. Keep the design implementable later as a Claude Artifact with no traditional backend.

Please produce:

1. A primary landing page plus in-product experience.
2. A desktop view and a mobile view.
3. At least these states:
   - landing page before asking anything
   - active chat with answer and citations
   - source-inspection state showing retrieved passages
   - chapter-browsing state
   - empty or no-match state
4. A cohesive design system:
   - type choices
   - color system
   - spacing
   - button/input styles
   - cards or panels
5. Short rationale for the visual direction.

Functional expectations:

- Users can ask questions about the book.
- Answers should appear with visible citations by chapter/section.
- Retrieved source cards should be inspectable.
- Users should be able to browse chapters even if they do not know what to ask.
- The interface should suggest question types like explain, compare, where is this covered, or quiz me.

Visual direction:

- Avoid purple-heavy AI tropes.
- Avoid looking like a CRM, analytics dashboard, or enterprise admin tool.
- Aim for something between a beautifully designed digital book companion and a scholarly field notebook.
- Use typography intentionally.
- Light mode is the default.
- Make it feel crafted, not template-driven.

Important implementation guardrails:

- Assume no traditional backend in v1.
- Assume the app will later run as a Claude Artifact.
- Do not rely on custom user accounts, payments, or private server-side storage.
- Do not assume external third-party API calls.
- Keep the interaction model compatible with a local corpus embedded in the app.

Prioritize the reading companion and chat experience over flashy product marketing.
