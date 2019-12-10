from django import template  # 关键代码
import datetime

register = template.Library()


# (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
# 2019-12-10T02:27:19+01:00
def too(value):
    st = value.split('+')[0]
    dates = datetime.datetime.strptime(st, "%Y-%m-%dT%H:%M:%S")
    value = (dates + datetime.timedelta(hours=+7)).strftime("%Y-%m-%d %H:%M:%S")
    return value


# too('2019-12-10T02:27:19+01:00')

register.filter(too)


