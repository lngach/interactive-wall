import pyrealsense2 as rs


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
        self.frame_queue = rs.frame_queue()
        self.device = device
        self.sensor = self.device.sensors[0]

        stream_profiles = self.sensor.get_stream_profiles()
        video_stream_profiles = []

        for item in stream_profiles:
            video_stream_profiles.append(item.as_video_stream_profile())

        depth_video_stream_profiles = filter(
            lambda x: x.stream_type() == rs.stream.depth, video_stream_profiles)

        depth_video_stream_profiles = list(depth_video_stream_profiles)

        sorted_depth_video_stream_profiles = sorted(
            depth_video_stream_profiles, key=lambda x: x.fps(), reverse=True)

        width_height_sorted_depth_video_stream_profiles = filter(
            lambda x: x.width() == width and x.height() == height, sorted_depth_video_stream_profiles)

        width_height_sorted_depth_video_stream_profiles = list(
            width_height_sorted_depth_video_stream_profiles)

        self.sensor_profile = width_height_sorted_depth_video_stream_profiles[0]
        self.width = self.sensor_profile.width()
        self.height = self.sensor_profile.height()
        self.depth = self.width * self.height
        self.distance = self.width
        self.sensor.open(self.sensor_profile)
        self.sensor.start(self.frame_queue)

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
                                                          self.width] * self.sensor.get_depth_scale()
            except expression as identifier:
                return False
            finally:
                return True

    def is_updated_frame_buffer(self):
        return self.sensor != None
