
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler
from storage import load_data, save_data


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


def test_overlapping_tasks_conflict():
    owner, dog, cat, scheduler = make_schedule()
    dog.add_task(Task("Walk", datetime(2026, 10, 18, 9), duration_minutes=30))
    cat.add_task(Task("Feed", datetime(2026, 10, 18, 9, 20)))
    assert len(scheduler.detect_conflicts()) == 1


def test_non_overlapping_tasks_do_not_conflict():
    owner, dog, cat, scheduler = make_schedule()
    dog.add_task(Task("Walk", datetime(2026, 10, 18, 9), duration_minutes=20))
    cat.add_task(Task("Feed", datetime(2026, 10, 18, 9, 20)))
    assert scheduler.detect_conflicts() == []


def test_storage_saves_and_loads_task_duration(tmp_path, monkeypatch):
    import storage

    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "pawpal_data.json")
    owner, dog, _, _ = make_schedule()
    dog.add_task(Task(
        "Walk", datetime(2026, 10, 18, 9), duration_minutes=45
    ))

    save_data(owner)

    loaded_owner = load_data()
    assert loaded_owner.pets[0].tasks[0].duration_minutes == 45


def test_storage_defaults_duration_for_existing_data(tmp_path, monkeypatch):
    import storage

    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "pawpal_data.json")
    storage.DATA_FILE.write_text(
        '{"owner":"Alex","pets":[{"name":"Buddy","species":"Dog",'
        '"tasks":[{"description":"Walk","due_time":"2026-10-18T09:00:00"}]}]}',
        encoding="utf-8",
    )

    loaded_owner = load_data()
    assert loaded_owner.pets[0].tasks[0].duration_minutes == 20


def test_daily_recurrence():
    owner, dog, cat, scheduler = make_schedule()
    task = Task(
        "Walk", datetime(2026, 10, 18, 8),
        frequency="daily", duration_minutes=40
    )
    dog.add_task(task)
    next_task = scheduler.handle_recurrence(dog, task)
    assert task.completed is True
    assert next_task.due_time == task.due_time + timedelta(days=1)
    assert len(dog.tasks) == 2
    assert next_task.duration_minutes == 40


def test_priority_scheduling():
    owner, dog, cat, scheduler = make_schedule()
    dog.add_task(Task("Groom", datetime(2026, 10, 18, 7),
                      priority="Low"))
    cat.add_task(Task("Medicine", datetime(2026, 10, 18, 9),
                      priority="High"))
    assert scheduler.sort_by_priority()[0][1].description == "Medicine"
