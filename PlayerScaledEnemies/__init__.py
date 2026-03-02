from typing import Any 
from mods_base import hook, build_mod,get_pc
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 
from random import randint

def get_variance(in_level:int) -> int:
    roll = randint(1, 100)
    if (roll < 20):
        return in_level - randint(1,2)
    elif (roll < 40):
        return in_level + randint(1,2)
    else:
        return in_level



@hook("/Game/AI/_Shared/Character/Script_Enemy.Script_Enemy_C:OnBeginPlay", Type.POST)
def SetEnemyLevels(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    player_level = get_pc().PlayerState.ExperienceState[0].ExperienceLevel
    exp_level = obj.Outer.AICharacterState.ExperienceLevel
    if abs(exp_level - player_level) >= 5:
        obj.Outer.AICharacterState.ExperienceLevel = get_variance(player_level)
        obj.Outer._post_edit_change_property("AICharacterState")



mod = build_mod()