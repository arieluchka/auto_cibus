from datetime import datetime, timezone, timedelta

def get_time_of_day(utc_offset: int = 3) -> str:
    tz = timezone(timedelta(hours=utc_offset))
    return datetime.now(tz=tz).strftime('%H:%M')


def check_if_workday():
    """
    0 Monday
    ...
    4 Friday
    5 Saturday
    6 Sunday
    """
    return datetime.now().weekday() not in [4, 5] # 0-4 represents Monday-Friday

if __name__ == '__main__':
    print(get_time_of_day())
    print(check_if_workday())