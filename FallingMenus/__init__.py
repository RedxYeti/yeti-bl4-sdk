from mods_base import build_mod, get_pc, keybind

@keybind("Open Menu Key",description="Set this to your default status menu key, example Tab")
def open_menu():
    pc = get_pc()
    if not pc.Pawn or not pc.Pawn.OakCharacterMovement or pc.Pawn.Class.Name == "OakVehicle":
        return
    if pc.Pawn.OakCharacterMovement.MovementMode == 3:
        pc.Pawn.OakCharacterMovement.SetMovementMode(1,0)

mod = build_mod()