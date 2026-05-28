# Technical Guardrails

This mock-up is intended to migrate later into Claude Artifacts.

Design accordingly.

## Practical constraints

- No traditional backend in the first public version.
- Retrieval corpus can be embedded locally in the app.
- Current corpus export is about 1.1 MB as `book_chunks.jsonl`.
- The app should not depend on external third-party API calls.
- Do not assume custom authentication.
- Do not assume a private database.

## Artifact-specific constraints from Anthropic docs

- AI-powered artifacts can call a limited text-based Claude capability.
- Shared artifacts do not charge the creator for other users’ AI usage.
- Artifacts can be published publicly.
- Advanced AI-powered capabilities require the viewer to sign in to Claude.
- External services are possible through MCP, but each user must authenticate independently.
- Persistent storage exists, but should be treated as optional and minimal in this project.

## What this means for design

Good fits:

- embedded corpus
- in-browser retrieval
- answer + citation workflow
- source drawer / source cards
- chapter browsing
- prompt suggestions

Bad fits for v1:

- collaborative editing
- shared annotations across users
- personalized dashboards
- server-side saved histories
- heavy account settings flows
- upload-and-index arbitrary user documents

## Current implementation model

The current local prototype already has:

- a conversation pane
- a source rail
- local retrieval over `book_chunks.jsonl`
- optional model generation

The redesign should improve the product expression and UX, not invent an entirely different system.

## Implementation target after Design

After the mock-up phase, the likely build target is:

- Claude Artifact
- local corpus included in the artifact
- retrieval done in the artifact client logic
- Claude used only for answer synthesis and follow-up prompting

Design for that reality.
