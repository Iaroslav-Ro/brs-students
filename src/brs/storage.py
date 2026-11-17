"""Загрузка и сохранение журнала в файл JSON."""
import json
from pathlib import Path
from typing import Union

from .models import Checkpoint, Discipline, Journal, Student


def load(path: Union[str, Path]) -> Journal:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    journal = Journal()
    for item in raw.get("students", []):
        journal.add_student(Student(item["id"], item["name"], item["group"]))
    for item in raw.get("disciplines", []):
        checkpoints = [Checkpoint(c["code"], c["title"], c["max_score"])
                       for c in item.get("checkpoints", [])]
        journal.add_discipline(Discipline(item["code"], item["title"], checkpoints))
    for item in raw.get("scores", []):
        journal.set_score(item["student"], item["discipline"],
                          item["checkpoint"], item["value"])
    return journal


def save(journal: Journal, path: Union[str, Path]) -> None:
    raw = {
        "students": [vars(s) for s in journal.students.values()],
        "disciplines": [
            {"code": d.code, "title": d.title,
             "checkpoints": [vars(c) for c in d.checkpoints]}
            for d in journal.disciplines.values()],
        "scores": [
            {"student": s, "discipline": d, "checkpoint": c, "value": v}
            for (s, d, c), v in journal.scores.items()],
    }
    Path(path).write_text(json.dumps(raw, ensure_ascii=False, indent=2),
                          encoding="utf-8")
