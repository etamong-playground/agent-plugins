---
name: nextjs-playwright-e2e
description: Add deterministic browser tests to a Next.js and Auth.js app with isolated synthetic authentication and representative backend behavior.
---

# Browser tests for Next.js and Auth.js

Inspect the current framework, authentication version, session strategy, scripts and test setup before changing it.
Reuse repository conventions and verify current configuration against the installed packages and official documentation.

1. Select a user-visible behavior and define its success and failure results independently of the implementation.
   Use a dedicated local test server, synthetic data and a test-only authentication secret.
   Never reuse production credentials, cookies, databases or identity providers.
2. Choose authentication compatible with the app's actual strategy.
   A synthetic session may use a test helper or the installed library's supported encoding API, but its cookie name, salt, claims and callbacks must match the test app.
   Do not assume that JWT encoding works for database sessions or every Auth.js version.
   Keep any test-only bypass unavailable in production.
3. Store generated browser state in an ignored test directory and treat it as sensitive even when synthetic.
   Mock backend responses at a seam the browser actually uses; server-side requests need a server fixture or isolated test backend.
   Fail unexpected backend calls instead of returning a successful catch-all response that conceals missing coverage.
4. Assert visible results, state changes, authentication denial and relevant error states.
   A synthetic-cookie suite does not verify real sign-in, refresh, logout or identity-provider integration; state that boundary and use separate authorized tests for those flows.
5. Stabilize clock, fixtures, fonts, animations and viewport for visual tests.
   Generate baselines in the same pinned environment as CI and review image changes deliberately.
   Use the repository's required/advisory policy rather than making visual tests advisory by default.
6. Run the actual project scripts locally and in PR CI, with matching package/browser versions and frozen dependency installation.
   A production build and server are appropriate when testing production behavior.

Example: “Test that an authenticated user saves a draft and sees a retryable failure when saving fails.”
The test must distinguish saved state from a mocked click, and show that unauthenticated access is denied.
Never put credentials into Docker command arguments, Git URL rewrites or committed browser state.
