
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def make_schedule():
    owner = Owner("Alex")
    dog = Pet("Buddy", "Dog")
    cat = Pet("Luna", "Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat, Scheduler(owner)


def test_task_completion():
    task = Task("Walk", datetime(2026, 10, 18, 8))
    task.mark_complete()
    assert task.completed is True


def test_task_addition():
    pet = Pet("Buddy", "Dog")
    pet.add_task(Task("Feed", datetime(2026, 10, 18, 7)))
    assert len(pet.tasks) == 1


def test_sorting_across_pets():
    owner, dog, cat, scheduler = make_schedule()
    dog.add_task(Task("Walk", datetime(2026, 10, 18, 9)))
    cat.add_task(Task("Feed", datetime(2026, 10, 18, 7)))
    assert [task.description for _, task in scheduler.sort_by_time()] == [
        "Feed", "Walk"
    ]


def test_filtering():
    owner, dog, cat, scheduler = make_schedule()
    dog.add_task(Task("Walk", datetime(2026, 10, 18, 9)))
    cat.add_task(Task("Feed", datetime(2026, 10, 18, 7)))
    assert len(scheduler.filter_tasks(pet_name="Buddy")) == 1


def test_conflict_detection():
    owner, dog, cat, scheduler = make_schedule()
    same_time = datetime(2026, 10, 18, 9)
    dog.add_task(Task("Walk", same_time))
    cat.add_task(Task("Feed", same_time))
    assert len(scheduler.detect_conflicts()) == 1


def test_daily_recurrence():
    owner, dog, cat, scheduler = make_schedule()
    task = Task("Walk", datetime(2026, 10, 18, 8), frequency="daily")
    dog.add_task(task)
    next_task = scheduler.handle_recurrence(dog, task)
    assert task.completed is True
    assert next_task.due_time == task.due_time + timedelta(days=1)
    assert len(dog.tasks) == 2


def test_priority_scheduling():
    owner, dog, cat, scheduler = make_schedule()
    dog.add_task(Task("Groom", datetime(2026, 10, 18, 7),
                      priority="Low"))
    cat.add_task(Task("Medicine", datetime(2026, 10, 18, 9),
                      priority="High"))
    assert scheduler.sort_by_priority()[0][1].description == "Medicine"
