from typing import Any 
from mods_base import hook, build_mod, BoolOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 


@hook("/Game/AI/_Shared/Corruption/Script_DroneProj_CorruptionShard.Script_DroneProj_CorruptionShard_C:Orbiting__OnStateEnabled", Type.POST)
def BreakAllOrbsHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    obj.GbxActorScriptEvt__OnExplode(obj.Outer)


@hook("/Game/AI/_Shared/Corruption/Script_IO_CorruptionCrystal.Script_IO_CorruptionCrystal_C:ExecuteUbergraph_Script_IO_CorruptionCrystal", Type.POST)
@hook("/Game/DLC/Cello/AI/_Shared/OrdiniteInfusion/Script_IO_OrdiniteCrystal.Script_IO_OrdiniteCrystal_C:ExecuteUbergraph_Script_IO_OrdiniteCrystal", Type.POST)
def BreakAllCrystalsHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    if oidNoCrystals.value:
        obj.GbxActorScriptEvt__DamageState_OnHealthDepleted(None, None)


oidNoCrystals = BoolOption(
    "Remove All Crystals",
    False,
    "On",
    "Off",
    description="Turning this on will remove enemy crystals when they spawn, unfortunately removes a portion of their health as well.",
)


build_mod()