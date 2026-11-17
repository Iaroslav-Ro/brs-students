"""Классы предметной области."""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Student:
    id: str
    name: str
    group: str


@dataclass(frozen=True)
class Checkpoint:
    code: str
    title: str
    max_score: float


@dataclass
class Discipline:
    code: str
    title: str
    checkpoints: List[Checkpoint] = field(default_factory=list)

    def checkpoint(self, code: str) -> Checkpoint:
        for item in self.checkpoints:
            if item.code == code:
                return item
        raise KeyError(f"Контрольная точка {code!r} не найдена в дисциплине {self.code!r}")

    @property
    def max_total(self) -> float:
        return sum(item.max_score for item in self.checkpoints)


@dataclass
class Journal:
    """Журнал БРС: студенты, дисциплины и выставленные баллы."""

    students: Dict[str, Student] = field(default_factory=dict)
    disciplines: Dict[str, Discipline] = field(default_factory=dict)
    scores: Dict[Tuple[str, str, str], float] = field(default_factory=dict)

    def add_student(self, student: Student) -> None:
        if student.id in self.students:
            raise ValueError(f"Студент {student.id!r} уже есть в журнале")
        self.students[student.id] = student

    def add_discipline(self, discipline: Discipline) -> None:
        if discipline.code in self.disciplines:
            raise ValueError(f"Дисциплина {discipline.code!r} уже есть в журнале")
        self.disciplines[discipline.code] = discipline

    def set_score(self, student_id: str, discipline_code: str,
                  checkpoint_code: str, value: float) -> None:
        if student_id not in self.students:
            raise KeyError(f"Студент {student_id!r} не найден")
        if discipline_code not in self.disciplines:
            raise KeyError(f"Дисциплина {discipline_code!r} не найдена")
        checkpoint = self.disciplines[discipline_code].checkpoint(checkpoint_code)
        if not 0 <= value <= checkpoint.max_score:
            raise ValueError(
                f"Балл {value} вне диапазона 0–{checkpoint.max_score} "
                f"для контрольной точки {checkpoint_code!r}")
        self.scores[(student_id, discipline_code, checkpoint_code)] = value

    def group_students(self, group: str) -> List[Student]:
        return sorted((s for s in self.students.values() if s.group == group),
                      key=lambda s: s.name)
