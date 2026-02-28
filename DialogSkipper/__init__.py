from typing import Any 
from mods_base import hook, build_mod,BoolOption,keybind,ENGINE 
from unrealsdk import find_class, find_all
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 
from threading import Timer
gameplay_statics = find_class("GameplayStatics").ClassDefaultObject

def skip_dialog():
    for dialog in find_all("GbxDialogProvider"):
        if dialog.CurrentPerformance.DialogThreadID != 0:
            if not dialog.bSpeakDirectlyToPlayer and oidAllowEnemyPlayer.value:
                return
            dialog.NetMulticast_StopDialog(dialog.CurrentPerformance.DialogThreadID, 0.1)
            break

def manual_skip_dialog():
    for dialog in find_all("GbxDialogProvider"):
        if dialog.CurrentPerformance.DialogThreadID != 0:
            dialog.NetMulticast_StopDialog(dialog.CurrentPerformance.DialogThreadID, 0.1)
            break

@hook("/Script/GbxGame.GbxDialogProvider:NetMulticast_StartDialog", Type.POST)
def dialogskip(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    if oidAutoSkip.value:
        #if str(obj.Outer.GetLevel().Name) == "World_P":
        #    skip_dialog()
        #else:
            Timer(0.5,skip_dialog).start()



@keybind("Skip Dialog Key")
def skip_dialog_key():
    manual_skip_dialog()


@keybind("Increase Game Speed")
def increase_game_speed():
    world = ENGINE.GameViewport.World
    current_speed = gameplay_statics.GetGlobalTimeDilation(world)
    if current_speed < 32:
        gameplay_statics.SetGlobalTimeDilation(world, current_speed * 2)

@keybind("Reset Game Speed")
def reset_game_speed():
    gameplay_statics.SetGlobalTimeDilation(ENGINE.GameViewport.World, 1)


@keybind("Toggle Auto Skip")
def toggle_auto_skip():
    oidAutoSkip.value = not oidAutoSkip.value
    print("Dialog Skipper: Auto Skip On" if oidAutoSkip.value else "Dialog Skipper: Auto Skip Off")
    mod.save_settings()


oidAutoSkip = BoolOption("Auto Skip Dialog",
                         False,
                         "On",
                         "Off",)

oidAllowEnemyPlayer = BoolOption("Enemy/Player VO",
                                False,
                                "On",
                                "Off",
                                description="With this on, enemy taunts in combat and player vo will play while auto skip is on."
                                )


mod = build_mod()