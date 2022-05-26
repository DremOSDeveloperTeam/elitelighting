# A (mostly) standalone script to control lights according to events in Elite: Dangerous.
# Coded in two afternoons with lots of coffee by Katie.
# This is meant to be a personal project, so I didn't really bother with expandability and such.
# Perhaps I'll revisit this in the future and make it so it can be expended upon easier. Don't count on it.
#
# (C) Innovation Science 2022

try:
    import tinytuya
except ModuleNotFoundError:
    print("You MUST install tinytuya first.")
    print("pip install tinytuya OR python -m pip install tinytuya")
    exit()

import time
import random
import json
import os

Version = "0.1"

# Use the classes below to configure your lights.
# You MUST go through the following setup process: https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys
class PortLight:
    # Actual light config.
    DeviceID: str =     "DEVICEID HERE"
    IP: str =           "LOCAL.IP.ADDRESS.HERE"
    LocalID: str =      "LOCALID HERE"
    # Color config. I've left it as my own preferences, but commented out the defaults as well.
    red: int =          230
    green: int =        100
    blue: int =         235

class StarboardLight:
    DeviceID: str =     "DEVICEID HERE"
    IP: str =           "LOCAL.IP.ADDRESS.HERE"
    LocalID: str =      "LOCALID HERE"
    red: int =          230
    green: int =        100
    blue: int =         235

class HazardLight:
    DeviceID: str =     "DEVICEID HERE"
    IP: str =           "LOCAL.IP.ADDRESS.HERE"
    LocalID: str =      "LOCALID HERE"
    red: int =          255
    green: int =        0
    blue: int =         0

# Below are the colors for the default hud colors. I'm estimating again, but it's close enough.
# red: int =            255
# green: int =          100
# blue: int =           0


# Elite Dangerous flags

#ED_Docked =                 0x0000000000000001
#ED_Landed =                 0x0000000000000002
#ED_LandingGearDown =        0x0000000000000004
#ED_ShieldsUp =              0x0000000000000008
#ED_Supercruise =            0x0000000000000010
#ED_FlightAssistOff =        0x0000000000000020
#ED_HardpointsDeployed =     0x0000000000000040
#ED_InWing =                 0x0000000000000080

#ED_LightsOn =               0x0000000000000100
#ED_CargoScoopDeployed =     0x0000000000000200
#ED_SilentRunning =          0x0000000000000400
#ED_ScoopingFuel =           0x0000000000000800
#ED_SRVHandbrake =           0x0000000000001000
#ED_SRVTurret =              0x0000000000002000
#ED_SRVTurretRetracted =     0x0000000000004000
#ED_SRVDriveAssist =         0x0000000000008000

#ED_FSDMassLocked =          0x0000000000010000
#ED_FSDCharging =            0x0000000000020000
#ED_FSDCooldown =            0x0000000000040000
#ED_LowFuel =                0x0000000000080000
#ED_OverHeating =            0x0000000000100000
#ED_HasLatLong =             0x0000000000200000
#ED_IsInDanger =             0x0000000000400000
#ED_BeingInterdicted =       0x0000000000800000

#ED_InMainShip =             0x0000000001000000
#ED_InFighter =              0x0000000002000000
#ED_InSRV =                  0x0000000004000000
#ED_HudInAnalysisMode =      0x0000000008000000
#ED_NightVision =            0x0000000010000000

# Status file stuff
# StatusDir will usually be: "C:\\Users\\{YOUR USERNAME HERE}\\Saved Games\\Frontier Developments\\Elite Dangerous"
StatusDir = "C:\\Users\\Sam\\Saved Games\\Frontier Developments\\Elite Dangerous"
CurrentLog = ""
StatusJSON = ""
StatusFlags = 0x00000000
StatusFlagsStr = ""

# Makes the infinate loop... loop.
ContinueFlag = True

# States
DoFlicker = False
DoHazards = False
LightsOn = True
LightsDim = False
LastHullHealth = 0
CurrentHullHealth = 0


# Initialize light variables and set version
port = tinytuya.BulbDevice(PortLight.DeviceID, PortLight.IP, PortLight.LocalID, dev_type="default")
starboard = tinytuya.BulbDevice(StarboardLight.DeviceID, StarboardLight.IP, StarboardLight.LocalID, dev_type="default")
hazards = tinytuya.BulbDevice(HazardLight.DeviceID, HazardLight.IP, HazardLight.LocalID, dev_type="default")

# Set Tuya versions
port.set_version(3.3)
starboard.set_version(3.3)
hazards.set_version(3.3)

