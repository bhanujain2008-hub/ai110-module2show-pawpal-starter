
# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used GitHub Copilot in VS Code Agent mode to improve the existing PawPal+ project by adding task durations and detecting overlapping scheduled tasks.

I instructed the agent to:

1. Add `duration_minutes` to the `Task` class, defaulting to 20 minutes.
2. Update `Scheduler.detect_conflicts()` to detect overlapping task intervals, not just identical start times.
3. Update `app.py` to store the duration entered by the user.
4. Update `storage.py` to save and load durations while preserving compatibility with older JSON files.
5. Add pytest tests for overlapping and non-overlapping tasks.
6. Update the final UML diagram.
7. Preserve all existing functionality, class names, and the original Streamlit layout.
8. Run `python -m pytest` and fix any failures.

I also required the agent to inspect existing files before editing, summarize its changes and test results, and avoid committing, pushing, or deleting files.

**What did the agent do?**

GitHub Copilot Agent inspected the existing project and modified six files:

| File | Changes |
|---|---|
| `pawpal_system.py` | Added `duration_minutes` with a 20-minute default, implemented interval-overlap detection, and preserved duration in recurring tasks. |
| `app.py` | Stored user-entered durations, displayed durations in the schedule, and improved conflict messages. |
| `storage.py` | Saved and loaded task durations, using a 20-minute default for older JSON records. |
| `tests/test_pawpal.py` | Added tests for overlaps, non-overlaps, persistence, and legacy-data compatibility. |
| `diagrams/uml_final.mmd` | Added the duration attribute to the Task class. |
| `README.md` | Updated the documentation to describe duration-aware conflict detection. |

The agent preserved existing local changes, including JSON persistence, and installed a missing pytest dependency in its execution environment.

**What did you have to verify or fix manually?**

I reviewed and approved the agent's requests to run terminal commands and perform Python analysis.

During execution, Copilot encountered temporary test-discovery and Pylance tool errors. It subsequently verified the implementation through terminal commands.

**Automated verification reported by Copilot:**

- `python -m pytest`: **11 tests passed**.
- Python compilation: Passed.
- `git diff --check`: Passed.
- No files were committed, pushed, or deleted.

**Manual verification:**

- Previously ran the CLI demonstration and verified the original seven automated tests.
- Tested the Streamlit application with multiple pets and simultaneous tasks.
- Verified that JSON persistence saved pet and task information.
- Restarted Streamlit and confirmed that saved pet information was restored.
- Confirmed that `pawpal_data.json` was excluded from Git using `git check-ignore -v pawpal_data.json`.
- Tested duration-aware conflict detection in the Streamlit browser:
  - Feeding: 10:00 AM, 30 minutes, ending at 10:30 AM.
  - Medication: 10:15 AM, 20 minutes, ending at 10:35 AM.
  - The application correctly displayed a conflict warning.
- Inspected `pawpal_data.json` and confirmed that the tasks retained their respective `duration_minutes` values of 30 and 20.

**Outcome:** GitHub Copilot Agent completed a genuine autonomous, multi-file development workflow. The updated scheduler detects overlapping time intervals, the automated test suite increased from seven to eleven passing tests, and the new behavior was verified in the browser and saved JSON data.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

**Task compared:** Recommend improvements to conflict detection in the existing PawPal+ scheduler.

I tested two prompts in separate GitHub Copilot chats using Ask mode. Both prompts addressed the same existing project. Neither modified project files.

| | Option A | Option B |
|---|---|---|
| **Model / tool used** | GitHub Copilot (Ask mode) | GitHub Copilot (Ask mode) |
| **Prompt** | Suggest how to improve conflict detection in my PawPal+ Python project. | Review `pawpal_system.py` and `tests/test_pawpal.py` in my existing PawPal+ project. Recommend exactly three improvements to `Scheduler.detect_conflicts()` that preserve its current behavior: overlapping intervals conflict, but tasks meeting exactly at an endpoint do not. For each improvement, explain the problem, propose a specific solution, and suggest one pytest test. Do not modify any files. |
| **Response summary** | Suggested six improvements: duration validation, completed-task handling, clearer overlap warnings, conflict scope, edge-case tests, and a sweep-line algorithm. | Suggested three improvements: reject invalid durations, validate mixed timezone awareness, and use an active-set sweep algorithm. Each included a problem, solution, and proposed pytest test. |
| **What was useful** | Identified a broad range of practical usability, correctness, and performance improvements. | Produced focused, technically specific recommendations with corresponding tests. |
| **Problems noticed** | Recommendations were broader and did not consistently include a concrete test for each change. | Excluded some useful UI and completed-task considerations because the prompt limited the response to three improvements. |
| **Decision** | Useful for brainstorming and identifying future enhancements. | Preferred for planning precise, testable implementation changes. |

**Which approach did you use in your final implementation and why?**

I preferred **Option B: specific, constrained prompting** for planning improvements because it:

- Identified the exact source and test files.
- Preserved the existing interval-overlap and endpoint rules.
- Limited the response to three focused improvements.
- Required a concrete solution and pytest test for each recommendation.
- Explicitly prevented file modifications.

Option A was valuable for brainstorming a wider range of enhancements, including usability considerations that Option B did not cover.

The comparison also reinforced the value of the detailed prompt used in SF7. That prompt specified the files to modify, the required behavior, compatibility constraints, testing expectations, and restrictions on Git operations.

**Conclusion:** Broad prompts are useful for exploring possibilities, while specific prompts produce more structured, actionable, and testable recommendations.

**Implementation status:** The SF11 recommendations were evaluated but not implemented during the comparison. The existing duration-aware scheduling implementation remained unchanged.
