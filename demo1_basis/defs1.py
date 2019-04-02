from cgm_engine import enum_for_custom_event_types, CgmEvent
from cgm_engine.util import enum_starting_from_zero

GameStates = enum_starting_from_zero('Default')
MyEvTypes = enum_for_custom_event_types('PlayerMoves', 'PlayerDies', 'NewTurn')
CgmEvent.inject_custom_names(MyEvTypes)
