import calendar
import datetime
from copy import deepcopy


# ПО методу "Фабричный метод"
class AbstractUser:
    __id = 1

    def __init__(self):
        self.id = AbstractUser.__id
        AbstractUser.__id += 1
        self.username = None
        self.first_name = None
        self.last_name = None
        self.type = None

    def __str__(self):
        return f'id: {self.id}, Username: {self.username}'


class Guest(AbstractUser):
    pass


class User(AbstractUser):
    pass


class Teacher(AbstractUser):
    pass


class UserManager:
    types = {
        'guest': Guest,
        'user': User,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, **kwargs):
        into = kwargs.get('type', None)
        return cls.types[into] if into else None

    @classmethod
    def get_type(cls):
        print(type(cls))
        # return


# ПО методу пораждающий паттерн
class MeetUpProto:
    def new_clone(self):
        return deepcopy(self)


class MeetUpBase(MeetUpProto):
    id = 1

    def __init__(self, name, type_into, datetime_at=None):
        self.id = MeetUpBase.id
        MeetUpBase.id += 1
        self.type = type_into
        self.name = name
        self.datetime_at = datetime_at



# Виды звонков и совещаний
class TeamCall(MeetUpBase):
    pass


class WorkFlow(MeetUpBase):
    pass


class P2PFlow(MeetUpBase):
    pass


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


class Application:
    def __init__(self):
        # TODO будем получать из файла
        self.guest = []
        self.user = []
        self.meetup = []
        self.type_meetup = []


    # Создание пользователя
    @staticmethod
    def create_user(type_in):
        return UserManager.create(type=type_in)

    # Создание "объекта: Встреча"
    @staticmethod
    def create_meetup(name, type):
        return MeetUpFactory.create(name=name, type=type)

    @staticmethod
    def create_type_meetup(name, type_m):
        return MeetUpType(name=name, type=type_m)

    def find_by_theme_id(self, id):
        if not self.themes_meetup:
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