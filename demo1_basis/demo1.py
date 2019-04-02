from cgm_engine.runners import VanillaGameCtrl
from sample_world import *
from glvars import SCREEN_SIZE, CAPTION


# - entry point
cgm_engine.init(SCREEN_SIZE, CAPTION)

# - building specific components
mod = AvatarMod()
view = SampleView(mod)
ctrl = AvatarCtrl(mod)
for receiver in (view, ctrl):
    receiver.turn_on()

# - building the generic component (game runner)
game_ctrl = VanillaGameCtrl()
game_ctrl.set_autoquit(True)
game_ctrl.turn_on()

# - let's run the game loop (blocking method)
game_ctrl.loop()
print('done.')
