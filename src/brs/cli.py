"""Интерфейс командной строки программы «БРС-Студент»."""
import argparse

from . import analysis, storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="brs", description="Учет и анализ балльно-рейтинговой системы студентов")
    sub = parser.add_subparsers(dest="command", required=True)

    rating = sub.add_parser("rating", help="рейтинг группы")
    rating.add_argument("file")
    rating.add_argument("--group", required=True)

    stats = sub.add_parser("stats", help="статистика по дисциплине")
    stats.add_argument("file")
    stats.add_argument("--group", required=True)
    stats.add_argument("--discipline", required=True)

    risk = sub.add_parser("risk", help="студенты с риском неаттестации")
    risk.add_argument("file")
    risk.add_argument("--group", required=True)

    score = sub.add_parser("score", help="выставить балл")
    score.add_argument("file")
    score.add_argument("student")
    score.add_argument("discipline")
    score.add_argument("checkpoint")
    score.add_argument("value", type=float)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    journal = storage.load(args.file)
    if args.command == "rating":
        print(f"Рейтинг группы {args.group}")
        for place, name, average in analysis.group_rating(journal, args.group):
            print(f"{place:>2}. {name:<32} {average:>5}  {analysis.grade(average)}")
    elif args.command == "stats":
        stats = analysis.discipline_stats(journal, args.discipline, args.group)
        print(f"Дисциплина: {journal.disciplines[args.discipline].title}")
        print(f"Студентов: {stats['count']}, средний балл: {stats['average']}, "
              f"минимум: {stats['min']}, максимум: {stats['max']}, "
              f"успевающих: {stats['pass_rate']} %")
    elif args.command == "risk":
        rows = analysis.at_risk(journal, args.group)
        if not rows:
            print("Студентов с риском неаттестации нет")
        for name, title, total in rows:
            print(f"{name:<32} {title:<36} {total:>5}")
    elif args.command == "score":
        journal.set_score(args.student, args.discipline, args.checkpoint, args.value)
        storage.save(journal, args.file)
        print("Балл сохранен")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
