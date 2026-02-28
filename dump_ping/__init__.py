from typing import Any 
from mods_base import hook, build_mod 
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 
from obj_dump import dump_object

@hook("/Script/OakGame.OakPlayerController:ClientCreatePing",Type.PRE)
def PingDump(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    if args.TargetedActor:
        dump_object(args.TargetedActor)


build_mod()