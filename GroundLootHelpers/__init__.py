from typing import Any 
from mods_base import hook, build_mod, SliderOption, BoolOption, get_pc, keybind
from unrealsdk import find_class, make_struct, find_all
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct, IGNORE_STRUCT

import math

MAX_PER_CIRCLE = 35
CIRCLE_SPACING = 150.0
BASE_RADIUS = 200.0

usables = ["Health", "ArmorShard", "Ammo", "ammo", "Money", "Eridium", "ShieldBooster"]

def GetIoTD() -> list:
    iotds = []
    pc = get_pc()
    for machine in find_all("OakVendingMachine", False):

        if not machine or machine == machine.Class.ClassDefaultObject:
            continue
        current_iotd = machine.GetIOTDForPlayer(pc)
        if current_iotd:
            iotds.append(current_iotd)
    return iotds



def get_sorted_ground_loot() -> dict:
    current_ground_loot = {
        "Pickups": [],
        "Gear": [],
    }
    iotd_pickups = GetIoTD()
    for inv in find_all("InventoryPickup", False):
        if not inv or inv == inv.Class.ClassDefaultObject or not inv.RootPrimitiveComponent or inv in iotd_pickups:
            continue

        inv.RootPrimitiveComponent.SetSimulatePhysics(True)

        inv_str = str(inv.BodyData)

        if "Pickups" in inv_str:
            current_ground_loot["Pickups"].append(inv)
            continue

        if not inv.BodyData:
            was_usable = False
            num_materials = inv.RootPrimitiveComponent.GetNumMaterials()

            for i in range(num_materials):
                if was_usable:
                    break

                mat = inv.RootPrimitiveComponent.GetMaterial(i)
                if not mat:
                    continue

                for usable in usables:
                    if usable in mat.Name:
                        current_ground_loot["Pickups"].append(inv)
                        was_usable = True
                        break

            if was_usable:
                continue

        if "Gear" in inv_str:
            current_ground_loot["Gear"].append(inv)
            continue

    return current_ground_loot


delete_loot_location = make_struct("Vector", X=100000,Y=100000,Z=-1000000000)
@keybind("Delete Loot")
def delete_loot():
    pickups = get_sorted_ground_loot()
    all_ground_loot = pickups["Pickups"] + pickups["Gear"]
    for inv in all_ground_loot:
        inv.RootPrimitiveComponent.SetSimulatePhysics(True)
        inv.K2_TeleportTo(delete_loot_location, IGNORE_STRUCT)


@keybind("Teleport Loot")
def teleport_loot():
    player_location = get_pc().Pawn.K2_GetActorLocation()
    player_location.Z -= 40

    all_ground_loot = get_sorted_ground_loot()
    for inv in all_ground_loot["Pickups"]:
        inv.K2_TeleportTo(player_location, IGNORE_STRUCT)

    item_index = 0
    for inv in all_ground_loot["Gear"]:
        ring = item_index // MAX_PER_CIRCLE
        pos_in_ring = item_index % MAX_PER_CIRCLE

        angle_offset = 0.0
        if pos_in_ring != 0:
            angle_offset = (2.0 * math.pi / MAX_PER_CIRCLE) * pos_in_ring

        radius = BASE_RADIUS + ring * CIRCLE_SPACING

        player_rot = get_pc().Pawn.K2_GetActorRotation()
        yaw_rad = math.radians(player_rot.Yaw)

        forward_x = math.cos(yaw_rad)
        forward_y = math.sin(yaw_rad)

        right_x = -math.sin(yaw_rad)
        right_y =  math.cos(yaw_rad)

        cos_a = math.cos(angle_offset)
        sin_a = math.sin(angle_offset)

        offset_x = (forward_x * radius * cos_a) + (right_x * radius * sin_a)
        offset_y = (forward_y * radius * cos_a) + (right_y * radius * sin_a)
        offset_z = 0

        new_x = player_location.X + offset_x
        new_y = player_location.Y + offset_y
        new_z = player_location.Z + offset_z

        new_location = make_struct("Vector", X=new_x, Y=new_y, Z=new_z)

        dir_x = new_x - player_location.X
        dir_y = new_y - player_location.Y
        dir_z = new_z - player_location.Z

        dir_length = math.sqrt(dir_x * dir_x + dir_y * dir_y + dir_z * dir_z)

        if dir_length < 0.0001:
            dir_length = 0.0001

        dir_x /= dir_length
        dir_y /= dir_length
        dir_z /= dir_length

        yaw = math.degrees(math.atan2(dir_y, dir_x))

        horizontal_len = math.sqrt(dir_x * dir_x + dir_y * dir_y)
        pitch = math.degrees(math.atan2(dir_z, horizontal_len))

        roll = 0

        rotation = make_struct("Rotator", Pitch=pitch, Yaw=yaw, Roll=roll)

        inv.K2_TeleportTo(new_location, rotation)

        item_index += 1
    return


build_mod(keybinds=[teleport_loot,delete_loot])