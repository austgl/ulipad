import Queue
import threading
import time

class AsyncAction(threading.Thread):
    """
    STOP control all inherit class  behivor
    """
    STOP = False
    def __init__(self, timestep=.1):
        super(AsyncAction, self).__init__()
        self.q = Queue.Queue(0)
        self.setDaemon(True)
        self.stop = False
        self.timestep = timestep
        self.last = None
        
    def put(self, obj):
        self.q.put(obj)
        
    def _is_stop(self):
        return self.stop or self.STOP
    is_stop = property(_is_stop)
    
    def stop(self):
        self.stop = True
        
    def _empty(self):
        return self.q.empty()
    empty = property(_empty)
    
    def clear(self):
        while 1:
            try:
                obj = self.q.get_nowait()
            except:
                break
        
    def run(self):
        try:
            while not self.is_stop:
                self.last = None
                while not self.is_stop:
                    try:
                        obj = self.q.get(True, self.get_timestep())
                        self.last = obj
                    except:
                        if self.last:
                            break
                if self.last:
                    try:
                        self.do_action(self.last)
                        self.last = None
                    except:
                        pass

        except:
            pass
            
    def do_action(self, obj):
        '''
        you should judge if not self.empty to quit the process, because
        it means that there is proceed infos need to process, so current
        one should ba cancelled
        '''
        pass
    
    def get_timestep(self):
        return self.timestep
    
if __name__ == '__main__':
    class Test(AsyncAction):
        def do_action(self, obj):
            time.sleep(0.5)
            if not self.empty:
                print 'xxxxxxxxxxxxxxxx', obj
                return
            print 'pppppp', obj
            
    a = Test(1)
    a.start()
    for i in range(100):
        a.put(i)
        print 'put', i
        time.sleep(.1)
    time.sleep(10)
