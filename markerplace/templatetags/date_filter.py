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


#[{'order_detail_id': '1', 'type': '1', 'status': '1',
# 'created_at': '2019-12-13T08:19:15+01:00', 'updated_at': '2019-12-13T08:19:15+01:00'}]
def detail_filter(value):
    ls = ''
    for li in value:
        upd_date = datetime.datetime.strptime(li['updated_at'], "%Y-%m-%dT%H:%M:%S+01:00")
        cre_date = datetime.datetime.strptime(li['created_at'], "%Y-%m-%dT%H:%M:%S+01:00")
        ls += f"detail_id:{li['order_detail_id']};type:{li['type']};status:{li['status']}" \
              f"\ncreated_at:{cre_date}\nupdated_at:{upd_date}\n\n"
    return ls


def id_strip(value):
    new = value.replace(' ', '').strip()
    return new
# too('2019-12-10T02:27:19+01:00')

register.filter(too)

register.filter(detail_filter)

register.filter(id_strip)