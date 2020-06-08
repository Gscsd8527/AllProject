from datetime import timedelta, datetime
from pandas import to_datetime

date = datetime.now().strftime('%Y%m%d')
date = to_datetime(date, format='%Y%m%d')
date_begin = date - timedelta(weeks=1) - timedelta(days=date.dayofweek)
date_end = date - timedelta(days=date.dayofweek)
date_begin = date_begin.strftime("%Y%m%d")
date_end = date_end.strftime("%Y%m%d")
print('date= ', date)
print('date_begin= ', date_begin)
print('date_end= ', date_end)

