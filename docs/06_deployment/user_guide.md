# Руководство пользователя

## Установка
1. Установить Python 3.9 или новее.
2. Клонировать репозиторий: `git clone <адрес репозитория>`.
3. Перейти в каталог проекта.

## Команды
| Команда | Назначение |
|---|---|
| `python3 -m src.brs.cli rating data/sample.json --group "ИЗДт 23.1"` | рейтинг группы |
| `python3 -m src.brs.cli stats data/sample.json --group "ИЗДт 23.1" --discipline PD` | статистика по дисциплине |
| `python3 -m src.brs.cli risk data/sample.json --group "ИЗДт 23.1"` | студенты с риском неаттестации |
| `python3 -m src.brs.cli score data/sample.json s4 PD exam 25` | выставить балл |
