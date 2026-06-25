import pytest
from pathlib import Path
from fastapi import status
from app.database.seed_all import DatabaseSeeder

@pytest.fixture(autouse=True)
def seed_test_db(db):
    data_dir = Path(__file__).parent.parent / "app" / "database" / "data"
    seeder = DatabaseSeeder(db, data_dir)
    seeder.seed_all(include_matrix=False)

class TestExcersiceCatalog:

    def test_list_levels(self, client):
        resp = client.get("/api/v1/excersices/levels")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 4
        assert any(item["code"] == "NIV1" for item in data)

    def test_list_goals(self, client):
        resp = client.get("/api/v1/excersices/goals")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 4
        assert any(item["code"] == "PG" for item in data)

    def test_list_conditions(self, client):
        resp = client.get("/api/v1/excersices/conditions")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 25
        assert any(item["code"] == "PAT001" for item in data)
        assert any(item["code"] == "ENF001" for item in data)

    def test_list_methods(self, client):
        resp = client.get("/api/v1/excersices/methods")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 30
        assert any(item["code"] == "FMT001" for item in data)
        assert any(item["code"] == "MET001" for item in data)

    def test_list_excersices_no_filters(self, client):
        resp = client.get("/api/v1/excersices/")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 214

    def test_list_excersices_filtered_by_muscle_group(self, client):
        resp = client.get("/api/v1/excersices/?muscle_group=Pecho")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert all(item["muscle_group"] == "Pecho" for item in data)

    def test_list_excersices_filtered_by_goal(self, client):
        resp = client.get("/api/v1/excersices/?goal_code=GMM")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for item in data:
            assert any(g["code"] == "GMM" for g in item["goals"])

    def test_list_excersices_exclude_forbidden_conditions(self, client):
        # Sentadilla Trasera (PIE001) has PAT002 (Hernia Discal) as FORBIDDEN.
        # Let's verify that PIE001 is present when not excluding conditions,
        # but is absent when excluding PAT002.
        
        # 1. Without exclusions
        resp1 = client.get("/api/v1/excersices/")
        data1 = resp1.json()
        assert any(item["code"] == "PIE001" for item in data1)

        # 2. Excluding PAT002 (Hernia Discal)
        resp2 = client.get("/api/v1/excersices/?exclude_conditions=PAT002")
        data2 = resp2.json()
        assert not any(item["code"] == "PIE001" for item in data2)
