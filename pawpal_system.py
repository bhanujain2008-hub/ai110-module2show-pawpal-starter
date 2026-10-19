
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


@dataclass
class Task:
    description: str
    due_time: datetime
    frequency: str = "once"
    completed: bool = False
    priority: str = "Medium"
    duration_minutes: int = 20

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task to this pet."""
        self.tasks.append(task)

    def list_tasks(self):
        """Return this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return tasks across all pets."""
        return [
            (pet, task)
            for pet in self.pets
            for task in pet.tasks
        ]


class Scheduler:
    def __init__(self, owner: Owner):
        """Manage the owner's combined pet schedule."""
        self.owner = owner

    def sort_by_time(self):
        """Sort all pet tasks chronologically."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda item: item[1].due_time
        )

    def filter_tasks(self, pet_name=None, completed=None):
        """Filter tasks by pet name or completion status."""
        tasks = self.owner.get_all_tasks()

        if pet_name is not None:
            tasks = [
                (pet, task) for pet, task in tasks
                if pet.name.lower() == pet_name.lower()
            ]

        if completed is not None:
            tasks = [
                (pet, task) for pet, task in tasks
                if task.completed == completed
            ]

        return tasks

    def detect_conflicts(self):
        """Find tasks whose scheduled time intervals overlap."""
        tasks = self.sort_by_time()
        conflicts = []

        for i in range(len(tasks)):
            task1 = tasks[i][1]
            task1_end = task1.due_time + timedelta(
                minutes=task1.duration_minutes
            )

            for j in range(i + 1, len(tasks)):
                task2 = tasks[j][1]
                if task2.due_time >= task1_end:
                    break
                conflicts.append((tasks[i], tasks[j]))

        return conflicts

    def handle_recurrence(self, pet: Pet, task: Task):
        """Complete a task and schedule its next occurrence."""
        task.mark_complete()

        intervals = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1)
        }

        interval = intervals.get(task.frequency.lower())

        if interval is None:
            return None

        next_task = Task(
            description=task.description,
            due_time=task.due_time + interval,
            frequency=task.frequency,
            priority=task.priority,
            duration_minutes=task.duration_minutes
        )
        pet.add_task(next_task)
        return next_task

    def sort_by_priority(self):
        """Sort tasks by priority, then due time."""
        priority_order = {"High": 0, "Medium": 1, "Low": 2}

        return sorted(
            self.owner.get_all_tasks(),
            key=lambda item: (
                priority_order.get(item[1].priority, 1),
                item[1].due_time
            )
        )
