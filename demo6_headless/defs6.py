from coremon_main import enum_for_custom_event_types, CgmEvent


# custom events
MyEvTypes = enum_for_custom_event_types(
    'TickOccured',  # contains int value: rank, nexttick_in
)
CgmEvent.inject_custom_names(MyEvTypes)
