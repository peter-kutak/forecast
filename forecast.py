from datetime import datetime
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("Europe/Bratislava"))

import xml.etree.ElementTree as ET
import requests
res = requests.get('https://www.shmu.sk/sk/?page=1&id=meteo_num_alad&mesto=POV.BYSTRICA&jazyk=en')

print(res)
inblock = False
block = ""
for line in res.text.splitlines():
  if "MAINCONTENT" in line:
    inblock = not inblock
  if inblock:
    block = block + "\n" + line
#print(block)

#root = ET.fromstring(block)
#f=root.findall(".//*[@id='maincontent']/section/pre[1]")
#print(f)

import re

inforecast = False
findex = 0
forecast = {}
forecast[0] = {}
for line in block.splitlines():
  #if inforecast and "pre" in line:
  #  break
  if "Forecast" in line:
    inforecast = True
  if inforecast:
    #forecast = forecast + "\n" + line
    if m := re.match(r".*Forecast for  (\w+)  (\d{2}\.\d{2}\.\d{4}) .*", line):
      fdate = datetime.strptime(m.group(2), "%d.%m.%Y")
      fdate = fdate.replace(tzinfo=ZoneInfo("Europe/Bratislava"))
      findex = - int((now - fdate).total_seconds()//(24*60*60))
      forecast[findex] = {}
      forecast[findex]["date"] = m.group(2)
      #forecast[findex]["datetime"] = fdate
    if m := re.match(r".*Morning .* (-?\d+) .*", line):
      min_temp = m.group(1)
      forecast[findex]["min_temp"] = min_temp
    if m := re.match(r".*Maximum .* (-?\d+) .*", line):
      max_temp = m.group(1)
      forecast[findex]["max_temp"] = max_temp

print(forecast)

from PublishFrcs import PublishFrcs

p=PublishFrcs()

hr = now.hour
therm = float(forecast[0]["max_temp"])
if hr < 8:
  therm = float(forecast[0]["min_temp"])
if hr > 18:
  #poobede uz davam zajtrajsiu predpoved
  therm = float(forecast[1]["min_temp"])
p.publish(therm)


