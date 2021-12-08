class Config(object):
    DEBUG = False

    # Video stream properties
    CAMERA_LINK = 'http://root:1961@192.168.15.100/mjpg/video.mjpg'
    FRAMES_QUEUE_MAX_SIZE = 5

    # Face detection properties
    FACE_DETECTION_THREADS_COUNT = 5
    # if at least 'MIN_FRAMES_WITH_FACE' frames out of last 'MAX_TEST_FRAMES' have the same face, the face will be processed
    MAX_TEST_FRAMES = 5
    MIN_FRAMES_WITH_FACE = 3

    # Printer config
    PRINT_TICKETS = True


class ProdConfig(Config):
    pass


class NoPrinterConfig(Config):
    PRINT_TICKETS = False


class LocalCameraConfig(Config):
    CAMERA_LINK = 0


class LocalProdConfig(LocalCameraConfig, NoPrinterConfig):
    pass


class DebugConfig(Config):
    DEBUG = True


class LocalDebugConfig(DebugConfig, LocalCameraConfig, NoPrinterConfig):
    pass
