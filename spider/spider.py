import datetime

import requests
from bs4 import BeautifulSoup
import re
import os


class Spider(object):
    def __init__(self):
        self.csv_path = ''
        self.URL = "https://solarmonitor.org/index.php"
        self.Parameter = {"date": "20160213", "type": "shmi_maglc", "indexnum": "1"}
        self.Header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}

    def set_date(self, date):
        self.Parameter['date'] = date

    def set_csv_path(self, path):
        self.csv_path = path
        with open(self.get_csv_path(), 'w+') as file:
            file.write("Date,NOAA_id,Latitude,Longitude,Area,Class,Time\n")

    def get_csv_path(self):
        return self.csv_path

    def get_today_date(self):
        return self.Parameter['date']

    def get_yesterday_date(self):
        year = int(self.Parameter['date'][:4])
        month = int(self.Parameter['date'][4:6])
        day = int(self.Parameter['date'][6:])
        today = datetime.date(year, month, day)
        yesterday = today + datetime.timedelta(days=-1)
        return str(yesterday).replace("-", '')

    def get_content(self):
        return BeautifulSoup(requests.get(self.URL, self.Parameter, headers=self.Header).text, 'html.parser')

    def save(self, doc):
        # with open("data/" + self.get_today_date()[:4] + ".csv", 'a+') as file:
        with open(self.get_csv_path(), 'a+') as file:
            for d in doc:
                line = ""
                for i in range(len(d)):
                    if i != len(d) - 1:
                        line += (d[i] + ",")
                    else:
                        if len(d[i]) != 0:
                            line += (d[i][0] + "," + d[i][1] + "\n")
                        else:
                            line += ("N" + "," + "N" + "\n")
                file.write(line)

    def get_data(self):
        contents = self.get_content().select('.noaaresults')
        for content in contents:
            # print(content.get_text())
            document = []
            number = content.find(id='noaa_number').a.string
            position = re.findall(r'-?\d+', content.find(id='position').get_text())[-2:]  # 使用的是下面的角秒形式
            area_raw = re.findall(r'^-?\d+', content.find(id='area').get_text().replace(' ', '').replace('\"',''))
            area = area_raw[0] if len(area_raw) != 0 else '0'  # 获取今日区域大小,如果不存在的话补0

            todays = []
            yesterdays = []

            for i in content.find(id='events'):
                # have flare
                if i.name == 'br':
                    continue
                if hasattr(i, 'a'):
                    try:
                        if i['style'] == 'color:#0000FF;':
                            text = i.get_text().replace(' ', '').replace("/", ''). \
                                replace("-", '').replace('\n', '')
                            if len(text) >= 10:
                                todays.append([text[0], text[5:10]])
                        if i['style'] == 'color:#58ACFA;':
                            text = i.get_text().replace(' ', '').replace("/", ''). \
                                replace("-", '').replace('\n', '')
                            if len(text) >= 10:
                                yesterdays.append([text[0], text[5:10]])
                    except KeyError:
                        print("Unparsable text,please contact TA(Text:", i.get_text())

            if len(todays) == 0:  # no flare
                todays.append(["N", "99:99"])
            for today in todays:
                document.append([self.get_today_date(), number, position[0], position[1], area, today])

            if len(yesterdays) != 0:
                for yesterday in yesterdays:
                    document.append([self.get_today_date(), number, position[0], position[1], area, yesterday])
            self.save(document)
            print(document)


def main(start_t, end_t):
    spider = Spider()
    start = datetime.date(*start_t)
    end = datetime.date(*end_t)

    assert (start <= end)
    csv_name = "data/" + str(start).replace("-", '') + '-' + str(end).replace("-", '') + '.csv'
    spider.set_csv_path(csv_name)

    while start != end:
        spider.set_date(str(start).replace("-", ''))
        try:
            spider.get_data()
        except requests.exceptions.ConnectionError:
            print("Retry!")
            continue
        start = start + datetime.timedelta(days=1)


if __name__ == '__main__':
    start_time = (1996, 11, 28)
    end_time = (2024, 3, 20)
    main(start_time, end_time)
