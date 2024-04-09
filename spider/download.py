import csv
import datetime
import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import csv
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.visualization import ImageNormalize, SqrtStretch
import sunpy.coordinates  # NOQA
import sunpy.map
import drms
from sunpy.net import Fido, jsoc
from sunpy.net import attrs as a

if __name__ == '__main__':
    with open('output.csv', 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            print(row)
            time = '{}-{}-{}T{}:{}:00'.format(row['Date'][0:4], row['Date'][4:6], row['Date'][6:8], row['Time'][0:2],
                                              row['Time'][3:5])
            start_time = Time(time, scale='utc', format='isot')
            start_time_0 = start_time - 12 * u.h
            start_time_1 = start_time - 24 * u.h
            start_time_2 = start_time - 48 * u.h
            e = '211250228@smail.nju.edu.cn'
            res1_0 = Fido.search(a.Time(start_time_0 - 0.5 * u.h, start_time_0 + 0.5 * u.h),
                                 a.jsoc.Series('hmi.B_720s'), a.jsoc.Notify(e))  # 12h前hmi.B_720s
            file_download = Fido.fetch(res1_0)
            # files1_0 = Fido.fetch(res1_0)
            # res1_1 = Fido.search(a.Time(start_time_1 - 0.5 * u.h, start_time_1 + 0.5 * u.h),
            #                      a.jsoc.Series('hmi.B_720s'), a.jsoc.Notify(e))  # 24h前hmi.B_720s
            # files1_1 = Fido.fetch(res1_1)
            # res1_2 = Fido.search(a.Time(start_time_2 - 0.5 * u.h, start_time_2 + 0.5 * u.h),
            #                      a.jsoc.Series('hmi.B_720s'), a.jsoc.Notify(e))  # 48h前hmi.B_720s
            # files1_2 = Fido.fetch(res1_2)