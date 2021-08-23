from datetime import datetime as dt, timedelta

FEDERAL_HOLIDAYS = [dt(2021,9,6), dt(2021,10,11), dt(2021,11,11), dt(2021, 11, 25), dt(2021,12,24), dt(2022,1,1), dt(2022,1,17), dt(2022,5,30), dt(2022,7,4), dt(2022,9,5)]
VALID_STATUS = ['pending', 'approved', 'rejected']
VALID_MGT_STATUS = ['pending', 'approved']

# Calculates number of work days used
def work_days_used(start, end):
    day_incrementor = start
    days_used = 0
    for _ in range((end - start).days):
        if day_incrementor.weekday() < 5 and day_incrementor not in FEDERAL_HOLIDAYS:
            days_used += 1

            day_incrementor += timedelta(days=1)
    return days_used