import time
def logger(message,level):
    print('\n[%s] %s %s'%(level,time.strftime('%Y-%m-%d %H:%M:%S'),message),end='')