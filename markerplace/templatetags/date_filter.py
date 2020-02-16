from django import template  # 关键代码
import datetime

register = template.Library()


# (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
# 2019-12-10T02:27:19+01:00
def too(value):
    if value == '':
        return value
    st = value.split('+')[0]
    dates = datetime.datetime.strptime(st, "%Y-%m-%dT%H:%M:%S")
    value = (dates + datetime.timedelta(hours=+7)).strftime("%Y-%m-%d %H:%M:%S")
    return value


# [{'order_detail_id': '1', 'type': '1', 'status': '1',
# 'created_at': '2019-12-13T08:19:15+01:00', 'updated_at': '2019-12-13T08:19:15+01:00'}]
def detail_filter(value):
    ls = ''
    for li in value:
        upd = li['updated_at'].split('+')[0]
        cre = li['created_at'].split('+')[0]
        upd_date = datetime.datetime.strptime(upd, "%Y-%m-%dT%H:%M:%S")
        cre_date = datetime.datetime.strptime(cre, "%Y-%m-%dT%H:%M:%S")
        ls += f"detail_id:{li['order_detail_id']}type:{li['type']}\nstatus:{li['status']}" \
              f"\ncreated_at:{cre_date}\nupdated_at:{upd_date}\n\n"
    return ls


def id_strip(value):
    new = value.replace(' ', '').strip()
    return new


# too('2019-12-10T02:27:19+01:00')

def rep_none(value):
    if value is None:
        return ''
    return value


def page_h(value):
    if int(value) == 1:
        return 1
    value = int(value) - 1
    return value


def page_a(value):
    if value is None:
        return 2
    new_value = int(value) + 1
    return new_value


def de_none(value):
    if value is None:
        return ''
    return value


def id_num(value):
    if value == '' or value is None:
        return 1
    return value


register.filter(id_num)
register.filter(de_none)

register.filter(page_a)
register.filter(page_h)

register.filter(rep_none)
register.filter(too)

register.filter(detail_filter)

register.filter(id_strip)
