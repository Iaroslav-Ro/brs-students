"""Расчет итоговых баллов, оценок, рейтинга и статистики."""
from typing import Dict, List, Tuple

from .models import Journal

GRADE_SCALE = (
    (85, "отлично"),
    (70, "хорошо"),
    (50, "удовлетворительно"),
    (0, "неудовлетворительно"),
)
PASS_SCORE = 50


def grade(total: float) -> str:
    """Перевод итогового балла (0–100) в оценку."""
    for threshold, name in GRADE_SCALE:
        if total >= threshold:
            return name
    return GRADE_SCALE[-1][1]


def total_score(journal: Journal, student_id: str, discipline_code: str) -> float:
    """Итоговый балл студента по дисциплине, приведенный к 100-балльной шкале."""
    discipline = journal.disciplines[discipline_code]
    earned = sum(journal.scores.get((student_id, discipline_code, c.code), 0)
                 for c in discipline.checkpoints)
    if discipline.max_total == 0:
        return 0.0
    return round(earned / discipline.max_total * 100, 1)


def group_rating(journal: Journal, group: str) -> List[Tuple[int, str, float]]:
    """Рейтинг группы: (место, ФИО, средний итоговый балл по всем дисциплинам)."""
    rows = []
    for student in journal.group_students(group):
        totals = [total_score(journal, student.id, code)
                  for code in journal.disciplines]
        average = round(sum(totals) / len(totals), 1) if totals else 0.0
        rows.append((student.name, average))
    rows.sort(key=lambda row: (-row[1], row[0]))
    rating, place = [], 0
    for index, (name, average) in enumerate(rows, start=1):
        if index == 1 or average != rows[index - 2][1]:
            place = index
        rating.append((place, name, average))
    return rating


def discipline_stats(journal: Journal, discipline_code: str, group: str) -> Dict[str, float]:
    """Статистика по дисциплине для группы."""
    totals = [total_score(journal, s.id, discipline_code)
              for s in journal.group_students(group)]
    if not totals:
        return {"count": 0, "average": 0.0, "min": 0.0, "max": 0.0, "pass_rate": 0.0}
    passed = sum(1 for value in totals if value >= PASS_SCORE)
    return {
        "count": len(totals),
        "average": round(sum(totals) / len(totals), 1),
        "min": min(totals),
        "max": max(totals),
        "pass_rate": round(passed / len(totals) * 100, 1),
    }


def at_risk(journal: Journal, group: str) -> List[Tuple[str, str, float]]:
    """Студенты, у которых итоговый балл по дисциплине ниже проходного."""
    result = []
    for student in journal.group_students(group):
        for code, discipline in journal.disciplines.items():
            total = total_score(journal, student.id, code)
            if total < PASS_SCORE:
                result.append((student.name, discipline.title, total))
    return result
