
import streamlit as st
from datetime import datetime, date, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, your smart pet care management system!

Plan daily routines, organize tasks by time or priority, detect
scheduling conflicts, and manage recurring activities for multiple pets.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner
plan care tasks for their pet(s) based on constraints like time,
priority, and preferences.

The scheduler organizes tasks across multiple pets.
"""
    )

with st.expander("What you need to build", expanded=False):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

# Keep the owner and pets in memory between Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.divider()

st.subheader("Quick Demo Inputs")

owner.name = st.text_input("Owner name", value=owner.name)

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add Pet")

    if add_pet:
        name = pet_name.strip()
        if not name:
            st.error("Please enter a pet name.")
        elif any(p.name.lower() == name.lower() for p in owner.pets):
            st.warning("This pet already exists.")
        else:
            owner.add_pet(Pet(name, species))
            st.success(f"{name} added successfully!")

if owner.pets:
    st.write("**Current pets:**", ", ".join(p.name for p in owner.pets))
else:
    st.info("Add a pet to start scheduling tasks.")

st.markdown("### Tasks")
st.caption("Add care tasks to your pet's schedule.")

if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet = st.selectbox(
            "Select pet", [pet.name for pet in owner.pets]
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input(
                "Duration (minutes)",
                min_value=1, max_value=240, value=20
            )
        with col3:
            priority = st.selectbox(
                "Priority", ["low", "medium", "high"], index=2
            )

        col4, col5 = st.columns(2)
        with col4:
            due_date = st.date_input("Due date", value=date.today())
        with col5:
            due_time = st.time_input("Due time", value=time(8, 0))

        frequency = st.selectbox(
            "Frequency", ["once", "daily", "weekly"]
        )

        add_task = st.form_submit_button("Add task")

        if add_task:
            if not task_title.strip():
                st.error("Please enter a task title.")
            else:
                pet = next(
                    p for p in owner.pets if p.name == selected_pet
                )
                task = Task(
                    description=task_title.strip(),
                    due_time=datetime.combine(due_date, due_time),
                    priority=priority.capitalize(),
                    frequency=frequency
                )
                pet.add_task(task)
                st.success(f"Task added for {pet.name}!")
                st.caption(f"Estimated duration: {duration} minutes")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule using the PawPal+ Scheduler class.")

sort_choice = st.radio(
    "Organize schedule by",
    ["Time", "Priority"],
    horizontal=True
)

pet_filter = st.selectbox(
    "Filter by pet",
    ["All pets"] + [pet.name for pet in owner.pets]
)

status_filter = st.selectbox(
    "Filter by status",
    ["All", "Pending", "Completed"]
)

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        tasks = (
            scheduler.sort_by_time()
            if sort_choice == "Time"
            else scheduler.sort_by_priority()
        )

        if pet_filter != "All pets":
            tasks = [
                (pet, task) for pet, task in tasks
                if pet.name == pet_filter
            ]

        if status_filter != "All":
            tasks = [
                (pet, task) for pet, task in tasks
                if task.completed == (status_filter == "Completed")
            ]

        rows = [
            {
                "Pet": pet.name,
                "Task": task.description,
                "Due": task.due_time.strftime("%Y-%m-%d %H:%M"),
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": "Complete" if task.completed else "Pending"
            }
            for pet, task in tasks
        ]

        if rows:
            st.table(rows)
            st.success(
                f"Schedule generated with {len(rows)} task(s), "
                f"ordered by {sort_choice.lower()}."
            )
        else:
            st.info("No tasks match the selected filters.")

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning(
                f"{len(conflicts)} scheduling conflict(s) detected!"
            )
            for (pet1, task1), (pet2, task2) in conflicts:
                st.write(
                    f"⚠️ {pet1.name}: {task1.description} and "
                    f"{pet2.name}: {task2.description} "
                    f"at {task1.due_time:%Y-%m-%d %H:%M}"
                )
        else:
            st.success("No scheduling conflicts detected.")

# Complete tasks and generate recurring occurrences.
pending_tasks = [
    (pet, task)
    for pet, task in owner.get_all_tasks()
    if not task.completed
]

if pending_tasks:
    st.divider()
    st.subheader("Complete a Task")

    task_options = {
        f"{index + 1}. {pet.name} — {task.description} "
        f"({task.due_time:%Y-%m-%d %H:%M})": (pet, task)
        for index, (pet, task) in enumerate(pending_tasks)
    }

    selected = st.selectbox(
        "Choose a task to complete",
        list(task_options.keys())
    )

    if st.button("Mark Complete"):
        pet, task = task_options[selected]
        next_task = scheduler.handle_recurrence(pet, task)

        if next_task:
            st.success(
                f"Completed! Next occurrence: "
                f"{next_task.due_time:%Y-%m-%d %H:%M}"
            )
        else:
            st.success("Task completed!")

        st.rerun()

