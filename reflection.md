
# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design uses four Python classes:

- **Owner:** Stores owner information, manages multiple pets, and retrieves tasks across all pets.
- **Pet:** Stores pet information and manages its assigned care tasks.
- **Task:** Represents a care activity, including its description, due date/time, frequency, priority, and completion status.
- **Scheduler:** Organizes tasks across multiple pets using sorting, filtering, recurring schedules, and conflict detection.

**Relationships:** One Owner can have multiple Pets, and each Pet can have multiple Tasks. The Scheduler accesses the Owner's combined task list.

**Core user actions:** Add a pet, schedule a care task, and view an organized daily schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I refined my initial design during implementation rather than changing its four-class structure.

Priority was already included in the initial UML design. During implementation, I developed the `sort_by_priority()` method to organize tasks by High, Medium, and Low priority, using due time to break ties.

I also used Python dataclasses for `Owner`, `Pet`, and `Task` to simplify initialization and reduce repetitive code.

These refinements made the scheduler more practical while preserving the original object-oriented design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers task due dates/times, priority levels, pet identity, completion status, and recurrence frequency.

Time matters because care tasks must be completed on schedule. Priority helps identify urgent activities, such as medication. Filtering allows owners to focus on individual pets or unfinished tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Conflict detection identifies tasks with identical due times rather than calculating overlapping durations. This approach is simple, readable, and sufficient to demonstrate basic scheduling conflicts.

However, tasks starting at different times could still overlap. Duration-aware conflict detection would improve a future version.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used ChatGPT to help design the UML diagram, implement the four Python classes, develop scheduling algorithms, create automated tests, and integrate the backend with Streamlit.

The most useful requests specified the required classes, their relationships, expected methods, and the grading criteria.

Separating design, implementation, testing, and UI integration into distinct steps helped keep the development process organized.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I requested that the Streamlit implementation preserve CodePath's original `app.py` structure rather than replacing the starter interface entirely. The revised approach retained the original sections while integrating the working backend.

I also chose to preserve CodePath's README structure and replace its placeholders instead of rewriting the entire document.

I verified the generated code by running `python main.py`, executing seven pytest tests, and manually testing multi-pet management and conflict detection in Streamlit.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I created seven automated tests covering:

1. Task completion.
2. Adding tasks to pets.
3. Sorting tasks across multiple pets.
4. Filtering tasks by pet.
5. Detecting scheduling conflicts.
6. Creating the next daily recurring task.
7. Sorting tasks by priority.

All seven tests passed. I also ran the CLI demonstration and tested the Streamlit interface with Luna and Mochi.

These tests verify that the classes work together and that the scheduler handles multiple pets correctly.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

**Confidence: 4/5.** All seven automated tests passed, and the demonstrated Streamlit features worked.

Additional tests should cover pets without tasks, weekly recurrence, invalid inputs, duplicate task descriptions, overlapping durations, and persistence after restarting the application.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with connecting the object-oriented Python backend to a functioning Streamlit interface. The same Scheduler methods work in both the CLI demonstration and browser application.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add JSON persistence, duration-aware conflict detection, task editing, and additional automated edge-case tests. These improvements would make PawPal+ more useful beyond a single browser session.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that AI can accelerate system design and implementation, but the developer must still define requirements, evaluate suggestions, test behavior, and make final design decisions.

Designing the UML first, keeping the backend separate from the UI, and verifying functionality before integration made the project easier to understand and debug.
