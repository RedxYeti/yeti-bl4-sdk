from typing import Any 
from mods_base import hook, build_mod,BoolOption,get_pc,SliderOption
from unrealsdk import find_object
from unrealsdk.hooks import Type 
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 


def set_move_slam_data(slam:UObject) -> None:
    slam.GravityModifier.constant = 40
    slam.bApplyLaunchVelocityOnStart = False
    slam.LaunchDirection.RelativeDirection = 0

def set_trick_options_data(options:list[UObject]) -> None:
    for option in options:
        option.bBlockWeaponActions = False
        option.bLockActionSkills = False
        option.bHideWeapons = False
        option.bBringUpWeaponAtEnd = False
        option.bLockActionSkills = False
        option.bHideFirstPersonLegs = True

    options[-1].bBlockJumping = False
    options[-1].MovementModesToBlock = 0


def set_slam_data():
    if not get_pc().Pawn or get_pc().Pawn.Class.Name == "OakVehicle":
        return

    Default__OakControlledMove_GroundSlam_options = find_object('OakTrickOptions','/Script/OakGame.Default__OakControlledMove_GroundSlam:options')
    Move_GroundSlam_options = find_object('OakTrickOptions','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Move_GroundSlam.Move_GroundSlam:options')
    
    try:
        Trick_Looping_GroundSlam = find_object('GbxTrick_Loop','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Trick_Looping_GroundSlam.Trick_Looping_GroundSlam')
        Trick_GroundSlamExit = find_object('GbxTrick_Anim','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Trick_GroundSlamExit.Trick_GroundSlamExit')
        Trick_Looping_GroundSlam.Start.Meshes[1].Anim.Asset = None
        Trick_Looping_GroundSlam.Loops[0].Anim.Meshes[1].Anim.Asset = None
        if not oidSlamEffect.value:
            Trick_GroundSlamExit.AnimData.Meshes[0].Anim.Asset = None
        Move_GroundSlam = find_object('OakControlledMove','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Move_GroundSlam.Move_GroundSlam')
        set_move_slam_data(Move_GroundSlam)
        Trick_Looping_GroundSlam_options = find_object('OakTrickOptions','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Trick_Looping_GroundSlam.Trick_Looping_GroundSlam:options')
        Trick_GroundSlamExit_Water_options = find_object('OakTrickOptions','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Trick_GroundSlamExit_Water.Trick_GroundSlamExit_Water:options')
        Trick_GroundSlamExit_options = find_object('OakTrickOptions','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Trick_GroundSlamExit.Trick_GroundSlamExit:options')
        trick_options = [
            Default__OakControlledMove_GroundSlam_options,
            Move_GroundSlam_options,
            Trick_Looping_GroundSlam_options,
            Trick_GroundSlamExit_Water_options,
            Trick_GroundSlamExit_options,
        ]
        set_trick_options_data(trick_options)
    except:
        pass

    try:
        Trick_Looping_GroundSlam = find_object('GbxTrick_Loop','/Game/DLC/Cowbell/PlayerCharacters/_Shared/Tricks/TrickLoop_GroundSlam_Robodealer.TrickLoop_GroundSlam_Robodealer')
        Trick_GroundSlamExit = find_object('GbxTrick_Anim','/Game/DLC/Cowbell/PlayerCharacters/_Shared/Tricks/Trick_GroundSlamExit_Robodealer.Trick_GroundSlamExit_Robodealer')
        Trick_Looping_GroundSlam.Start.Meshes[1].Anim.Asset = None
        Trick_Looping_GroundSlam.Loops[0].Anim.Meshes[1].Anim.Asset = None
        if not oidSlamEffect.value:
            Trick_GroundSlamExit.AnimData.Meshes[0].Anim.Asset = None
        Move_GroundSlam = find_object('OakControlledMove','/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Move_GroundSlam.Move_GroundSlam')
        set_move_slam_data(Move_GroundSlam)
        Trick_Looping_GroundSlam_options = find_object('OakTrickOptions','/Game/DLC/Cowbell/PlayerCharacters/_Shared/Tricks/TrickLoop_GroundSlam_Robodealer.TrickLoop_GroundSlam_Robodealer:options')
        Trick_GroundSlamExit_Water_options = find_object('OakTrickOptions','/Game/DLC/Cowbell/PlayerCharacters/_Shared/Tricks/Trick_GroundSlamExit_Water_Robodealer.Trick_GroundSlamExit_Water_Robodealer:options')
        Trick_GroundSlamExit_options = find_object('OakTrickOptions','/Game/DLC/Cowbell/PlayerCharacters/_Shared/Tricks/Trick_GroundSlamExit_Robodealer.Trick_GroundSlamExit_Robodealer:options')
        trick_options = [
            Default__OakControlledMove_GroundSlam_options,
            Move_GroundSlam_options,
            Trick_Looping_GroundSlam_options,
            Trick_GroundSlamExit_Water_options,
            Trick_GroundSlamExit_options,
        ]
        set_trick_options_data(trick_options)
    except:
        pass

    return


def set_slam_damage(option = None, new_value = None, obj=None):
    if not get_pc():
        return
    if not obj:
        obj = get_pc()
    if not obj.Pawn or obj.Pawn.Class.Name == "OakVehicle":
        return
    if not new_value:
        new_value = oidSlamDamage.value
    obj.Pawn.OakCharacterMovement.GroundSlamDamage.Value = new_value
    return


@hook("/Script/OakGame.OakPlayerController:ServerNotifyCharacterSelectFinished",Type.POST)
def ServerNotifyCharacterSelectFinished_Slams(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    set_slam_data()
    set_slam_damage(obj=obj)
    return


@hook("/Game/PlayerCharacters/_Shared/Tricks/ControlledMoves/Trick_GroundSlamExit.Trick_GroundSlamExit_Script_Instanced_C:OnBegin_Mut", Type.POST)
def FixCamera_Slams(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    obj.OnEnd_Mut(args.Actor, 0)
    return


oidSlamEffect = BoolOption("Play Final Anim For Sound",
                         False,
                         "On",
                         "Off",
                         description="With this on, it will play the final slam animation which will add the sound back. Requires restart to turn on if you've already loaded in game.")


oidSlamDamage = SliderOption("Slam Damage",
                         100,
                         0,
                         1000000,
                         description="Set your slam damage. Since you can slam effectively 3 times faster you might want to lower this. Default is 95, and the max is for Mario mode.",
                         on_change=set_slam_damage)


mod = build_mod(on_enable=set_slam_damage)