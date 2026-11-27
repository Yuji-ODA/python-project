from datetime import date, timedelta


def last_monday(base: date) -> date:
    return base - timedelta(days=(base.weekday() - 1) % 7 + 1)


def first_monday_of_month_before(base: date) -> date:
    if base.weekday() == 0 and base.day < 7:
        return base
    else:
        monday = last_monday(base)
        return monday if monday.day <= 7 else first_monday_of_month_before(monday)


if __name__ == '__main__':
    print(first_monday_of_month_before(date(2025, 4, 6)))
