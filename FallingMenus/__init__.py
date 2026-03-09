from mods_base import build_mod, get_pc, keybind,SpinnerOption


@keybind("Open Menu Key",description="Set this to your default status menu key, example Tab")
def open_menu():
    pc = get_pc()
    if not pc.Pawn or not pc.Pawn.OakCharacterMovement or "OakVehicle" in str(pc.Pawn):
        return
    if pc.Pawn.OakCharacterMovement.MovementMode != 1:
        pc.Pawn.OakCharacterMovement.SetMovementMode(1,0)
        match oidMenu.value:
            case "Map":
                pc.ToggleMapMenu()
            case "Missions":
                pc.ToggleMissionLogMenu()
            case "Inventory":
                pc.OpenInventoryMenu()
            case "Skills":
                pc.OpenSkillsMenu()

oidMenu = SpinnerOption(
    "Menu to Open",
    "Map",
    ["Map", "Missions", "Inventory", "Skills"],
    description="Pick which menu opens."
)


mod = build_mod()