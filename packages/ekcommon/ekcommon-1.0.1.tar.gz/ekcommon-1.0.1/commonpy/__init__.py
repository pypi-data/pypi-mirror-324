import functools
import pytz
from datetime import date
from .simpleexceptioncontext import SimpleExceptionContext, simple_exception_handling
from .log_handler import start_logging, MyFormatter



dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
dictnfilt = lambda x, y: dict([(i, x[i]) for i in x if not(i in set(y))])

lmap= lambda x,y: list(map(x,y))
smap = lambda x,y: set(map(x,y))

def never_throw(f,*args,default=None,**kwargs):
    try:
        return f(*args,**kwargs)
    except:
        return default

def tzawareness(d1,d2):
    if d2.tzinfo is not None:
        return localize_it(d1)
    else:
        return unlocalize_it(d1)


def localize_it (x):
    if x is None:
        return None
    if type(x) is date:
        return x
    return (pytz.UTC.localize(x, True) if not x.tzinfo else x)
def unlocalize_it(dat):
    if type(dat) is date:
        return dat
    d=localize_it(dat)
    return d.replace(tzinfo=None)


def ifnotnan(t, v, els=lambda x: None):
    if t is not None:
        return v(t)
    else:
        return els(t)
def selfifnn(t,el):
    if t is not None:
        return t
    else:
        return el

def ifnn(t, v, els=lambda: None):
    if t is not None:
        return v()
    else:
        return els()


def assert_not_none(x):
    assert x is not None 
    return x 

def cache_if_not_cond(func=None, cond=None):
    if func is None:
        return functools.partial(cache_if_not_cond,
                cond=cond)    
    def internal(*arg,**kw):
        func.cache_remove_if( lambda user_function_arguments, user_function_result, is_alive: cond(user_function_result))
        return func(*arg,**kw)
    return internal

def cache_if_not_none(func):
    def internal(*arg,**kw):
        func.cache_remove_if( lambda user_function_arguments, user_function_result, is_alive: user_function_result is None)
        return func(*arg,**kw)
    return internal






