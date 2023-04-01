from datetime import datetime

date = '05-04-1994'

datetime_ = datetime.strptime(date, '%d-%m-%Y').date()

print(datetime_)