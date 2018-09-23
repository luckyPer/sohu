import time

def get_time():
    data = time.strftime("%Y-%m-%d", time.localtime())
    return data