def SetupLights(): # Initializes lights
    # Set light modes to color
    port.set_mode(mode='colour')
    starboard.set_mode(mode='colour')
    hazards.set_mode(mode='colour')

    # Turn on the lights
    port.turn_on()
    starboard.turn_on()
    hazards.turn_on()

    # Set light colors
    port.set_colour(PortLight.red, PortLight.green, PortLight.blue)
    starboard.set_colour(StarboardLight.red, StarboardLight.green, StarboardLight.blue)
    hazards.set_colour(HazardLight.red, HazardLight.green, HazardLight.blue)

    # Set light brightness (port and starboard are dim, whereas hazard is bright.)
    port.set_brightness_percentage(brightness=1)
    starboard.set_brightness_percentage(brightness=1)
    hazards.set_brightness_percentage(brightness=100)

    # Turn off hazard.
    hazards.turn_off()

def NormalLights(): # Returns lights to normal operation (used when exiting)
    # Change lights back to white mode.
    port.set_mode(mode='white')
    starboard.set_mode(mode='white')
    hazards.set_mode(mode='white')

    # Set brightness to full to blind the user.
    port.set_brightness_percentage(brightness=100)
    starboard.set_brightness_percentage(brightness=100)
    hazards.set_brightness_percentage(brightness=100)

def FlickerLights():
    # So far, I've made it so there are four types of flickers possible (0 being no flicker.)
    choices = [0, 1, 2, 3, 4]
    choice = random.choice(choices) # Randomly choose a flicker type
    flickertime = random.random()   # Randomly choose a flicker time (0 to 1 sec)

    # Welcome to if-else hell! I'm using python 3.9.6 so no pattern matching for me, and I don't care enough to deal with dictionaries.
    # If you would like to add more flicker patterns, add them here and add a new number to the choices list.
    if(choice==0):
        # Nothing happens.
        pass
    elif(choice==1):
        # Flicker port
        port.turn_off()
        time.sleep(flickertime)
        port.turn_on()
    elif(choice==2):
        # Flicker starboard
        starboard.turn_off()
        time.sleep(flickertime)
        starboard.turn_on()
    elif(choice==3):
        # Flicker both, port first
        port.turn_off()
        starboard.turn_off()
        time.sleep(flickertime)
        port.turn_on()
        starboard.turn_on()
    elif(choice==4):
        starboard.turn_off()
        port.turn_off()
        time.sleep(flickertime)
        starboard.turn_on()
        port.turn_on()
    else:
        print("How did we get here?")

def MainLightsOn(): # Turns main (port and starboard) lights on
    port.turn_on()
    starboard.turn_on()

def MainLightsOff(): # Turns main (port and starboard) lights off
    port.turn_off()
    starboard.turn_off()

def DimAllLights():  # Dims all lights. Used when FSD is charging to make it look like it's heavily loading the powerplant.
    port.set_brightness_percentage(brightness=0)
    starboard.set_brightness_percentage(brightness=0)
    hazards.set_brightness_percentage(brightness=80)

def LightsStandard(): # Standard brightness configuration for lights.
    port.set_brightness_percentage(brightness=1)
    starboard.set_brightness_percentage(brightness=1)
    hazards.set_brightness_percentage(brightness=100)

def HazardsOn():      # Turns the hazard light on
    hazards.turn_on()

def HazardsOff():     # Turns the hazard light off
    hazards.turn_off()

def ReloadFlags():    # Reloads Elite: Dangerous status flags and sets flicker, hazard on/off, lights on/off, and dimming variables for later processing
    global StatusDir
    global StatusJSON
    global StatusFlags
    global StatusFlagsStr
    global DoFlicker
    global DoHazards
    global LightsOn
    global LightsDim
    global ContinueFlag
    
    # Open the status file
    f = open(StatusDir + "\\Status.json", "r")
    try:
        StatusJSON = json.loads(f.read()) # Read the json from the Status.json file. 
    except:
        pass # Sometimes it guffs up reading (JSONDecodeError), and I can't really fix this.
    else:                                               # This makes the logic below use the previous status flags if an exception is raised
        StatusFlags = "0x%8x" % StatusJSON["Flags"]     # Extrapolate the flags from the json file and make it a known length (8 hex digits)
    f.close() # Close Status.json

    try:
        # Convert the ship state (3rd from right) byte (LightsOn, Cargo Scoop Deployed, Silent Running, Scooping Fuel)
        ShipStateByte = bin(int(StatusFlagsStr[-3]))[2:].zfill(4)
        ShipStateByteStr = str(ShipStateByte)

        # Convert the FSD (5th from right) byte (FSD MassLocked, FSD Charging, FSD Cooldown, Low Fuel (<25%))
        FSDByte = bin(int(StatusFlagsStr[-5]))[2:].zfill(4)
        FSDByteStr = str(FSDByte)
        
        # Convert the hazards (6th from right) byte (Overheating (>100%), Has Lat Long, IsInDanger, Being Interdicted)
        HazardByte = bin(int(StatusFlagsStr[-6]))[2:].zfill(4)
        HazardByteStr = str(HazardByte)
        
        # If you would like to add more effects to the lights, add them here.

        if(HazardByteStr[-1] == "1" or LastHullHealth > CurrentHullHealth):
            DoFlicker = True                                # Overheating and taking damage causes lights to flicker
        else:
            DoFlicker = False

        if(int(StatusFlagsStr[-6]) > 0):                    # If there's any hazard, hazard light is turned on
            DoHazards = True
        else:
            DoHazards = False
        
        if(ShipStateByteStr[-3] == "1"):                    # Port and starboard lights turn off when rigged for silent running
            LightsOn = False
        else:
            LightsOn = True

        if(FSDByteStr[-2] == "1"):                          # Lights dim when the FSD is charging
            LightsDim = True
        else:
            LightsDim = False
    except ValueError:
        print("ValueError! More than likely, Elite: Dangerous is closed. Exiting.")
        ContinueFlag = False

