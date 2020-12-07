import re
import requests
from datetime import datetime

BLACKLIST_URL = 'https://front-test-pg.herokuapp.com/blacklist/'

# List of valid DDD numbers
ddd_list = [11, 12, 13, 14, 15, 16, 17, 18,
            19, 21, 22, 24, 27, 28, 31, 32,
            33, 34, 35, 37, 38, 41, 42, 43,
            44, 45, 46, 47, 48, 49, 51, 53,
            54, 55, 61, 62, 63, 64, 65, 66,
            67, 68, 69, 71, 73, 74, 75, 77,
            79, 81, 82, 83, 84, 85, 86, 87,
            88, 89, 91, 92, 93, 94, 95, 96,
            97, 98, 99]

# Map of brokers
brokers = {}
brokers['VIVO'] = 1
brokers['TIM'] = 1
brokers['CLARO'] = 2
brokers['OI'] = 2
brokers['NEXTEL'] = 3

# Decorator to check function args
def accepts(*types):
    def check_accepts(f):
        assert len(types) == (f.__code__.co_argcount)

        def new_function(*args, **kwds):
            for(a, t) in zip(args, types):
                ret_str = f"arg {a} does not match {t}"
                assert isinstance(a, t), ret_str
            return f(*args, **kwds)
        new_function.__name__ = f.__name__
        return new_function
    return check_accepts

# Message class
class Message:

    number_pattern = r'(9)([7-9])\d{7}'
    ddd_pattern = r'\d\d'
    time_format = '%H:%M:%S'

    def __init__(self, msg_id, ddd, number, cpny, schedule, content):
        # Start all messages with valid state
        self.valid = True

        self.msg_id = msg_id
        self.ddd = ddd
        self.number = number
        self.cpny = cpny
        self.schedule = schedule
        self.content = content

    # Creates a message from a comma separated string
    @classmethod
    def from_string(cls, msg):
        """ Returns a Message instance

        Keyword arguments:
        string -- a string containing comma separated values
        """
        try:
            args = msg.split(';')
            msg_id = args[0]
            ddd = int(args[1])
            number = int(args[2])
            cpny = args[3]
            schedule = args[4]
            content = ''.join(args[5:])
            return cls(msg_id, ddd, number, cpny, schedule, content)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            raise(inst)

    def _isvalid_ddd(self):
        """Returns a boolean

        Checks if the ddd is valid
        """
        is_ddd = self.ddd in ddd_list

        return is_ddd

    def _isvalid_number(self):
        """ Returns a boolean

        Checks if the given phone number (without ddd) is valid. If the
        number dont match the pattern we'll return False instead of None
        """
        match = re.match(Message.number_pattern, str(self.number))
        is_number = True if match else False

        return is_number

    def _isfrom_sp(self):
        """ Returns a boolean

        Retuns True if the DDD is from Sao Paulo
        """
        return self.ddd == 11

    def _isvalid_schedule(self):
        """ Returns a boolean

        Returns True if the message's scheduled hour is a valid one
        """
        date_limit = datetime.strptime('19:59:59', Message.time_format)

        date = datetime.strptime(self.schedule, Message.time_format)
        return date < date_limit

    def _isvalid_size(self):
        """ Retuns a boolean

        Returns True if the message respect the size limit
        """
        return len(self.content) < 141

    def _ison_blacklist(self):
        """Returns a boolean

        Checks if the number is in a blacklist:
        200 - is in the blacklist
        404 - it is not
        """
        url = BLACKLIST_URL
        PARAMS = {'phone': self.phone}
        req = requests.get(url, params=PARAMS)
        return req.status_code == 200

    def _validate_number(self):
        return self._isvalid_ddd() and self._isvalid_number()

    def validate_message(self):
        """ Retuns a boolean

        Checks all message parameters and set the message
        state to True if everything is valid, or False if
        some of the parameters is not valid
        """
        number = self._validate_number()
        schedule = self._isvalid_schedule()
        size = self._isvalid_size()
        blacklist = self._ison_blacklist()

        self.valid = (number and schedule and size and blacklist)
        return self.valid

    def phone(self):
        return str(self.ddd) + str(self.number)

    @property
    def ddd(self):
        """ Returns the integer value saved in _ddd"""
        return self._ddd

    @ddd.setter
    def ddd(self, ddd):
        """ Sets an integer value to _ddd"""
        self._ddd = ddd  

    @property
    def msg_id(self):
        """ REtuns the id of this message """
        return self._msg_id
    
    @msg_id.setter
    def msg_id(self, msg_id):
        self._msg_id = msg_id

    def broker(self):
        """ Returns the number of the broken for the given company"""
        return brokers[self.cpny]