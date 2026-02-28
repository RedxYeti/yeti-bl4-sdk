from typing import Any 
from mods_base import hook, build_mod,BoolOption,keybind,ENGINE 
from unrealsdk import find_class, find_all
from unrealsdk.hooks import Type, Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct 

blacklisted_modifiers = []

def remove_child_drones(enemy_pawn):
    for child in enemy_pawn.Children:
        child_str = str(child)
        if "DroneProj_Trait_Special_Invulnerable" in child_str or "DroneProj_Trait_Special_Invisible" in child_str:
            child.deactivate()

        
trait_statics = find_class("OakTraitStatics").ClassDefaultObject
param_lib = find_class("GbxParamBlueprintLibrary").ClassDefaultObject
@hook("/Game/AI/_Shared/Character/Script_Enemy.Script_Enemy_C:OnBeginPlay",Type.POST)
def ModEater_OnBeginPlay(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) ->  None:
    pawn_traits = obj.Outer.OakTraitContainer
    traits_to_remove = []
    for idx in range(len(pawn_traits.ActiveSet)):
        trait = pawn_traits.ActiveSet[idx]
        trait_str = str(pawn_traits.ActiveSet[idx].TraitDef)
        found_trait = False

        for mod in blacklisted_modifiers:
            if mod in trait_str:
                traits_to_remove.append(pawn_traits.ActiveSet[idx])
                if mod in ["Trait_Special_Invisible", "Trait_Special_Invisible"]:
                    remove_child_drones(obj.Outer)
                found_trait = True
                break
        if found_trait:
            continue

    if len(traits_to_remove):
        for trait in traits_to_remove:
            trait_statics.RemoveTrait(obj.Outer, trait.TraitDef)
        obj.Outer.OnRep_TraitsChanged()


def trait_changed(option,new_value):
    if new_value == False:
        blacklisted_modifiers.append(option.identifier)
    else:
        try:
            blacklisted_modifiers.remove(option.identifier)
        except:
            pass

def mod_enabled():
    global blacklisted_modifiers
    blacklisted_modifiers = []
    for option in oid_list:
        if option.value == False:
            blacklisted_modifiers.append(option.identifier)

oidDeflector = BoolOption(
    "Trait_Damage_Deflect",
    True,
    "Active",
    "Inactive",
    display_name="Deflector",
    on_change=trait_changed,
)

oidStrong = BoolOption(
    "Trait_Damage_Increase",
    True,
    "Active",
    "Inactive",
    display_name="Strong",
    on_change=trait_changed,
)

oidImmovable = BoolOption(
    "Trait_Damage_LockReactions",
    True,
    "Active",
    "Inactive",
    display_name="Immovable",
    on_change=trait_changed,
)

oidLineDrive = BoolOption(
    "Trait_Damage_ReturnProjectile",
    True,
    "Active",
    "Inactive",
    display_name="Line Drive",
    on_change=trait_changed,
)

oidQuickened = BoolOption(
    "Trait_Damage_SpeedBurst",
    True,
    "Active",
    "Inactive",
    display_name="Quickened",
    on_change=trait_changed,
)

oidChainMaster = BoolOption(
    "Trait_Elemental_Chains",
    True,
    "Active",
    "Inactive",
    display_name="Chain Master",
    on_change=trait_changed,
)

oidChromatic = BoolOption(
    "Trait_Elemental_Cycle",
    True,
    "Active",
    "Inactive",
    display_name="Chromatic",
    on_change=trait_changed,
)

oidElementalEater = BoolOption(
    "Trait_Elemental_Heal",
    True,
    "Active",
    "Inactive",
    display_name="Elemental Eater",
    on_change=trait_changed,
)

oidContagious = BoolOption(
    "Trait_Elemental_Spread",
    True,
    "Active",
    "Inactive",
    display_name="Contagious",
    on_change=trait_changed,
)

oidLeaking = BoolOption(
    "Trait_Elemental_Trail",
    True,
    "Active",
    "Inactive",
    display_name="Leaking",
    on_change=trait_changed,
)

oidArmored = BoolOption(
    "Trait_Health_AddArmorBar",
    True,
    "Active",
    "Inactive",
    display_name="Armored",
    on_change=trait_changed,
)

