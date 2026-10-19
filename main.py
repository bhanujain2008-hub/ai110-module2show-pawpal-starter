
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Alex")
buddy = Pet("Buddy", "Dog")
luna = Pet("Luna", "Cat")

owner.add_pet(buddy)
owner.add_pet(luna)

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

buddy.add_task(Task("Morning walk", today + timedelta(hours=8),
                    frequency="daily", priority="High"))
luna.add_task(Task("Breakfast", today + timedelta(hours=7),
                   frequency="daily", priority="High"))
buddy.add_task(Task("Medication", today + timedelta(hours=9),
                    priority="High"))
luna.add_task(Task("Grooming", today + timedelta(hours=9),
                   priority="Low"))

scheduler = Scheduler(owner)

def display(title, items):
    print(f"\n{title}")
    print("-" * 55)
    for pet, task in items:
        print(f"{task.due_time:%Y-%m-%d %H:%M} | "
              f"{pet.name:6} | {task.description:15} | {task.priority}")

display("TODAY'S SCHEDULE (SORTED BY TIME)", scheduler.sort_by_time())
display("HIGH-PRIORITY TASKS FIRST", scheduler.sort_by_priority())
display("BUDDY'S TASKS", scheduler.filter_tasks(pet_name="Buddy"))

print("\nSCHEDULING CONFLICTS")
for first, second in scheduler.detect_conflicts():
    print(f"WARNING: {first[0].name} and {second[0].name} "
          f"have tasks at {first[1].due_time:%H:%M}")

next_task = scheduler.handle_recurrence(buddy, buddy.tasks[0])
print(f"\nRecurring task created: {next_task.description} "
      f"on {next_task.due_time:%Y-%m-%d}")
