from pyrealsense2 import rs2


class DeviceData():
    frame_queue = None
    device = None
    sensor = None
    sensor_profile = None
    width = None
    height = None
    depth = None
    distance = None

    def __init__(self, device, width, height):
        self.init(device, width, height)

    def init(self, device, width, height):
        self.un_init()
        self.frame_queue = rs2.frame_queue()
        self.device = device
        self.sensor = self.device.sensors[0]
        self.sensor_profile = filter(self.video_stream_profiles_wh_filter, filter(self.video_stream_profiles_filter, self.device.sensors[0].video_stream_profiles.sort(
            self.video_stream_profiles_descending)))

    def un_init(self):
        if self.sensor != None:
            self.sensor.stop()
            self.sensor.close()
            self.sensor = None
        self.device = None
        self.frame_queue = None
        self.depth = None

    def frame_wait(self, touchline):
        if self.sensor != None:
            try:
                video_frame = self.frame_queue.wait_for_frame(100)
                video_frame.copy_to(self.depth)
                video_frame.dispose()
                if touchline >= 0:
                    if touchline <= self.height:
                        for i in range(self.width):
                            self.distance[i] = self.depth[i + touchline *
                                                          self.width] * self.sensor.depth_scale
            except expression as identifier:
                return False
            finally:
                return True

    def is_updated_frame_buffer(self):
        return self.sensor != None

    def video_stream_profiles_depth_filter(video_stream_profile):
        return video_stream_profile.stream == rs2.stream.depth

    def video_stream_profiles_descending(video_stream_profile):
        return video_stream_profile.frame_rate

    def video_stream_profiles_wh_filter(video_stream_profile):
        return video_stream_profile.width == w and video_stream_profile.height == h
