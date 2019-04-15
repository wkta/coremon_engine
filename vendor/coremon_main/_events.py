import time
import weakref
from abc import abstractmethod

import pygame
from pygame.event import Event as PygameEvent
from pygame.locals import USEREVENT

from coremon_main.Singleton import Singleton
from ._defs import EngineEvTypes, FIRST_CUSTO_TYPE


class CgmEvent:
    ETYPE_ATTR_NAME = 'cgm_type'
    ref_enum_custom = None

    def __init__(self, engin_ev_type, **kwargs):
        if engin_ev_type == USEREVENT:
            raise ValueError('ev_type {} is not valid (cgm reserved type)')

        self.type = engin_ev_type

        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def inject_custom_names(cls, ref_enum):
        cls.ref_enum_custom = ref_enum

    @staticmethod
    def ext_tev_detection(etype):
        # extended type event detection
        return etype == USEREVENT

    def wrap(self):
        """
        :return: a corresponding pygame event object, so it can be put on the pygame queue
        """
        tmp = self.__dict__.copy()
        if self.type > USEREVENT:
            tmp[self.ETYPE_ATTR_NAME] = self.type
            t = USEREVENT
        else:
            t = self.type
        del tmp['type']
        return PygameEvent(t, tmp)

    @classmethod
    def unwrap(cls, pygam_ev_obj):
        assert pygam_ev_obj.type == USEREVENT
        engin_type = getattr(pygam_ev_obj, cls.ETYPE_ATTR_NAME)

        tmp = pygam_ev_obj.dict
        del tmp[cls.ETYPE_ATTR_NAME]
        return cls(engin_type, **tmp)  # instanciation CgmEvent

    def __str__(self):
        if self.type > USEREVENT:
            if self.type < FIRST_CUSTO_TYPE:
                nom = EngineEvTypes.inv_map[self.type]
            elif self.ref_enum_custom is None:
                nom = '????'
            else:
                nom = self.ref_enum_custom.inv_map[self.type]
        else:
            nom = pygame.event.event_name(self.type)
        tmp = self.__dict__.copy()
        del tmp['type']
        return '<CgmEvent({}-{} {})>'.format(self.type, nom, tmp)


class CogObject:
    """
    basic cogmonger object,
    grants access to utility methods:
    - get_id()
    - pev(ev_type, ...)
    """

    _instances_clue = set()
    _unavailable_ids = set()
    _next_id = 0

    # cached info.
    _manager = None
    _lu_cached_ev = None
    _paint_cached_ev = None

    # we can send 'N times' the logic update event
    # while keeping the same time.time() value
    # => this speeds up the game without loosing too much precision on time handling
    _optim_counter = 0
    _n_times_same_timeval = 100

    def __init__(self, explicit_id=None):
        cls = __class__

        # first call to CogObject.__init__ => initialized cached info. for class
        if cls._manager is None:
            cls._manager = EventManager.instance()
            cls._lu_cached_ev = CgmEvent(EngineEvTypes.LOGICUPDATE, curr_t=None)
            cls._paint_cached_ev = CgmEvent(EngineEvTypes.PAINT)

        # - attribue un nouvel _id pour cette instance de CogObject
        self._id = self.__trouve_nouvel_id() if (explicit_id is None) else explicit_id
        assert isinstance(self._id, int)
        self.__class__._unavailable_ids.add(self._id)

        # - garde trace de cette nouvelle instance...
        self._instances_clue.add(weakref.ref(self))

    @classmethod
    def __trouve_nouvel_id(cls):
        while cls._next_id in cls._unavailable_ids:
            cls._next_id += 1
        res = cls._next_id
        return res

    def __del__(self):
        self.__class__._unavailable_ids.remove(self._id)

    def get_id(self):
        return self._id

    @classmethod
    def __list_instances(cls):
        dead = set()
        for ref in cls._instances_clue:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances_clue -= dead

    @classmethod
    def select_by_id(cls, given_id):
        for obj in cls.__list_instances():
            if given_id == obj.get_id():
                return obj
        return None

    def pev(self, ev_type, **kwargs):
        if ev_type == EngineEvTypes.LOGICUPDATE:
            adhoc_ev = self._lu_cached_ev
            if self._optim_counter == 0:
                adhoc_ev.curr_t = time.time()
            self._optim_counter = self._optim_counter % self._n_times_same_timeval
        elif ev_type == EngineEvTypes.PAINT:
            adhoc_ev = self._paint_cached_ev
        else:
            adhoc_ev = CgmEvent(ev_type, source=self, **kwargs)

        self._manager.post(adhoc_ev)


