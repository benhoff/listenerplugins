import re
import types
from yapsy.IPlugin import IPlugin

def return_error(instance, message, done, *args, **kwargs):
    if isinstance(done, types.FunctionType):
        done()
    done = True
    # FIXME
    result = 'You are not authorized to {}'.format(message.command)
    return result, done

class ActivityAuth(object):
    USER_ROLE_MAPPING = None
    ACTIVITY_ROLE_MAPPING = None

    def __init__(self, activity):
        self.activity = re.compile(activity)

    def __call__(self, f):
        def wrapped_function(instance, message, done, *args, **kwargs):
            user = message.user
            if message.command in instance.matches:
                if self.activity in self.get_user_activities(user):
                    return f(instance, message, *args, **kwargs)
                else:
                    return return_error(instance, message, done, *args, **kwargs)

    @classmethod
    def get_user_activities(kls, user):
        role = kls.USER_ROLE_MAPPING[user] 
        return kls.ACTIVITY_ROLE[role]

class Base(IPlugin):
    def __init__(self, function=None, config_source=None):
        super(Base, self).__init__()
        self.config_source = config_source
        self.matches = []
        self.function = function
    
    @ActivityAuth('None')
    def call(self, message, done=None, *args, **kwargs):
        if command in self.matches:
            # TODO: add in authentication here
            result = function(argument, *args, **kwargs)
            if isinstance(done, types.FunctionType):
                done()
            done = True
            return result, done
