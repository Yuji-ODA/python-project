import timeit
from datetime import date, timedelta
from annotated_types import Len
from typing import Annotated, Sequence


def last_weekday(base: date, weekday_num: int) -> date:
    return base - timedelta(days=(base.weekday() - weekday_num - 1) % 7 + 1)

def last_monday(base: date) -> date:
    return last_weekday(base, 0)

def first_weekday_of_month_before(base: date, weekday_num: int) -> date:
    monday = last_weekday(base, weekday_num)
    return monday if monday.day <= 7 else first_weekday_of_month_before(monday, weekday_num)

def first_monday_of_month_before(base: date) -> date:
    return first_weekday_of_month_before(base, 0)

def first_monday_of_month_before_1(base: date) -> date:
    day_of_prev_monday = base.day - base.weekday()
    last_monday_in_this_month = 0 < base.day - ((base.weekday() - 1) % 7 + 1)
    days_of_prev_month = 0 if last_monday_in_this_month else (base - timedelta(days=base.day)).day
    return base - timedelta(days=base.weekday() + (day_of_prev_monday + days_of_prev_month - 1) // 7 * 7)


if __name__ == '__main__':
    dates = [date(2015, 1, 1) + timedelta(days=i) for i in range(10_000)]

    print(timeit.timeit('list(map(first_monday_of_month_before, dates))', number=100, globals=globals()))
    print(timeit.timeit('list(map(first_monday_of_month_before_1, dates))', number=100, globals=globals()))

    r = list(map(first_monday_of_month_before, dates))
    r1 = list(map(first_monday_of_month_before_1, dates))

    print(r == r1)

    print(last_weekday(date.today(), 3))

    print(last_monday(date.today()))

    l: Annotated[Sequence[float], Len[2]] = (1,2,2)

    x = 'hoge'
