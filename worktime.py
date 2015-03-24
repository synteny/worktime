#!/usr/bin/python

import requests
import datetime
import os
import ConfigParser


def btrx_format(iso_format):
    tmp = iso_format.split("-")
    bf = tmp[2] + "." + tmp[1] + "." + tmp[0]
    return bf

current_date = datetime.date.today()
exclude_dates = {datetime.date(current_date.year, 2, 23),
                 datetime.date(current_date.year, 3, 9),
                 datetime.date(current_date.year, 5, 1),
                 datetime.date(current_date.year, 5, 4),
                 datetime.date(current_date.year, 5, 11),
                 datetime.date(current_date.year, 11, 4),
                 datetime.date(current_date.year, 12, 31)}

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(os.getenv('HOME'), ".worktime")))

url = "https://portal.biocad.ru/work_time/index.php"

general = dict(config.items('GENERAL'))
userid = general['userid']
username = general['username']
password = general['password']

params = {"ajaxToAddData": "yes"}

projects = config.items('PROJECTS')
for project, time in projects:
    params.update({"tm[{0}][{1}]".format(userid, project): "{}:00".format(time)})

current_date = datetime.date.today()
start_date = current_date.replace(day=1)

for single_date in (start_date + datetime.timedelta(n) for n in range((current_date-start_date).days+1)):
    if single_date.weekday() not in (5, 6) and single_date not in exclude_dates:
        current_params = params.copy()
        current_params.update({"date": btrx_format(single_date.isoformat())})
        auth = requests.post(url, params=current_params, auth=(username, password))