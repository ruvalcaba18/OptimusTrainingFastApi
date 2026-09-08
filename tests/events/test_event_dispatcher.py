from app.events.dispatcher import EventDispatcher
from app.events.domain.routine_generated_event import RoutineGeneratedEvent
from app.events.domain.user_registered_event import UserRegisteredEvent
from app.events.domain.workout_completed_event import WorkoutCompletedEvent


def test_user_registered_event_dispatch():
    dispatcher = EventDispatcher()
    received = []

    def sample_handler(event: UserRegisteredEvent):
        received.append(event)

    dispatcher.subscribe(UserRegisteredEvent, sample_handler)

    event = UserRegisteredEvent(
        user_id=1,
        email="test@uabc.edu.mx",
        first_name="Test",
        last_name="User",
    )
    dispatcher.dispatch(event)

    assert len(received) == 1
    assert received[0].user_id == 1
    assert received[0].email == "test@uabc.edu.mx"
    assert received[0].event_name == "UserRegisteredEvent"


def test_routine_generated_event_dispatch():
    dispatcher = EventDispatcher()
    received = []

    def sample_handler(event: RoutineGeneratedEvent):
        received.append(event)

    dispatcher.subscribe(RoutineGeneratedEvent, sample_handler)

    event = RoutineGeneratedEvent(
        user_id=42,
        weeks_count=4,
        trigger_source="onboarding",
    )
    dispatcher.dispatch(event)

    assert len(received) == 1
    assert received[0].user_id == 42
    assert received[0].weeks_count == 4


def test_handler_error_isolation():
    dispatcher = EventDispatcher()
    results = []

    def failing_handler(event: WorkoutCompletedEvent):
        raise ValueError("Simulated handler crash")

    def successful_handler(event: WorkoutCompletedEvent):
        results.append("success")

    dispatcher.subscribe(WorkoutCompletedEvent, failing_handler)
    dispatcher.subscribe(WorkoutCompletedEvent, successful_handler)

    event = WorkoutCompletedEvent(user_id=10, week=1, day=2, exercise_count=5)

    # Debería capturar la excepción y permitir que los demás handlers continúen
    dispatcher.dispatch(event)

    assert results == ["success"]
