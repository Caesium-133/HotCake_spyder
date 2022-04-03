from functools import wraps
import time

def debug(isDebug=False,method=None):
    def debugDec(func):
        @wraps(func)
        def wrappedFun(*args,**kwargs):
            if not isDebug or method is None:
                func(*args, **kwargs)
                return
            if method=="time":
                t1=time.time()
                func(*args,**kwargs)
                t2=time.time()
                print("[DEBUG]:"+func.__name__+f"() had run for {t2-t1} seconds")
                return
        return wrappedFun
    return debugDec

