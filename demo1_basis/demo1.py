from RocksModel import RocksModel
from ShipModel import ShipModel
from coremon_main.runners import VanillaGameCtrl
import coremon_main
from TinyWorldView import TinyWorldView
from ShipCtrl import ShipCtrl
from glob_scope1 import SCREEN_SIZE, CAPTION


# - entry point
coremon_main.init(SCREEN_SIZE, CAPTION)

# - building specific components
shipm = ShipModel()
rocksm = RocksModel()
view = TinyWorldView(shipm, rocksm)
ctrl = ShipCtrl(shipm, rocksm)
for receiver in (view, ctrl):
    receiver.turn_on()

# - building the generic component (game runner)
game_ctrl = VanillaGameCtrl()
game_ctrl.turn_on()

# - let's run the game loop (blocking method)
print('------------')
print('HOW TO PLAY:')
print('* use arrows to move')
print('* use TAB to use a wormhole!')
print('------------')
print()

game_ctrl.loop()
print('done.')
