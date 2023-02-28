import datetime
from copy import deepcopy
from time import time
from sqlite3 import connect

from settings.architec_pat import DomainObject
from settings.behav_pat import Subject
from settings.exceptions import DbDeleteException, DbUpdateException, DbCommitException, RecordNotFoundException

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
    def __init__(self, username=None, type=None):
        super().__init__()
        self.username = 'GUEST'
        self.type = 'guest'


class User(AbstractUser, DomainObject):
    def __init__(self, username=None, type=None):
        # В каких созвонах участвовал
        self.meetups = []
        super().__init__()
        self.username = username
        self.type = type


class Speaker(AbstractUser):
    def __init__(self, username=None, type=None):
        # В каких созвонах участвовал
        self.meetups = []
        super().__init__()
        self.username = username
        self.type = type


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
        return cls.types[type_](username=username, type=type_) if type_ else None

    @classmethod
    def get_type(cls):
        print(type(cls))
        # return


# ПО методу пораждающий паттерн
class MeetUpProto:
    def new_clone(self):
        return deepcopy(self)


class MeetUpBase(MeetUpProto, Subject):
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
        return UserManager.create(type=type_in, name=name)

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


class UserMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'user'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, username, type_ = item
            user = User(username,type_)
            user.id = id
            result.append(user)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, username FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return User(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (username, type) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.username,obj.type))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MeetUpMapper(UserMapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'meetup'


connection = connect('db.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'user': UserMapper,
        'mapper': MeetUpMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, User):
            return UserMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
