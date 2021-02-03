def convert_time_to_s(time):
    unit = time[-1]
    seconds = {"s": 1, "m": 60, "h": 3600}
    if unit.isalpha():
        return int(time[:-1]) * seconds[unit]

    return int(time)
