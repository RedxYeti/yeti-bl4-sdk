from typing import Any 
from mods_base import hook, build_mod, SliderOption, BoolOption, get_pc
from unrealsdk import find_class
from unrealsdk.hooks import Type,prevent_hooking_direct_calls
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 

statics = find_class("GameplayStatics").ClassDefaultObject

def enable_true_mode():
    with prevent_hooking_direct_calls():
        game_state = statics.GetGameState(get_pc())
        if not game_state:
            return
        game_state.bTrueMode = True
        for player in game_state.PlayerStateStableArray:
            player.bTrueMode = True

@hook("/Script/Engine.GameplayStatics:GetGameState",Type.PRE)
def GetGameState_TMT(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    enable_true_mode()


build_mod(on_enable=enable_true_mode)