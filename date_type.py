#!/usr/bin/env python3
import datetime
from chinese_calendar import get_holiday_detail, is_workday

def get_date_type(date=None):
    if date is None:
        date = datetime.datetime.now().date()

    if is_workday(date):
        return 'workday'

    is_holiday, holiday_name = get_holiday_detail(date)
    
    if holiday_name is not None:
        return 'holiday'

    weekday = date.weekday()
    if weekday in (4, 5):
        return 'weekend'

    return 'workday'