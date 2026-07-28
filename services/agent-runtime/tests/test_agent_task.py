from app.tasks import AgentTask, TaskStatus


def test_create_agent_task():
    task = AgentTask(
        task_id="task_001",
        agent_id="assistant-agent",
        intent="system_health_check",
    )

    assert task.task_id == "task_001"
    assert task.agent_id == "assistant-agent"
    assert task.intent == "system_health_check"


def test_default_task_status_is_created():
    task = AgentTask(
        task_id="task_002",
        agent_id="assistant-agent",
        intent="test",
    )

    assert task.status == TaskStatus.CREATED


def test_task_serialization():
    task = AgentTask(
        task_id="task_003",
        agent_id="assistant-agent",
        intent="serialization_test",
    )

    data = task.model_dump()

    assert data["task_id"] == "task_003"
    assert data["status"] == TaskStatus.CREATED


def test_required_fields_validation():
    try:
        AgentTask(
            task_id="task_004",
            intent="missing_agent",
        )
        assert False

    except Exception:
        assert True