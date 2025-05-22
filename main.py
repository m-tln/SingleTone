import ctypes
import threading


# First approach: Classic Singleton using __new__
class SingletonClassic:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SingletonClassic, cls).__new__(cls)
                    cls._instance.value = "Classic Singleton"
        return cls._instance

    def __str__(self):
        return self.value


# Second approach: Singleton using ctypes
class SingletonCTypes:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # Create a low-level instance using ctypes
                    cls._instance = ctypes.py_object(super(SingletonCTypes, cls).__new__(cls))
                    cls._instance.value = ctypes.c_char_p(b"Singleton with ctypes")
        return cls._instance

    def __str__(self):
        return self.value.decode('utf-8')


# Third approach: Singleton using metaclass
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonMetaclass(metaclass=SingletonMeta):
    def __init__(self):
        self.value = "Metaclass Singleton"

    def __str__(self):
        return self.value


# Test the implementations
if __name__ == "__main__":
    # Test Classic Singleton
    t1 = SingletonClassic()
    t2 = SingletonClassic()
    print(f"Thread-safe: {t1}, Same instance: {t1 is t2}")

    # Test ctypes Singleton
    c1 = SingletonCTypes()
    c2 = SingletonCTypes()
    print(f"CTypes: {c1}, Same instance: {c1 is c2}")

    # Test Metaclass Singleton
    m1 = SingletonMetaclass()
    m2 = SingletonMetaclass()
    print(f"Metaclass: {m1}, Same instance: {m1 is m2}")
