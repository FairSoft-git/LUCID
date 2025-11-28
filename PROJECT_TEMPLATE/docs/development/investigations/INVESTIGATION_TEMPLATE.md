# Problem Investigation Template

Use this template to document significant issues, bugs, or outages.
Copy this file to `docs/development/investigations/INV-NNNN-short-title.md`.

---

# INV-NNNN: [Short Title]

## Status
[Draft | Review | Complete]

## Date
YYYY-MM-DD

## Authors
[List of contributors]

## 1. Problem Summary
**What happened?**
Briefly describe the issue, its impact, and severity.
*Example: The scraper failed for 4 hours, resulting in 50 missing cards.*

## 2. Context & Lead-up
**What was the sequence of events?**
Describe the state of the system before the problem occurred and what triggered it.
*Example: A new set code was added to the configuration, but the URL pattern matcher wasn't updated.*

## 3. Root Cause Analysis (The 5 Whys)
Drill down to the fundamental cause.

1.  **Why?** [First level cause]
2.  **Why?** [Second level cause]
3.  **Why?** [Third level cause]
4.  **Why?** [Fourth level cause]
5.  **Why?** [Root cause]

## 4. Investigation Findings
Detail the technical evidence found during debugging.
- Logs
- Error messages
- Code snippets
- Data inconsistencies

## 5. Corrective Actions
What will be done to fix this and prevent recurrence?

| Action Item | Type | Owner | Status |
|-------------|------|-------|--------|
| [Fix the bug] | Fix | LF | [Pending] |
| [Add a test case] | Prevention | LF | [Pending] |
| [Update documentation] | Process | LF | [Pending] |

## 6. Lessons Learned
**What went well?**
*Example: The alerting system notified us immediately.*

**What could be improved?**
*Example: The error logs were too verbose to find the root cause quickly.*

## Related Decisions (ADRs)
- [Link to relevant ADRs if this investigation leads to architectural changes]
