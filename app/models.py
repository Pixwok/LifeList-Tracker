from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base

# Gestion des tables

class Goals(Base):
    __tablename__ = "objectifs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    advancement: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    statut: Mapped[bool] = mapped_column(Boolean, default=False)
    deadline: Mapped[date] = mapped_column(Date, nullable=True)
    categorie_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    categorie: Mapped["Categories"] = relationship("Categories", back_populates="goals") #Synchro entre categories et objectifs
    task: Mapped[list["Task"]] = relationship("Task", back_populates= "objectif") #Syncrho entre task et objectifs

class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)

    goals: Mapped[list["Goals"]] = relationship("Goals", back_populates="categorie") #Synchro entre objectif et objectifs

class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    statut: Mapped[bool] = mapped_column(Boolean, default=False)
    deadline: Mapped[date] = mapped_column(Date, nullable=True)
    objectif_id: Mapped[int] = mapped_column(ForeignKey("objectifs.id"), nullable=False)

    objectif: Mapped[Goals] = relationship("Goals", back_populates="task") #Synchro entre task et objectifs
