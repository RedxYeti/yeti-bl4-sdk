from typing import Any 
from mods_base import hook, build_mod,get_pc
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 
from random import randint

def get_variance(in_level:int) -> int:
    roll = randint(1, 100)
    if (roll < 20):
        return in_level - 1
    elif (roll < 40):
        return in_level + 1
    else:
        return in_level


def get_player_level() -> int:
    player_state = get_pc().PlayerState
    return player_state.ExperienceState[0].ExperienceLevel


@hook("/Game/AI/_Shared/Character/Script_Enemy.Script_Enemy_C:OnBeginPlay", Type.POST)
def SetEnemyLevels(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    player_level = get_player_level()
    
    exp_level = obj.Outer.AICharacterState.ExperienceLevel
    if abs(exp_level - player_level) >= 5:
        obj.Outer.AICharacterState.ExperienceLevel = get_variance(player_level)
        obj.Outer.OnRep_AICharacterState()


mod = build_mod()