def GetCurrentLog(): # Gets the most recent log file left by Elite: Dangerous.
    global StatusDir


    LogName = ""
    # Changes working dir to the saved games dir temporarily, remembering the original working dir
    OriginalDir = os.getcwd()
    os.chdir(StatusDir)
    StatusDirContents = sorted(os.listdir(StatusDir), key=os.path.getmtime) # Get and sort the "saved game" directory from newest first.
    os.chdir(OriginalDir)
    
    for f in (StatusDirContents):
        if(f[-4:] == ".log"): # Search for the newest .log file.
            LogName = f   # We found the file!
    
    print("Discovered current log file: " + f)
    
    return LogName # Return the newest log file.
    
def GetDamageStats(): # Extrapolates damage taken from the log file. I'm not sure if this works quite yet.
    global StatusDir
    global CurrentLog
    try:
        f = open(StatusDir + "\\" + CurrentLog, "r") # Open the log file
    except:
        print("Error opening log. Continuing.")      # Error checking for if the log file cannot be opened.
        return
    try:
        Lines = f.readlines()                        # This should never happen.
    except:
        print("Error reading lines from log. Continuing")
    f.close() # Close the log file

    i = 0
    tempjson = ""
    for line in reversed(Lines): # Scan in reversed for the newest loadout readings
        i += 1
        try:
            tempjson = json.loads(line) # Attempt to load the line as JSON.
        except:
            continue                    # I'm willing to bet that we will encounter a similar JSONDecodeError here on occasion, so we skip that line.
                                        # This will probably lead to issues, but I'm not too worried about it.

        if(tempjson["event"] == "Loadout"):
            return tempjson["HullHealth"] # Returns HullHealth from Loadout event.
    

        

def RunStates(): # Processes light effect variables set by ReloadFlags()
    if(DoFlicker):
        FlickerLights()

    if(DoHazards):
        HazardsOn()
    else:
        HazardsOff()

    if(LightsOn):
        MainLightsOn()
    else:
        MainLightsOff()

    if(LightsDim):
        DimAllLights()
    else:
        LightsStandard()


# Program initialization

print("Elite Lighting v. " + Version)
print("If the program crashes in this stage, you either need to open Elite: Dangerous first or configure the program.")
print("To configure the program, follow the instructions at: https://git.innovation-inc.org/Innovation/elitelighting")
print("You will also need to read alongside: https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys")
print("Failure to do so will cause a crash and may kill your cat(s).")
print("\n")

print("Setting up lights")
SetupLights() # Set up lights

print("Lights set up.")

print("Getting current Elite: Dangerous log")
CurrentLog = GetCurrentLog() # Get current Elite: Dangerous log

print("Ready. Press CTRL+C at any time to set lights back to normal operation.")

while ContinueFlag == True:
    try:
        LastHullHealth = CurrentHullHealth
        CurrentHullHealth = GetDamageStats()
        ReloadFlags()
        RunStates()
        time.sleep(0.25)
    except KeyboardInterrupt: # This makes it so CTRL+C begins the program exiting sequence, and so the program exits gracefully at any point during execution.
        break

HazardsOn() # Turn on hazards so that it isn't off when lights return to normal operation.

lightschoice = input("Would you like your lights off? Y/n > ") # Would you like to be light mode'd?
if(lightschoice != "n" and lightschoice != "N"):
    print("Turning off lights.")                               # No, I like having eyes.
    MainLightsOff()
    HazardsOff()

print("Returning lights to normal operation.")
NormalLights()                                                 # Return lights to normal operation (white mode, full brightness)
print("Goodbye.")
