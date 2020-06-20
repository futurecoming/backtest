from datetime import datetime as dt
from abc import ABCMeta, abstractmethod
from engine.event import FillEvent


class ExecutionHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError('Should implement execute_order()')


class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self, events):
        self.events = events

    def execute_order(self, event):
        if event.type == 'ORDER':
            fill_event = FillEvent(dt.utcnow(), event.symbol, 'SHF', event.quantity, event.direction)
            self.events.put(fill_event)
