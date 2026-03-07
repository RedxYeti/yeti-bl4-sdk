from typing import Any 
from mods_base import hook, build_mod,get_pc
from unrealsdk.hooks import Type, Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 
from unrealsdk import make_struct,find_all
from random import randint

dome_size = make_struct("Vector",X=4.125,Y=4.125,Z=4.125)
trigger_vol_size = make_struct("Vector",X=2.85,Y=2.85,Z=2.85)

@hook("/Game/AI/_Shared/Scripts/Script_BossFight_WorldBosses.Script_BossFight_WorldBosses_C:OnBeginPlay", Type.POST)
def WorldBoss_OnBeginPlay(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    for volume in find_all("OakTriggerVolume"):
        if "/Temp/Game/Maps/WorldStamps/Layouts/Events/WorldBossEvents/SL_WorldBoss_Default" in str(volume):
            volume.SetActorScale3D(trigger_vol_size)

    for dome in find_all("OakInteractiveObject"):
        if "/Temp/Game/Maps/WorldStamps/Layouts/Events/WorldBossEvents/SL_WorldBoss_Default" in str(dome):
            dome.BlueprintCreatedComponents[0].SetRelativeScale3D(dome_size)


@hook("/Game/AI/_Shared/Scripts/Script_BossFight_WorldBosses.Script_BossFight_WorldBosses_C:GbxActorScriptEvt__OnAnyPlayerLeftArena", Type.PRE)
def WorldBoss_OnAnyPlayerLeftArena(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    return Block


build_mod()