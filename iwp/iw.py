import numpy as np
from datetime import datetime
from math import sin, cos, pi
import pyrealsense2 as rs

from .classes.device_data import DeviceData
from .classes.device_setting_info import DeviceSettingInfo
from .classes.hit_area import HitArea
from .classes.movie_data import MovieData
from .classes.wait_movie_data import WaitMovieData

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class InteractiveWall():
    _mBGMId = ''
    _mMaxMovieCount = 3
    DEPTH_SENSOR_WIDTH = 640
    DEPTH_SENSOR_HEIGHT = 480
    DEFAULT_MAX_MOVIE_COUNT = 3
    SETTING_FILE_NAME = 'setting.txt'
    MOVIE_STATUS_KEY = '_status'
    MOVIE_START_KEY = '_play'
    MOVIE_STOP_KEY = '_stop'
    MOVIE_PAUSE_KEY = '_pause'
    AUDIO_STATUS_KEY = '_status'
    AUDIO_START_KEY = '_play'
    AUDIO_STOP_KEY = '_stop'
    AUDIO_PAUSE_KEY = '_pause'
    CHROMEDRIVER_PATH = '/home/nah/Worlplace/Nah/iwp/iwp/chromedriver'
    _mContentPath = None
    _mDeviceList = None
    _mContext = None
    _mIsUpdatingDeviceList = None
    _mMovieList = None
    _mDeviceSetting = None
    _mHitAreaIdList = None
    _mHitList = None
    _mCurrentHitList = None
    _mLastHitTime = None

    @staticmethod
    def run():
        InteractiveWall._mIsUpdatingDeviceList = False
        InteractiveWall._mDeviceList = []
        InteractiveWall._mDeviceSetting = []
        InteractiveWall._mMovieList = []

        try:
            with open('/home/nah/Worlplace/Nah/iwp/iwp/setting.txt', 'r') as f:
                line = f.readline()
                separator = ":"
                while line:
                    str_array = line.split(separator, 2)
                    if len(str_array) >= 2:
                        str = str_array[0]
                        if not(str == "content"):
                            if not(str == "max_movie_count"):
                                if not(str == "senser"):
                                    if not(str == "wait_movie"):
                                        if not(str == "movie"):
                                            if str == "bgm":
                                                InteractiveWall._mBGMId = str_array[1].strip(
                                                )
                                        else:
                                            str_array2 = str_array[1].strip().split(
                                                ',')
                                            if len(str_array2) >= 5:
                                                hit_area = HitArea()
                                                hit_area.movieId = str_array2[0].strip(
                                                )
                                                try:
                                                    hit_area.left = str_array2[1]
                                                    hit_area.top = str_array2[2]
                                                    hit_area.right = str_array2[3]
                                                    hit_area.bottom = str_array2[4]
                                                    InteractiveWall._mMovieList.append(
                                                        hit_area)
                                                except Exception as e:
                                                    print(
                                                        'Error at fifth block {0}'.format(e))

                                    else:
                                        str_array2 = str_array[1].strip().split(
                                            ',')
                                        if len(str_array2) >= 2:
                                            wait_movie_data = WaitMovieData()
                                            wait_movie_data.movieId = str_array2[0].strip(
                                            )
                                            try:
                                                wait_movie_data.wait_time = str_array2[1].strip(
                                                )
                                                InteractiveWall._mMovieList.append(
                                                    wait_movie_data)
                                            except Exception as e:
                                                print(
                                                    'Error at third block {0}'.format(e))
                                else:
                                    str_array2 = str_array[1].strip().split(
                                        ',')
                                    if len(str_array2) >= 7:
                                        device_setting_info = DeviceSettingInfo()
                                        device_setting_info.device_serial = str_array2[0].strip(
                                        )
                                        try:
                                            device_setting_info.touch_line = str_array2[1].strip(
                                            )
                                            device_setting_info.view_range = str_array2[2].strip(
                                            )
                                            device_setting_info.angle = str_array2[3].strip(
                                            )
                                            device_setting_info.reverse_flag = str_array2[4].strip(
                                            )
                                            device_setting_info.offset_left = str_array2[5].strip(
                                            )
                                            device_setting_info.offset_top = str_array2[6].strip(
                                            )
                                            InteractiveWall._mDeviceSetting.append(
                                                device_setting_info)
                                        except Exception as e:
                                            print(
                                                'Error at third block {0}'.format(e))
                            else:
                                try:
                                    InteractiveWall._mMaxMovieCount = str_array[1].strip(
                                    )
                                except Exception as e:
                                    print(
                                        'Error at second block {0}'.format(e))

                        else:
                            InteractiveWall._mContentPath = str_array[1].strip(
                            )
                    line = f.readline()
        except Exception as e:
            print(
                'Error at first block {0}'.format(e))
        InteractiveWall._mContext = rs.context()
        InteractiveWall._mContext.set_devices_changed_callback(
            InteractiveWall.on_sense_devices_changed)
        if len(InteractiveWall._mDeviceSetting) <= 0:
            input()
        else:
            InteractiveWall._mHitAreaIdList = []
            InteractiveWall._mHitList = []
            InteractiveWall._mCurrentHitList = []
            for i in range(len(InteractiveWall._mMovieList)):
                mMovie = InteractiveWall._mMovieList[i]
                InteractiveWall._mHitList.append(False)
                InteractiveWall._mCurrentHitList.append(False)
                if type(mMovie) == type(HitArea):
                    InteractiveWall._mHitAreaIdList.append(i)
            InteractiveWall._mLastHitTime = datetime.now()

            options = Options()
            options.add_argument('disable-infobars')
            driver = webdriver.Chrome(
                InteractiveWall.CHROMEDRIVER_PATH, chrome_options=options)
            driver.get('file://' + InteractiveWall._mContentPath)
            if InteractiveWall._mBGMId != "":
                driver.find_element_by_id(
                    InteractiveWall._mBGMId + "_play").click()

            while True:
                enumerator1 = enumerate(InteractiveWall._mHitAreaIdList)
                for i, current in enumerator1:
                    InteractiveWall._mCurrentHitList[current] = False
                    if current.device_serial in InteractiveWall._mDeviceList:
                        mDevice = InteractiveWall._mDeviceList[current.device_serial]
                        if mDevice.frame_wait(current.touch_line) and mDevice.is_update_frame_buffer():
                            for i in range(mDevice.width):
                                num1 = (
                                    mDevice.widh - i) / mDevice.width if current.reverse_flag != 0 else i / mDevice.width
                                num2 = current.angle - current.view_range / 2.0 + num1 * current.view_range
                                num3 = mDevice.distance[i]
                                if num3 > 0.0:
                                    num4 = num3 * \
                                        cos(num2*pi / 180.0) + \
                                        current.offset_left
                                    num5 = num3 * \
                                        sin(num2*pi / 180.0) + \
                                        current.offset_top
                                    for index, item in enumerator1:
                                        if not InteractiveWall._mCurrentHitList[item]:
                                            mMovie = InteractiveWall._mMovieList[item]
                                            if mMovie.left <= num4 and mMovie.top <= num5 and (num4 <= mMovie.right and num5 <= mMovie.bottom):
                                                InteractiveWall._mCurrentHitListp[current] = True
            flag = False
            num = 0
            for index, current in enumerator1:
                if InteractiveWall._mCurrentHitList[current]:
                    flag = True
            if flag:
                for i in range(len(InteractiveWall._mMovieList)):
                    mMovie = InteractiveWall._mMovieList[i]
                    if type(mMovie) == type(WaitMovieData):
                        if driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                            driver.find_element_by_id(
                                mMovie.movie_stop_key()).click()
                    elif driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                        ++num
            else:
                time_span = datetime.now - InteractiveWall._mLastHitTime
                for i in range(len(InteractiveWall._mMovieList)):
                    mMovie = InteractiveWall._mMovieList[i]
                    if type(mMovie) == type(WaitMovieData) and time_span >= mMovie.wait_time and driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                        driver.find_element_by_id(
                            mMovie.movie_start_key()).click()
            for index, current in enumerator1:
                if InteractiveWall._mCurrentHitList[current] != InteractiveWall._mHitList[current]:
                    mMovie = InteractiveWall._mMovieList[current]
                    InteractiveWall._mHitList[current] = InteractiveWall._mCurrentHitList[current]
                    if num < InteractiveWall._mMaxMovieCount and InteractiveWall._mHitList[current] and not driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                        driver.find_element_by_id(
                            mMovie.movie_start_key()).click()
                        ++num

    @staticmethod
    def on_sense_devices_changed(removed, added):
        InteractiveWall.update_device_list()

    @staticmethod
    def update_device_list():
        InteractiveWall._mIsUpdatingDeviceList = True
        InteractiveWall._mDeviceList.clear()
        for index, current in enumerate(InteractiveWall._mDeviceList):
            device_data = DeviceData(
                current, InteractiveWall.DEPTH_SENSOR_WIDTH, InteractiveWall.DEPTH_SENSOR_HEIGHT)
            key = device_data.device.get_info(rs.camera_info.serial_number)
            InteractiveWall._mDeviceList.append(key, device_data)

        for index, current in enumerate(InteractiveWall._mDeviceList):
            print(" >> Device serial {0}".format(current))
        InteractiveWall._mIsUpdatingDeviceList = False
