# KatMoviesWorld AutoPilot — safe starter

This adds a research-only daily digest to the existing site repository. It does not change the live homepage or deploy new website content.

## Included
- Scheduled and manual GitHub Actions workflow.
- RSS headline collection into content/drafts for human review.
- ShrinkEarn API adapter and unit tests.

## Setup
1. Review this branch before merging.
2. Rotate the ShrinkEarn API key because the previous key was shared in chat. Store the replacement only as GitHub Actions secret SHRINKEARN_API_KEY.
3. Run Actions → Daily entertainment research digest → Run workflow.
4. Review generated drafts before publishing.

The workflow does not use the ShrinkEarn key yet. The adapter is available for later, controlled use. It does not promise clicks, traffic, or earnings. Never use it to link to unauthorized movie downloads or copyrighted files. GitHub Pages is static hosting; no secret belongs in public HTML or JavaScript.
