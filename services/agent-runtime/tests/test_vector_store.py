from app.vector_store.memory import InMemoryVectorStore
from app.vector_store.models import VectorRecord


def test_add_and_get_vector_record():
    store = InMemoryVectorStore()

    record = VectorRecord(
        id="vec-001",
        collection="knowledge",
        vector=[0.1, 0.2, 0.3],
    )

    store.add(record)

    retrieved = store.get("vec-001")

    assert retrieved is not None
    assert retrieved.id == "vec-001"
    assert retrieved.collection == "knowledge"


def test_delete_vector_record():
    store = InMemoryVectorStore()

    record = VectorRecord(
        id="vec-001",
        vector=[0.1],
    )

    store.add(record)
    store.delete("vec-001")

    assert store.get("vec-001") is None


def test_search_returns_records():
    store = InMemoryVectorStore()

    store.add(
        VectorRecord(
            id="vec-001",
            vector=[0.1, 0.2],
        )
    )

    results = store.search([0.1, 0.2])

    assert len(results) == 1
    assert results[0].id == "vec-001"