class EventReceiver(CogObject):

    def __init__(self, sticky=False):
        super().__init__()
        self._sticky = sticky  # True => this receiver won't be turned off when the EventManager soft resets
        self._active_receiver = False

    def is_sticky(self):
        return self._sticky

    def is_active(self):
        return self._active_receiver

    def turn_on(self, prio=None):
        self._manager.add_listener(self, prio)
        self._active_receiver = True

    def turn_off(self):
        self._manager.remove_listener(self)
        self._active_receiver = False


    @abstractmethod
    def proc_event(self, ev, source):
        pass


class EventDispatcher:
    binf_priority = 0
    bsup_priority = 0

    def __init__(self):
        self._assoc_recv_prio = dict()
        self._assoc_prio_recv = dict()

    def add_listener(self, obj, val_priorite=None):
        assert isinstance(obj, EventReceiver)
        assert obj not in self._assoc_recv_prio
        cls = self.__class__

        if val_priorite is None:
            cls.bsup_priority += 1
            p = cls.bsup_priority
        else:
            p = val_priorite
            assert p not in self._assoc_prio_recv
            if p < cls.binf_priority:
                cls.binf_priority = p
            elif p > cls.bsup_priority:
                cls.bsup_priority = p

        self._assoc_recv_prio[obj] = p
        self._assoc_prio_recv[p] = obj

    # - deprecated block --- ?
    def _mod_priority(self, obj, chosen_p):
        assert obj in self._assoc_recv_prio
        self.remove_listener(obj)
        self.add_listener(obj, chosen_p)

    def prioritize(self, obj):
        self._mod_priority(obj, self.__class__.binf_priority - 1)

    def postpone(self, obj):
        self._mod_priority(obj, self.__class__.bsup_priority + 1)

    # ---

    def remove_listener(self, obj):
        if obj not in self._assoc_recv_prio:
            return  # rien à faire

        old_prio = self._assoc_recv_prio[obj]

        del self._assoc_recv_prio[obj]
        del self._assoc_prio_recv[old_prio]

        cls = self.__class__
        if old_prio == cls.binf_priority:
            try:
                cls.binf_priority = min(self._assoc_prio_recv.keys())
            except ValueError:
                cls.binf_priority = 0
        elif old_prio == cls.bsup_priority:
            try:
                cls.bsup_priority = max(self._assoc_prio_recv.keys())
            except ValueError:
                cls.bsup_priority = 0

    def soft_reset(self):
        for memb in tuple(self._assoc_recv_prio.keys()):
            if memb not in self._assoc_recv_prio:
                continue
            if not memb.is_sticky():
                self.remove_listener(memb)

    def hard_reset(self):
        for memb in tuple(self._assoc_recv_prio.keys()):
            if memb not in self._assoc_recv_prio:
                continue
            self.remove_listener(memb)
        cls = self.__class__
        cls.binf_priority = cls.bsup_priority = 0

    def count_listeners(self):
        return len(self._assoc_recv_prio)

    # - the most important method here!
    def dispatch(self, cgm_event, source):
        """
        :param cgm_event: instance of CgmEvent class, includes a type
        :param source: None can be used as a wildcard value, denoting the global EventManager
        :return:
        """

        cls = self.__class__
        for p in range(cls.binf_priority, cls.bsup_priority + 1):
            if p in self._assoc_prio_recv:
                stop_sig = self._assoc_prio_recv[p].proc_event(cgm_event, source)
                if stop_sig:
                    return


@Singleton
class EventManager(EventDispatcher):
    """
    the root source for all events
    """

    def post(self, engin_ev):
        pygame.event.post(engin_ev.wrap())

    def update(self):
        for pygame_reg_ev in pygame.event.get():
            # - ev. classiques
            if not CgmEvent.ext_tev_detection(pygame_reg_ev.type):
                self.dispatch(pygame_reg_ev, None)
                continue
            # - ev. étendus
            cgm_ev = CgmEvent.unwrap(pygame_reg_ev)
            self.dispatch(cgm_ev, None)
