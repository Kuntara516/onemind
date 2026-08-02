from app.vector_store.models import VectorRecord
from app.vector_store.service import VectorStoreService


def test_vector_store_service_add_and_get():
    service = VectorStoreService()

    record = VectorRecord(
        id="vec-service-001",
        collection="knowledge",
        vector=[0.1, 0.2, 0.3],
    )

    service.add(record)

    result = service.get("vec-service-001")

    assert result is not None
    assert result.id == "vec-service-001"


def test_vector_store_service_delete():
    service = VectorStoreService()

    service.add(
        VectorRecord(
            id="vec-service-002",
            vector=[0.1],
        )
    )

    service.delete("vec-service-002")

    assert service.get("vec-service-002") is None


def test_vector_store_service_search():
    service = VectorStoreService()

    service.add(
        VectorRecord(
            id="vec-service-003",
            vector=[0.1, 0.2],
        )
    )

    results = service.search([0.1, 0.2])

    assert len(results) == 1
    assert results[0].id == "vec-service-003"