from coremon_main import enum_for_custom_event_types, CgmEvent


# custom events
MyEvTypes = enum_for_custom_event_types(
    'InvadersMoveSide',
    'InvadersMoveDown',
    'PlayerReloads'
)
CgmEvent.inject_custom_names(MyEvTypes)
