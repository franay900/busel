import calendar
from datetime import datetime, timedelta

def get_all_weeks(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    one_day, one_week = timedelta(days=1), timedelta(days=7)
    days=timedelta(days=8-1)
    current_week_start = calendar.Calendar().monthdatescalendar(start_date.year, start_date.month)[0][0]
    while True:
        if current_week_start + one_week <= start_date:
            current_week_start += one_week
            continue
        if current_week_start > end_date:
            break
        yield [current_week_start.strftime('%d.%m.%Y'), (current_week_start + one_week - one_day).strftime('%d.%m.%Y')]
        current_week_start += one_week
def get_dates(start,end):
    d1 = datetime.strptime(start, '%d.%m.%Y').date()
    d2 = datetime.strptime(end, '%d.%m.%Y').date()
    arr=[]
    arr2=[]
    delta = d2 - d1         # timedelta
    if delta.days<=0:
        print ("Ругаемся и выходим")

    a1 = []
    for j in range(delta.days + 1):
        date=d1 + timedelta(j)
        a1.append(date)
    return a1

