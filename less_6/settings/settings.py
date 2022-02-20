import datetime
from copy import deepcopy
from time import time
from .behav_pat import FileWriter, Subject

"""ПОРАЖДАЮЩИЕ ПАТТЕРНЫ"""


# ПО методу "Фабричный метод"
class AbstractUser:
    __id = 1

    def __init__(self):
        self.id = AbstractUser.__id
        AbstractUser.__id += 1
        self.username = None
        self.type = None

    def __str__(self):
        return f'id: {self.id}, Username: {self.username}'


class Guest(AbstractUser):
    def __init__(self,username=None, type=None):
        super().__init__()
        self.username = 'GUEST'
        self.type = 'guest'


class User(AbstractUser):
    def __init__(self, username=None, type=None):
        # В каких созвонах участвовал
        self.meetups = []
        super().__init__()
        self.username = username
        self.type = type


class Speaker(AbstractUser):
    pass


class UserManager:
    types = {
        'guest': Guest,
        'user': User,
        'speaker': Speaker
    }

    @classmethod
    def create(cls, **kwargs):
        type_ = kwargs.get('type')
        username = kwargs.get('name')
        return cls.types[type_](username=username,type=type_) if type_ else None

    @classmethod
    def get_type(cls):
        print(type(cls))
        # return


# ПО методу пораждающий паттерн
class MeetUpProto:
    def new_clone(self):
        return deepcopy(self)


class MeetUpBase(MeetUpProto,Subject):
    id = 1

    def __init__(self, name, type_into, datetime_at=None):
        self.id = MeetUpBase.id
        MeetUpBase.id += 1
        self.type = type_into
        self.name = name
        self.datetime_at = datetime_at
        self.users = []

    def __getitem__(self, item):
        return self.users[item]

    def add_student(self, user_inst):
        self.users.append(user_inst)
        user_inst.courses.append(self)
        self.notify()


# Виды звонков и совещаний
class TeamCall(MeetUpBase):
    pass


class WorkFlow(MeetUpBase):
    pass


class P2PFlow(MeetUpBase):
    pass


# ПО методу "Фабричный метод"
class MeetUpFactory:
    choice = {
        'team': TeamCall,
        'work': WorkFlow,
        'p2p': P2PFlow
    }

    @classmethod
    def create(cls, **kwargs):
        # TODO запись в файл 'meetup.json'
        _name, _type = kwargs.get('name', None), kwargs.get('type', None)
        print(f'{_name}{_type}')

        if not _name and _type:
            return None
        _utc_now = datetime.datetime.now()
        return cls.choice[_type](name=_name, type_into=_type, datetime_at=_utc_now)


class MeetUpType:
    id = 1

    def __init__(self, name, type):
        self.id = MeetUpType.id
        MeetUpType.id += 1
        self.name = name
        self.type = type
        self.call = []

    def call_count(self):
        result = len(self.call)
        # if self.type:
        #     result += self.call.call_count()
        return result


# Структурный паттерн - "метод ФАСАД"
class Application:
    def __init__(self):
        # TODO будем получать из файла

        self.user = []
        self.meetup = []
        self.type_meetup = []

    # Создание пользователя
    @staticmethod
    def create_user(type_in, name=None):
        return UserManager.create(type=type_in,name=name)

    # Создание "объекта: Встреча"
    @staticmethod
    def create_meetup(name, type):
        return MeetUpFactory.create(name=name, type=type)

    @staticmethod
    def create_type_meetup(name, type_m):
        return MeetUpType(name=name, type=type_m)

    def find_by_theme_id(self, id):
        if not self.type_meetup:
            return None

    def get_all_meet_up(self):
        return self.meetup

    def get_call(self, name):
        for item in self.meetup:
            if item.name == name:
                return item
        return None

    def find_type_meetup_by_id(self, id):
        for obj in self.type_meetup:
            if obj.id == id:
                return obj
        return None


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)


"""СТРУКТУРНЫЕ ПАТТЕРНЫ"""


# Структурный паттерн - метод "Декоратор"
class Route:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes.update({self.url: cls()})


# Структурный паттерн - метод "Декоратор"
class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        # Вспомогательная функция будет декорировать каждый отдельный метод класса
        def timewrap(method):
            def timeit(*args, **kwargs):
                time_start = time()
                result = method(*args, **kwargs)
                time_end = time()
                time_delta = time_end - time_start

                print(f'debug --> {self.name}.{cls.__name__} выполнялся {round(time_delta, 2)} мс')
                return result

            return timeit

        return timewrap(cls)