oidShielded = BoolOption(
    "Trait_Health_AddEnergyBar",
    True,
    "Active",
    "Inactive",
    display_name="Shielded",
    on_change=trait_changed,
)

oidHealthy = BoolOption(
    "Trait_Health_AddFleshBar",
    True,
    "Active",
    "Inactive",
    display_name="Healthy",
    on_change=trait_changed,
)

oidExperienced = BoolOption(
    "Trait_Health_LevelUp",
    True,
    "Active",
    "Inactive",
    display_name="Experienced",
    on_change=trait_changed,
)

oidRegenerative = BoolOption(
    "Trait_Health_Regen",
    True,
    "Active",
    "Inactive",
    display_name="Regenerative",
    on_change=trait_changed,
)

oidVampiric = BoolOption(
    "Trait_Health_Steal",
    True,
    "Active",
    "Inactive",
    display_name="Vampiric",
    on_change=trait_changed,
)

oidWealthy = BoolOption(
    "Trait_Loot_Cash",
    True,
    "Active",
    "Inactive",
    display_name="Wealthy",
    on_change=trait_changed,
)

oidBougie = BoolOption(
    "Trait_Loot_Eridium",
    True,
    "Active",
    "Inactive",
    display_name="Bougie",
    on_change=trait_changed,
)

oidArmsDealer = BoolOption(
    "Trait_Loot_Guns",
    True,
    "Active",
    "Inactive",
    display_name="Arms Dealer",
    on_change=trait_changed,
)

oidQuartermaster = BoolOption(
    "Trait_Loot_Gear",
    True,
    "Active",
    "Inactive",
    display_name="Quartermaster",
    on_change=trait_changed,
)

oidTicking = BoolOption(
    "Trait_Death_Explode",
    True,
    "Active",
    "Inactive",
    display_name="Ticking",
    on_change=trait_changed,
)

oidColdHearted = BoolOption(
    "Trait_Death_Freeze",
    True,
    "Active",
    "Inactive",
    display_name="Cold Hearted",
    on_change=trait_changed,
)

oidTricky = BoolOption(
    "Trait_Death_DropProjectile",
    True,
    "Active",
    "Inactive",
    display_name="Tricky",
    on_change=trait_changed,
)

oidVengeful = BoolOption(
    "Trait_Death_ReturnProjectile",
    True,
    "Active",
    "Inactive",
    display_name="Vengeful",
    on_change=trait_changed,
)

oidCentripetal = BoolOption(
    "Trait_Death_Singularity",
    True,
    "Active",
    "Inactive",
    display_name="Centripetal",
    on_change=trait_changed,
)

oidFortified = BoolOption(
    "Trait_Special_Barricade",
    True,
    "Active",
    "Inactive",
    display_name="Fortified",
    on_change=trait_changed,
)

oidInvisible = BoolOption(
    "Trait_Special_Invisible",
    True,
    "Active",
    "Inactive",
    display_name="Invisible",
    on_change=trait_changed,
)

oidInvulnerable = BoolOption(
    "Trait_Special_Invulnerable",
    True,
    "Active",
    "Inactive",
    display_name="Invulnerable",
    on_change=trait_changed,
)

oidOneCritWonder = BoolOption(
    "Trait_Silly_Critical",
    True,
    "Active",
    "Inactive",
    display_name="One Crit Wonder",
    on_change=trait_changed,
)

oid_list = [
    oidArmored,
    oidArmsDealer,
    oidBougie,
    oidCentripetal,
    oidChainMaster,
    oidChromatic,
    oidColdHearted,
    oidContagious,
    oidDeflector,
    oidElementalEater,
    oidExperienced,
    oidFortified,
    oidHealthy,
    oidImmovable,
    oidInvisible,
    oidInvulnerable,
    oidLeaking,
    oidOneCritWonder,
    #oidLineDrive,
    oidQuartermaster,
    oidQuickened,
    oidRegenerative,
    oidShielded,
    oidStrong,
    oidTicking,
    oidTricky,
    oidVampiric,
    oidVengeful,
    oidWealthy,
]

build_mod(options=oid_list, on_enable=mod_enabled)