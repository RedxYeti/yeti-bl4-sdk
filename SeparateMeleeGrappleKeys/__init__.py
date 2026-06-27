from typing import Any 
from mods_base import hook, build_mod,keybind,get_pc,command,BoolOption
from unrealsdk import find_class, make_struct,find_object,find_all
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct,IGNORE_STRUCT,notify_changes

GbxTargetingFunctionLibrary = find_class("GbxTargetingFunctionLibrary").ClassDefaultObject

can_melee = True
melee_name = make_struct("SName",
                        SummaryHash=327007336,
                        TokenCount=1,
                        InlineTokens=make_struct("SToken", Hash=327007336,Name='Melee_Default')
                        )

@keybind("Melee")
def melee_key():
    if not can_melee:
        return
    
    if oidDoLockon.value:
        target = GbxTargetingFunctionLibrary.GetTarget(get_pc().Pawn,get_pc().Pawn,[])[1]
    else:
        target = None

    get_pc().Pawn.ServerPerformSpecificMelee(melee_name, target, oidDoLockon.value)



@hook("/Script/GbxGame.GbxTrickScript:OnBegin_Mut", Type.PRE)
def OnBegin_Mut_SeparateMelee(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    if "ATrick_Melee" in str(obj) and args.Actor == get_pc().Pawn:
        global can_melee
        can_melee = False
        
@hook("/Script/GbxGame.GbxTrickScript:OnEnd_Mut", Type.POST)
def OnIrrelevant_Mut_SeparateMelee(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    if "ATrick_Melee" in str(obj) and args.Actor == get_pc().Pawn:
        global can_melee
        can_melee = True

@command("fixmelee")
def fix_melee(*_):
    global can_melee
    can_melee = True
    print("Melee Reset!")


@keybind("Grapple")
def grapple_key():
    get_pc().Pawn.ServerStartGrapple()


oidDoLockon = BoolOption(
    "Melee Lock on",
    False,
    "Lock On: Off",
    "Lock On: On"
)

mod = build_mod()