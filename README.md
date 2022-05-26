# Elite Lighting
## A standalone script to control lights according to events in Elite: Dangerous.

### What will I need?
You will need three Tuya-compatible RGB light bulbs and a bit of patience.

### Setup
#### Light configuration
Setting up Elite Lighting is done by modifying the script itself, because I didn't care enough to make a setup.
Don't worry, it's quite simple.
First, open the file and start from the top. Press CTRL+F (or whatever keybind you use to find text) and search for `class PortLight`. This is the class for the port light, and contains configuration data for said port light.
You will see two similar classes below, named `StarboardLight` and `HazardLight`. These contain configuration data for the starbaord and hazard lights respectively.

Before we continue with configuration, please follow the [tintya setup wizard](https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys). This will give your the Device IDs, local IP addresses, and Local IDs for your lights, which are needed for the script to make them work.

Now that we have this information, we may continue configuring the script.
Let's say that the Device ID for your port light is `2407vbgerng885`, the IP address is `192.168.1.15`, and the Local ID is `9yt9er8ty0349tvyn7`. Don't try to use those numbers, I just mashed the keyboard for them.
You'll take this information and plug it into the `PortLight` class, like the following:
```
class PortLight:
    # Actual light config.
    DeviceID: str =     "2407vbgerng885"
    IP: str =           "192.168.1.15"
    LocalID: str =      "9yt9er8ty0349tvyn7"
    red: int =          230
    green: int =        100
    blue: int =         235
```
This light is now configured. Repeat the process for `StarboardLight` and `HazardLight`, and your setup should just work.

#### Color configuration
By default, the port and starboard lights are purple, These are the colors for my HUD, and are probably not the colors for yours. Get an RGB value that matches your liking and set the `red`, `green`, and `blue` values to the RGB values. For example, if you wanted it to match the default HUD colors:
```
red: int =            255
green: int =          100
blue: int =           0
```

If you want the hazard light to not be red, you can also change it with the same method.

### Troubleshooting
#### When I run tinytuya's wizard, the version on my lights say 3.1.
Some lights run a different version of Tuya than the next. By default, the script assumes the bulbs run 3.3, as all new Tuya devices run 3.3. If you have an older bulb, it may run 3.1. Search for `Set Tuya versions` and change 3.3 on the devices below this line to 3.1.
If you're mixing old and new bulbs, only change the versions for the bulbs that have the older versions, obviously.

Does that make sense? I'm really tired.
