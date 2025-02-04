
class BaseInterface():
    def __init__(self):
        self._is_running: bool = False

    def __enter__(self):
        self._is_running = True
        return self

    def __exit__(self, *args, **kwargs):
        self._is_running = False

    def start(self):
        return self.__enter__()

    def stop(self, *args, **kwargs):
        self.__exit__()

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def publics(self):
        yield from type(self).publics(self)

    @classmethod
    def publics(cls):
        for name in dir(cls):
            if not name.startswith('_'):
                attribute = getattr(cls, name)
                if callable(attribute) and getattr(attribute, 'public', False):
                    yield attribute
