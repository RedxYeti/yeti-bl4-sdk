from mods_base import build_mod, SliderOption, BoolOption, SpinnerOption, command
from unrealsdk import find_all, make_struct, find_class
from unrealsdk.unreal import UObject, notify_changes
from random import uniform
from argparse import Namespace

KismetStringLibrary = find_class("KismetStringLibrary").ClassDefaultObject
TimeOfDayBlueprintLibrary = find_class("TimeOfDayBlueprintLibrary").ClassDefaultObject

def _get_tod() -> UObject:
    return find_all("WorldTimeOfDayActor", False)[-1]#type: ignore


def set_time(new_time:float) -> None:
    tod = _get_tod()
    with notify_changes():
        tod.TimeOfDay = new_time
    tod.OnRep_TimeOfDay()
    return


def set_weather(region:str,new_layer:str):
    new_layer = new_layer.replace(" ", "")
    finalized_weather = ""
    finalized_min = oidNewWeatherMinTime.value
    finalized_max = oidNewWeatherMaxTime.value
    match region.lower():
        case "fadefields":
            match new_layer.lower():
                case "default":
                    finalized_weather = "G_Clear"
                    finalized_min = 0
                    finalized_max = 1
                case "clear":
                    finalized_weather = "G_Clear"
                case "foggy":
                    finalized_weather = "G_Foggy"
                case "rainlight":
                    finalized_weather = "G_Rain_Light"
                case "rainmedium":
                    finalized_weather = "G_Rain_Medium"
                case "rainheavy":
                    finalized_weather = "G_Rain_Heavy"
                case "pollen":
                    finalized_weather = "G_Pollen_Light"
        case "carcadia":
            match new_layer.lower():
                case "default":
                    finalized_weather = "S_Clear"
                    finalized_min = 0
                    finalized_max = 1
                case "clear":
                    finalized_weather = "S_Clear"
                case "foggy":
                    finalized_weather = "S_Foggy"
                case "dustlight":
                    finalized_weather = "S_Dust_Light"
                case "dustmedium":
                    finalized_weather = "S_Dust_Medium"
                case "dustheavy":
                    finalized_weather = "S_Dust_Heavy"
                case "poison":
                    finalized_weather = "S_Poison"
        case "terminus":
            match new_layer.lower():
                case "default":
                    finalized_weather = "M_Clear"
                    finalized_min = 0
                    finalized_max = 1
                case "clear":
                    finalized_weather = "M_Clear"
                case "snowlight":
                    finalized_weather = "M_Snow_Light"
                case "snowmedium":
                    finalized_weather = "M_Snow_Medium"
                case "snowheavy":
                    finalized_weather = "M_Snow_Heavy"
        case "event":
            match new_layer.lower():
                case "snow":
                    finalized_weather = "Global_Snow"
                case "bloodrain":
                    finalized_weather = "Global_BLOODRAIN"


    #['Prison_Intro', 'Grasslands_Start', 'Grasslands_Default_Cycle', 'Mountains_Default_Cycle', 'Mountains_Fortress_Default_Cycle', 'Shattered_Lands_Default_Cycle', 'Return_From_Elpis', 'Shattered_Lands_Crater_Default_Cycle']

    if finalized_weather == "":
        print(f"Region or Weather is incorrect. check spelling and options.")
        set_weather_help()
        return
    
    weather_name = KismetStringLibrary.Conv_StringToName(finalized_weather)
    tod = _get_tod()

    TimeOfDayBlueprintLibrary.TransitionToLayer(tod, "", 0, True)
    
    new_weather_layer = make_struct("TimeOfDayWeatherForecast",
                                    layer=weather_name,
                                    Chance=1.0,
                                    TransitionTime=1,
                                    MinimumDuration=finalized_min,
                                    bLimitDuration=True,
                                    MaxDuration=finalized_max,
                                    )
    tod.TransitionWeatherLayer(new_weather_layer)
    tod.WorldBaseLayerOverrides = []




oidNewWeatherMinTime = SliderOption(
    "New Weather Minimum Time",
    300,
    0,
    99999,
    1,
    description="Minimum time in seconds the new weather will stay."
)

oidNewWeatherMaxTime = SliderOption(
    "New Weather Maximum Time",
    600,
    1,
    99999,
    1,
    description="Maximum time in seconds the new weather will stay."
)

@command("settime")
def set_time_command(args: Namespace) -> None:
    if not args.time:
        return
    new_time = float(args.time)
    if new_time == "1.01":
        new_time = uniform(0,1)
    set_time(float(args.time))
set_time_command.add_argument("time", help="Values accepted 0-1, 1.01 for a random time.")

@command("setweather")
def set_weather_command(args: Namespace) -> None:
    if not args.region or not args.weather_type:
        return
    set_weather(args.region, args.weather_type)
set_weather_command.add_argument("region", help="Values accepted fadefields, carcadia or terminus")
set_weather_command.add_argument("weather_type", help="Values accepted vary per region, use command setweatherhelp")

@command("pausetime")
def pause_time(args: Namespace) -> None:
    _get_tod().bTimeOfDayPaused = True

@command("unpausetime")
def unpause_time(args: Namespace) -> None:
    _get_tod().bTimeOfDayPaused = False

@command("setweatherhelp")
def set_weather_help_command(args: Namespace) -> None:
    set_weather_help()

def set_weather_help():
    print("==========All Weather Options==========")
    print("Usage: setweather region weathertype")
    print("")
    print("fadefields clear")
    print("fadefields foggy")
    print("fadefields rainlight")
    print("fadefields rainmedium")
    print("fadefields rainheavy")
    print("fadefields pollen")
    print("")
    print("carcadia clear")
    print("carcadia foggy")
    print("carcadia dustlight")
    print("carcadia dustmedium")
    print("carcadia dustheavy")
    print("carcadia poison")
    print("")
    print("terminus clear")
    print("terminus snowlight")
    print("terminus snowmedium")
    print("terminus snowheavy")
    print("")
    print("event snow")
    print("event bloodrain")
    print("")
    print("use any region and 'default' to reset weather")
    print("=======================================")


mod_options = [
    oidNewWeatherMinTime,
    oidNewWeatherMaxTime,
]

mod = build_mod(options=mod_options)