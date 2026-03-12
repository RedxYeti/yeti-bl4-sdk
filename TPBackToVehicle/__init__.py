from typing import Any 
from mods_base import hook, build_mod,keybind,get_pc,command
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 
from argparse import Namespace

loc = None
rot = None

@hook("/Script/GbxGame.GbxActorScript:OnEndPlay", Type.PRE)
def OnEndPlay_TPVehicle(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    if "OakVehicle" in str(obj) and obj.Outer.RestrictedOwner and obj.Outer.RestrictedOwner.Class.Name == "OakPlayerController":
        global loc,rot
        loc = get_pc().Pawn.K2_GetActorLocation()
        rot = get_pc().Pawn.K2_GetActorRotation()


@keybind("Teleport to Vehicle")
def tp_to_vehicle():
    if loc:
        get_pc().Pawn.K2_TeleportTo(loc,rot)

@command("tptovehicle")
def tp_to_vehicle_command(args: Namespace) -> None:
    if loc:
        get_pc().Pawn.K2_TeleportTo(loc,rot)

mod = build_mod()