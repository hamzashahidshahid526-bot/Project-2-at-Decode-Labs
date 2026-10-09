from sqlalchemy import Column, Integer, String, CheckConstraint
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)  # UNIQUE + NOT NULL = Vault Gatekeeper
    age = Column(Integer, nullable=False)  # NOT NULL

    # Schema Level Constraints - The Immune System
    __table_args__ = (
        CheckConstraint('age >= 0', name='check_age_non_negative'),
    )
