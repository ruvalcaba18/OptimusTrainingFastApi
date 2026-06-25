import pytest
from pathlib import Path
from fastapi import status
from app.models import UserProfile
from app.models import Level
from app.models import Goal
from app.models import Condition
from app.models import Equipment
from app.database.seed_all import DatabaseSeeder

@pytest.fixture(autouse=True)
def seed_test_db(db):
    data_dir = Path(__file__).parent.parent / "app" / "database" / "data"
    seeder = DatabaseSeeder(db, data_dir)
    seeder.seed_all(include_matrix=True)

def test_generate_routine_without_profile(client, auth_headers):
    resp = client.post("/api/v1/routines/generate", headers=auth_headers)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "perfil" in resp.json()["error"]["message"].lower()

def test_generate_routine_with_basic_profile(client, db, test_user, auth_headers):
    goal = db.query(Goal).filter(Goal.code == "PG").first()
    level = db.query(Level).filter(Level.code == "NIV1").first()
    
    profile = UserProfile(
        id=test_user.id,
        goal_id=goal.id,
        level_id=level.id,
        age=25,
        weight=70.0,
        height=170.0
    )
    db.add(profile)
    
    mancuernas = db.query(Equipment).filter(Equipment.name == "Mancuernas").first()
    if mancuernas:
        test_user.equipments.append(mancuernas)
    barra = db.query(Equipment).filter(Equipment.name == "Barra").first()
    if barra:
        test_user.equipments.append(barra)
    
    db.commit()
    
    resp = client.post("/api/v1/routines/generate", headers=auth_headers)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["goal"] == goal.name
    assert data["level"] == level.name
    assert data["sets"] == 3 
    assert data["reps"] == "12-15 reps"
    assert len(data["exercises"]) > 0

    for ex in data["exercises"]:
        assert ex["complexity"] in ["Baja", "Baja-Media", "Media", "Media-Alta", "Alta"]

def test_generate_routine_excludes_forbidden_conditions(client, db, test_user, auth_headers):
    goal = db.query(Goal).filter(Goal.code == "PG").first()
    level = db.query(Level).filter(Level.code == "NIV1").first()
    
    profile = UserProfile(
        id=test_user.id,
        goal_id=goal.id,
        level_id=level.id,
        age=25,
        weight=70.0,
        height=170.0
    )
    db.add(profile)
    

    hernia = db.query(Condition).filter(Condition.code == "PAT002").first()
    if hernia:
        test_user.pathologies.append(hernia)
        

    all_equip = db.query(Equipment).all()
    test_user.equipments.extend(all_equip)
    
    db.commit()
    
    resp = client.post("/api/v1/routines/generate", headers=auth_headers)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    exercises = data["exercises"]
    assert not any(ex["code"] == "PIE001" for ex in exercises)
