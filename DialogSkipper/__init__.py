from typing import Any 
from mods_base import hook, build_mod,BoolOption,keybind,ENGINE,get_pc, SliderOption
from unrealsdk import find_class, find_all
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct, UClass
from threading import Timer
GameplayStatics = find_class("GameplayStatics").ClassDefaultObject
GbxTeamFunctionLibrary = find_class("GbxTeamFunctionLibrary").ClassDefaultObject

def check_skip_dialog():
    for host in find_all("LiveDialogSpeakerHost"):
        for speaker in host.LiveSpeakers:
            if speaker.GbxDialogProvider.CurrentPerformance.DialogThreadID == 0:
                continue

            dialog = speaker.GbxDialogProvider

            if not oidAllowPlayer.value and not oidAllowEnemy.value:
                skip_dialog()
                return
            
            implementer = speaker.AttachedAudioImplementer
            if not implementer:
                dialog.NetMulticast_StopDialog(dialog.CurrentPerformance.DialogThreadID, 0.1)
                continue
            
            if "OakCharacter" in str(speaker.AttachedAudioImplementer):
                team_reaction = GbxTeamFunctionLibrary.GetAttitudeTowards(speaker.AttachedAudioImplementer, get_pc().Pawn)
                if oidAllowPlayer.value:
                    if speaker.AttachedAudioImplementer.Controller and speaker.AttachedAudioImplementer.Controller.Class.Name == "OakPlayerController":
                        return
                if oidAllowEnemy.value and team_reaction == 2:
                    return

            dialog.NetMulticast_StopDialog(dialog.CurrentPerformance.DialogThreadID, 0.1)



def skip_dialog():
    for dialog in find_all("GbxDialogProvider"):
        if dialog.CurrentPerformance.DialogThreadID != 0:
            dialog.NetMulticast_StopDialog(dialog.CurrentPerformance.DialogThreadID, 0.1)


@hook("/Script/GbxGame.GbxDialogProvider:NetMulticast_StartDialog", Type.POST)
def dialogskip(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    if oidAutoSkip.value:
        Timer(oidDelay.value,check_skip_dialog).start()

@keybind("Skip Dialog Key")
def skip_dialog_key():
    skip_dialog()


@keybind("Increase Game Speed")
def increase_game_speed():
    world = ENGINE.GameViewport.World
    current_speed = GameplayStatics.GetGlobalTimeDilation(world)
    if current_speed < 32:
        GameplayStatics.SetGlobalTimeDilation(world, current_speed * 2)

@keybind("Reset Game Speed")
def reset_game_speed():
    GameplayStatics.SetGlobalTimeDilation(ENGINE.GameViewport.World, 1)


@keybind("Toggle Auto Skip")
def toggle_auto_skip():
    oidAutoSkip.value = not oidAutoSkip.value
    print("Dialog Skipper: Auto Skip On" if oidAutoSkip.value else "Dialog Skipper: Auto Skip Off")
    mod.save_settings()


oidAutoSkip = BoolOption("Auto Skip Dialog",
                         False,
                         "On",
                         "Off",)

oidAllowEnemy = BoolOption("Enemy Taunts",
                                False,
                                "On",
                                "Off",
                                description=("With this on, enemy taunts will play.")
                                )

oidAllowPlayer = BoolOption("Player Taunts",
                            False,
                            "On",
                            "Off",
                            description=("With this on, ALL player voice lines will play. Note: Random things use the player for dialog, so you'll have to skip those manually when needed.")
                            )
oidDelay = SliderOption(
    "Skip Delay",
    0.3,
    0.1,
    5,
    0.1,
    False,
    description="Time in seconds how long to wait for auto skip to attempt to skip dialog. Increase this if it's missing voice lines. Shouldn't need more than 1 second. 0.3 usually only misses when you dont have control of your character."
)

mod = build_mod()