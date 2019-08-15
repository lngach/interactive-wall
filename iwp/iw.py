import numpy as np
from datetime import datetime
from math import sin, cos, pi
import pyrealsense2 as rs2

from classes.device_data import DeviceData
from classes.device_setting_info import DeviceSettingInfo
from classes.hit_area import HitArea
from classes.movie_data import MovieData
from classes.wait_movie_data import WaitMovieData

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class InteractiveWall:
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
    CHROMEDRIVER_PATH = './chromedriver'
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
    def run(self):
        self._mIsUpdatingDeviceList = False
        self._mDeviceList = []
        self._mDeviceSetting = []
        self._mMovieList = []

        try:
            with open('setting.txt', 'r') as f:
                line = f.readline()
                separator = ":"
                ch_array = [' ', '\t']
                while line:
                    str_array = line.split(separator, 2)
                    if str_array >= 2:
                        str = str_array[0]
                        if not (str == "content"):
                            if not(str == "max_movie_count"):
                                if not(str == "senser"):
                                    if not(str == "wait_movie"):
                                        if not(str == "movie"):
                                            if str == "bgm":
                                                self._mBGMId = str_array[1].strip(
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
                                                    self._mMovieList.append(
                                                        hit_area)
                                                except:
                                                    pass

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
                                                self._mMovieList.append(
                                                    wait_movie_data)
                                            except:
                                                pass
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
                                            self._mDeviceSetting.append(
                                                device_setting_info)
                                        except:
                                            pass
                            else:
                                try:
                                    self._mMaxMovieCount = str_array[1].strip()
                                except:
                                    pass

                        else:
                            self._mContentPath = str_array[1].strip()
                    line = f.readline()
        except:
            pass
        self._mContext = rs2.context()
        self._mContext.on_devices_changed += rs2.context.set_devices_changed_callback(
            self.on_sense_devices_changed)
        if len(self._mDeviceSetting) <= 0:
            input()
        else:
            self._mHitAreaIdList = []
            self._mHitList = []
            self._mCurrentHitList = []
            for i in range(len(self._mMovieList)):
                mMovie = self._mMovieList[i]
                self._mHitList.append(False)
                self._mCurrentHitList.append(False)
                if type(mMovie) == type(HitArea):
                    self._mHitAreaIdList.append(i)
            self._mLastHitTime = datetime.now()

            options = Options()
            options.headless = True
            driver = webdriver.Chrome(
                CHROMEDRIVER_PATH, chrome_options=options)
            driver.navigate().goto_url(self._mContentPath)
            driver.manage().window.full_screen()
            if self._mBGMId != "":
                driver.find_element_by_id(self._mBGMId + "_play").click()

            while true:
                enumerator1 = enumerate(self._mHitAreaIdList)
                for i, current in enumerator1:
                    self._mCurrentHitList[current] = False
                    if current.device_serial in self._mDeviceList:
                        mDevice = self._mDeviceList[current.device_serial]
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
                                        if self._mCurrentHitList[item]:
                                            mMovie = self._mMovieList[item]
                                            if mMovie.left <= num4 and mMovie.top <= num5 and (num4 <= mMovie.right and num5 <= mMovie.bottom):
                                                self._mCurrentHitListp[current] = True
            flag = False
            num = 0
            for index, current in enumerator1:
                if self._mCurrentHitList[current]:
                    flag = True
            if flag:
                for i in range(len(self._mMovieList)):
                    mMovie = self._mMovieList[i]
                    if type(mMovie) == type(WaitMovieData):
                        if driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                            driver.find_element_by_id(
                                mMovie.movie_stop_key()).click()
                    elif driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                        ++num
            else:
                time_span = datetime.now - self._mLastHitTime
                for i in range(len(self._mMovieList)):
                    mMovie = self._mMovieList[i]
                    if type(mMovie) == type(WaitMovieData) and time_span >= mMovie.wait_time and driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                        driver.find_element_by_id(
                            mMovie.movie_start_key()).click()
            for index, current in enumerator1:
                if self._mCurrentHitList[current] != self._mHitList[current]:
                    mMovie = self._mMovieList[current]
                    self._mHitList[current] = self._mCurrentHitList[current]
                    if num < self._mMaxMovieCount and self._mHitList[current] and not driver.find_element_by_id(mMovie.movie_status_key()).get_attribute("data_is_play") == "true":
                        driver.find_element_by_id(
                            mMovie.movie_start_key()).click()
                        ++num

    @staticmethod
    def on_sense_devices_changed(removed, added):
        self.update_device_list()

    @staticmethod
    def update_device_list(self):
        self._mIsUpdatingDeviceList = True
        self._mDeviceList.clear()
        for index, current in enumerate(self._mDeviceList):
            device_data = DeviceData(
                current, self.DEPTH_SENSOR_WIDTH, self.DEPTH_SENSOR_HEIGHT)
            # Lack of parameter
            key = device_data.device.get_info(rs2.camera_info.serial_number)
            self._mDeviceList.append(key, device_data)

        for index, current in enumerate(self._mDeviceList):
            print(" >> Device serial {0}".format(current))
        self._mIsUpdatingDeviceList = False
