import time
class Timer(object):
    TIMER_STOP = -1
    def __init__(self, duration)-> None:
        self.inicio = self.TIMER_STOP
        self.duracion = duration

    def start(self)-> None:
        if self.inicio == self.TIMER_STOP:
            self.inicio = time.time()

    def stop(self)-> None:
        if self.inicio != self.TIMER_STOP:
            self.inicio = self.TIMER_STOP

    def running(self)-> bool:
        return self.inicio != self.TIMER_STOP

    def timeout(self)-> bool:
        if not self.running():
            return False
        else:
            return time.time() - self.inicio >= self.duracion
