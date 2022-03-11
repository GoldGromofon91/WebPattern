import datetime
from pytz import timezone

TIMEZONE = 'Europe/Moscow'


def FC_server_date(request):
    request['SERVER_DATE_TIME'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return request


def FC_current_date(request):
    zone = TIMEZONE
    request['CURRENT_DATE_TIME'] = datetime.datetime.now(timezone(zone)).strftime("%Y-%m-%d %H:%M:%S")
    return request


if __name__ == "__main__":
    request = {}
    FC_current_date(request)
    FC_server_date(request)
    print(request)
