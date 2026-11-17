import unittest

from src.brs import analysis
from src.brs.models import Checkpoint, Discipline, Journal, Student


def make_journal() -> Journal:
    journal = Journal()
    journal.add_student(Student("s1", "Алексеев А. А.", "Г-1"))
    journal.add_student(Student("s2", "Борисов Б. Б.", "Г-1"))
    journal.add_student(Student("s3", "Васильев В. В.", "Г-2"))
    journal.add_discipline(Discipline("D1", "Дисциплина 1", [
        Checkpoint("kt1", "Контрольная точка 1", 40),
        Checkpoint("exam", "Экзамен", 60),
    ]))
    journal.set_score("s1", "D1", "kt1", 40)
    journal.set_score("s1", "D1", "exam", 50)
    journal.set_score("s2", "D1", "kt1", 20)
    journal.set_score("s2", "D1", "exam", 20)
    return journal


class GradeTest(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(analysis.grade(100), "отлично")
        self.assertEqual(analysis.grade(85), "отлично")
        self.assertEqual(analysis.grade(84.9), "хорошо")
        self.assertEqual(analysis.grade(70), "хорошо")
        self.assertEqual(analysis.grade(50), "удовлетворительно")
        self.assertEqual(analysis.grade(49.9), "неудовлетворительно")


class JournalTest(unittest.TestCase):
    def test_total_score(self):
        journal = make_journal()
        self.assertEqual(analysis.total_score(journal, "s1", "D1"), 90.0)
        self.assertEqual(analysis.total_score(journal, "s2", "D1"), 40.0)

    def test_score_above_maximum_is_rejected(self):
        journal = make_journal()
        with self.assertRaises(ValueError):
            journal.set_score("s1", "D1", "kt1", 41)

    def test_group_rating(self):
        rating = analysis.group_rating(make_journal(), "Г-1")
        self.assertEqual(rating, [(1, "Алексеев А. А.", 90.0), (2, "Борисов Б. Б.", 40.0)])

    def test_discipline_stats(self):
        stats = analysis.discipline_stats(make_journal(), "D1", "Г-1")
        self.assertEqual(stats["average"], 65.0)
        self.assertEqual(stats["pass_rate"], 50.0)

    def test_at_risk(self):
        rows = analysis.at_risk(make_journal(), "Г-1")
        self.assertEqual(rows, [("Борисов Б. Б.", "Дисциплина 1", 40.0)])


if __name__ == "__main__":
    unittest.main()
