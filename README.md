
# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

The following is actual output from running `python main.py`:

```text
TODAY'S SCHEDULE (SORTED BY TIME)
-------------------------------------------------------
2026-10-18 07:00 | Luna   | Breakfast       | High
2026-10-18 08:00 | Buddy  | Morning walk    | High
2026-10-18 09:00 | Buddy  | Medication      | High
2026-10-18 09:00 | Luna   | Grooming        | Low

HIGH-PRIORITY TASKS FIRST
-------------------------------------------------------
2026-10-18 07:00 | Luna   | Breakfast       | High
2026-10-18 08:00 | Buddy  | Morning walk    | High
2026-10-18 09:00 | Buddy  | Medication      | High
2026-10-18 09:00 | Luna   | Grooming        | Low

BUDDY'S TASKS
-------------------------------------------------------
2026-10-18 08:00 | Buddy  | Morning walk    | High
2026-10-18 09:00 | Buddy  | Medication      | High

SCHEDULING CONFLICTS
WARNING: Buddy and Luna have tasks at 09:00

Recurring task created: Morning walk on 2026-10-19
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output from `python -m pytest`:

```text
collected 7 items

tests\test_pawpal.py ...........                     [100%]
=================== 11 passed in 0.09s ===================
```

The eleven tests verify task completion, task addition, chronological sorting across pets, filtering, overlapping and non-overlapping scheduling, duration persistence and legacy JSON compatibility, daily recurrence, and priority-based scheduling.

**Confidence level: 4/5.** All eleven tests passed, including overlap boundaries and legacy JSON compatibility.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | Sorts tasks chronologically or by High, Medium, Low priority, then time. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by pet name or completion status. |
| Conflict handling | `Scheduler.detect_conflicts()` | Detects overlapping task intervals across pets. |
| Recurring tasks | `Scheduler.handle_recurrence()` | Creates the next daily or weekly task when an existing task is completed. |

The Scheduler retrieves tasks from `Owner.get_all_tasks()`, allowing its algorithms to operate across multiple pets.

Tasks default to a duration of 20 minutes. Task durations are saved with the schedule, used to detect overlapping intervals, and default to 20 minutes when loading older JSON files.


**JSON Persistence:** PawPal+ uses `storage.py` to save owner information, pets, and tasks to `pawpal_data.json`. The application automatically loads saved data when a new session starts and saves changes when pets or tasks are added or completed. The JSON file is excluded from GitHub using `.gitignore`. Saving and loading pets were verified across an application restart, and task data was verified in the JSON file.

## 📸 Demo Walkthrough


1. Launch the Streamlit app using `python -m streamlit run app.py`.
2. Enter the owner's name and add pets, such as Luna (cat) and Mochi (dog).
3. Add care tasks with a description, due date, time, priority, and frequency.
4. Select sorting by Time or Priority, optionally filter by pet or completion status, and click **Generate schedule**.
5. Review the generated schedule. Tasks with overlapping intervals produce a conflict warning.
6. Select a pending task and click **Mark Complete**. Daily or weekly tasks automatically generate their next occurrence.

The browser demonstration confirmed that multiple pets could be added and simultaneous tasks triggered a scheduling conflict warning.

**Screenshot or video (optional):** Not included; the walkthrough and CLI output document the demonstrated functionality.
