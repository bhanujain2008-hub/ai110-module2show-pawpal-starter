
import json
from datetime import datetime
from pathlib import Path

from pawpal_system import Owner, Pet, Task


DATA_FILE = Path(__file__).with_name("pawpal_data.json")


def save_data(owner):
    """Save the owner, pets, and tasks to a JSON file."""
    data = {
        "owner": owner.name,
        "pets": [
            {
                "name": pet.name,
                "species": pet.species,
                "tasks": [
                    {
                        "description": task.description,
                        "due_time": task.due_time.isoformat(),
                        "frequency": task.frequency,
                        "completed": task.completed,
                        "priority": task.priority,
                        "duration_minutes": task.duration_minutes,
                    }
                    for task in pet.tasks
                ],
            }
            for pet in owner.pets
        ],
    }

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data():
    """Load previously saved pets and tasks from JSON."""
    if not DATA_FILE.exists():
        return Owner("Jordan")

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    owner = Owner(data.get("owner", "Jordan"))

    for pet_data in data.get("pets", []):
        pet = Pet(
            name=pet_data["name"],
            species=pet_data["species"],
        )

        for task_data in pet_data.get("tasks", []):
            task = Task(
                description=task_data["description"],
                due_time=datetime.fromisoformat(task_data["due_time"]),
                frequency=task_data.get("frequency", "once"),
                completed=task_data.get("completed", False),
                priority=task_data.get("priority", "Medium"),
                duration_minutes=task_data.get("duration_minutes", 20),
            )
            pet.add_task(task)

        owner.add_pet(pet)

    return owner
