from typing import Any 
from mods_base import hook, build_mod,keybind,get_pc,command,SliderOption
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 
from argparse import Namespace


@hook("/Script/OakGame.OakPlayerController:ServerNotifyCharacterSelectFinished", Type.POST)
def ServerAcknowledgePossession_FOVSlider(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    obj.player.basefov = oidFOV.value

def changed_fov(option,new_value):
    if get_pc() and get_pc().player:
        get_pc().player.basefov = new_value

@command("fovp")
def set_fov(args: Namespace):
    try:
        float(args.fov)
    except:
        return
    oidFOV.value = float(args.fov)
    mod.save_settings()
    if get_pc() and get_pc().player:
        get_pc().player.basefov = float(args.fov)


set_fov.add_argument("fov")

oidFOV = SliderOption(
    "FOV",
    100,
    0,
    360,
)

mod = build_mod()