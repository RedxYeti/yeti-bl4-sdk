from unrealsdk import find_all
from unrealsdk.hooks import Type
from mods_base import build_mod, SETTINGS_DIR, hook, ENGINE
import os

console_history_path:str = ""
saved_history:list = []
prep_finished:bool = False

def prep_history() -> None:
    global console_history_path, prep_finished, saved_history
    console_history_dir = os.path.join(SETTINGS_DIR, "console_history")

    if not os.path.exists(console_history_dir):
        os.makedirs(console_history_dir)

    console_history_path = os.path.join(console_history_dir, "console_history.txt")

    if not os.path.exists(console_history_path):
        with open(console_history_path, "w") as file:
            file.write("")
    else:
        with open(console_history_path, "r") as file:
            history = [line.strip() for line in file if line.strip()]
    
        ENGINE.GameViewport.ViewportConsole.HistoryBuffer = history
        saved_history = history

    prep_finished = True
    

def update_history(current_history):
    global saved_history
    saved_history = current_history
    with open(console_history_path, "w") as file:
        for command in current_history:
            file.write(command + "\n")


@hook("/Script/Engine.CameraModifier:BlueprintModifyCamera", Type.POST)
def save_command(*_):
    if not prep_finished:
        prep_history()
        return
    
    current_history = list(ENGINE.GameViewport.ViewportConsole.HistoryBuffer)

    if saved_history != current_history:
        update_history(current_history)


build_mod()