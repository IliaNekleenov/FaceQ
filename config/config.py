#
# файл с набором разных конфигураций запуска приложения
#

class Config(object):
    DEBUG = False

    # Параметры подключения к камере и конфигурация обработки видеопотока с нее
    CAMERA_LINK = 'http://root:1961@192.168.15.100/mjpg/video.mjpg'
    FRAMES_QUEUE_MAX_SIZE = 5

    # Конфигурация распознавания лица
    FACE_DETECTION_THREADS_COUNT = 5
    # если хотя бы на 'MIN_FRAMES_WITH_FACE' из последних 'MAX_TEST_FRAMES' одно и то же лицо, то оно обрабатывается
    MAX_TEST_FRAMES = 5
    MIN_FRAMES_WITH_FACE = 3

    # Конфигурация печати талонов
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
