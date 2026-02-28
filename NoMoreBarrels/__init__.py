from typing import Any 
from mods_base import hook, build_mod,BoolOption,keybind,ENGINE 
from unrealsdk import find_class, find_all
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 


@hook("/Game/InteractiveObjects/ExplodingObjects/ElementalBarrels/_Shared/Script_IO_ExplodingObject_Barrel.Script_IO_ExplodingObject_Barrel_C:OnBeginPlay", Type.POST)
def Script_IO_ExplodingObject_Barrel_C_Begin(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    obj.Outer.GbxDestroyActor(True)
    
@hook("/Game/InteractiveObjects/CarryableObjects/Explosive/Script_Carryable_ExplodingObject_Simple.Script_Carryable_ExplodingObject_Simple_C:OnBeginPlay", Type.POST)
def Script_Carryable_ExplodingObject_Simple_C_Begin(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    if oidDeleteThrowables.value:
        obj.Outer.GbxDestroyActor(True)





oidDeleteThrowables = BoolOption("Delete Throwables",
                         False,
                         "On",
                         "Off",
                         description="With this on, the grappleable barrels will be gone as well.")


mod = build_mod()