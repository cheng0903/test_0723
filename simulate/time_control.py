DAILY_TIME_ZONES = [
    (960, 1320, 'red', 'peak'),        # 16:00–22:00
    (540, 960, 'gold', 'semi-peak'),   # 09:00–16:00
    (1320, 1440, 'gold', 'semi-peak'), # 22:00–24:00
    (0, 540, 'lightgreen', 'off-peak') # 00:00–09:00
]

def get_time_period(minute_of_day):
    for start, end, _, label in DAILY_TIME_ZONES:
        if start <= minute_of_day < end:
            return label
    return 'off-peak'
