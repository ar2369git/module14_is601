# tests/integration/test_calculation_model.py

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.models.calculation import Calculation
from app.models.user import User  # new import

TEST_DB = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(
    TEST_DB,
    connect_args={"check_same_thread": False} if TEST_DB.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_calculation_insert(db_session):
    # create a dummy user so user_id FK is satisfied
    user = User(username="testuser", email="test@example.com", password_hash="fakehash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    from app.factory.calculation_factory import compute

    calc = Calculation(
        a=4.0,
        b=5.0,
        type="Add",
        result=compute("Add", 4, 5),
        user_id=user.id,      # supply user_id explicitly
    )
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    assert calc.result == 9
    assert calc.a == 4

def test_invalid_type(db_session):
    with pytest.raises(ValueError):
        from app.factory.calculation_factory import compute
        compute("Foo", 1, 1)
