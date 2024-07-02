# app/db/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    link = Column(String, index=True)
    thumbnail = Column(String, nullable=True)
    published = Column(DateTime)
    guid = Column(String, unique=True, index=True)
    feed_id = Column(Integer)
    summary = Column(Text, nullable=True)
    likes = Column(Integer, default=0, nullable=True)
    views = Column(Integer, default=0, nullable=True)

    job_tags = relationship("ItemJobTag", back_populates="item")
    skill_tags = relationship("ItemSkillTag", back_populates="item")


class ItemJobTag(Base):
    __tablename__ = "item_job_tags"

    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    job_tag_id = Column(Integer, primary_key=True)

    item = relationship("Item", back_populates="job_tags")

    __table_args__ = (PrimaryKeyConstraint("item_id", "job_tag_id"),)


class ItemSkillTag(Base):
    __tablename__ = "item_skill_tags"

    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    skill_tag_id = Column(Integer, primary_key=True)

    item = relationship("Item", back_populates="skill_tags")

    __table_args__ = (PrimaryKeyConstraint("item_id", "skill_tag_id"),)
