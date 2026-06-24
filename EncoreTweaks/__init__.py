from typing import Any 
from mods_base import hook, build_mod, BoolOption, get_pc, ENGINE
from unrealsdk import find_class, find_all
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct, FGbxDefPtr, IGNORE_STRUCT #type: ignore


GameplayStatics = find_class("GameplayStatics").ClassDefaultObject
DamageStatics = find_class("DamageStatics").ClassDefaultObject
GbxSkillComponentFunctions_ActionSkill = find_class("GbxSkillComponentFunctions_ActionSkill").ClassDefaultObject
WeaponStatics = find_class("WeaponStatics").ClassDefaultObject


@hook("/Game/InteractiveObjects/GameSystemMachines/BossReplay/Script_BossReplay.Script_BossReplay_C:GbxActorScriptEvt__UsableActorState_K2_OnUsed",Type.PRE)
def Script_BossReplay_C_OnUsed_EncoreTweaks(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    if oidKillAll.value:
        get_pc().ServerActivateDevPerk(3)

    vending = GameplayStatics.SpawnObject(find_class("OakVendingMachine"), get_pc())
    vending.ShopDef = FGbxDefPtr('InventoryShop_VendingMachine_Resupply', 'OakInventoryShopDef')
    vendor = GameplayStatics.FinishSpawningActor(vending, IGNORE_STRUCT, 1)[0]
    
    for player in ENGINE.GameViewport.World.GameState.PlayerArray:
        pawn = player.PawnPrivate

        pawn.Owner.ServerOnRefillAmmo(vendor,IGNORE_STRUCT,False)

        healthtypes = pawn.HealthState.HealthTypeStates
        for index, state in enumerate(pawn.HealthState.HealthTypeStates):
            if state.HealthType.DisplayColor < 3:
                DamageStatics.RefillHealthPercent(get_pc().Pawn, healthtypes[index].HealthType, 100, 100)

        GbxSkillComponentFunctions_ActionSkill.RefillCooldown(pawn, 1.0, 0)


oidKillAll = BoolOption(
    "Kill All on Reset",
    False,
    "On",
    "Off",
    description="Using the Encore Machine will kill all the enemies in the area first."
)

build_mod()