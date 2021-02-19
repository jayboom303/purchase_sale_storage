import os


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


@singleton
class ProjectConfig:
    """
    manage.py中进行调用，并传入manage.py文件自身
    """
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.log_dir = os.path.join(self.project_root, "log")
