from typing import Any 
from mods_base import hook, build_mod,BoolOption,keybind,ENGINE,get_pc
from unrealsdk import find_class, find_all
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct, UClass
from threading import Timer
gameplay_statics = find_class("GameplayStatics").ClassDefaultObject
GbxTeamFunctionLibrary = find_class("GbxTeamFunctionLibrary").ClassDefaultObject

def skip_dialog():
    for host in find_all("LiveDialogSpeakerHost"):
        for speaker in host.LiveSpeakers:
            if speaker.GbxDialogProvider.CurrentPerformance.DialogThreadID == 0:
                continue

            if oidAllowEnemyPlayer.value:
                implementer = speaker.AttachedAudioImplementer

                if not implementer:
                    continue

                if "OakCharacter" in str(speaker.AttachedAudioImplementer.Name):
                    continue

                if GbxTeamFunctionLibrary.GetAttitudeTowards(implementer, get_pc().Pawn) == 2:
                    continue

            dialog = speaker.GbxDialogProvider
            dialog.NetMulticast_StopDialog(dialog.CurrentPerformance.DialogThreadID, 0.1)


def manual_skip_dialog():
    for dialog in find_all("GbxDialogProvider"):
        if dialog.CurrentPerformance.DialogThreadID != 0:
            dialog.NetMulticast_StopDialog(dialog.CurrentPerformance.DialogThreadID, 0.1)


@hook("/Script/GbxGame.GbxDialogProvider:NetMulticast_StartDialog", Type.POST)
def dialogskip(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    if oidAutoSkip.value:
        Timer(0.1,skip_dialog).start()




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
                                description="With this on, enemy taunts in combat and all player vo will play while auto skip is on. (Can still be skipped with the hotkey.)"
                                )


mod = build_mod()