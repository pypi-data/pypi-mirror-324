import thinqconnect.devices
from thinqconnect.const import DeviceType
from thinqconnect.devices.connect_device import ConnectDeviceProfile

DEVICE_PROFILES: dict[str, tuple[ConnectDeviceProfile, ConnectDeviceProfile | None]] = {
    DeviceType.AIR_CONDITIONER: (thinqconnect.devices.AirConditionerProfile, None),
    DeviceType.AIR_PURIFIER: (thinqconnect.devices.AirPurifierProfile, None),
    DeviceType.AIR_PURIFIER_FAN: (thinqconnect.devices.AirPurifierFanProfile, None),
    DeviceType.CEILING_FAN: (thinqconnect.devices.CeilingFanProfile, None),
    DeviceType.COOKTOP: (thinqconnect.devices.CooktopProfile, thinqconnect.devices.CooktopSubProfile),
    DeviceType.DEHUMIDIFIER: (thinqconnect.devices.DehumidifierProfile, None),
    DeviceType.DISH_WASHER: (thinqconnect.devices.DishWasherProfile, None),
    DeviceType.DRYER: (thinqconnect.devices.DryerProfile, None),
    DeviceType.HOME_BREW: (thinqconnect.devices.HomeBrewProfile, None),
    DeviceType.HOOD: (thinqconnect.devices.HoodProfile, None),
    DeviceType.HUMIDIFIER: (thinqconnect.devices.HumidifierProfile, None),
    DeviceType.KIMCHI_REFRIGERATOR: (
        thinqconnect.devices.KimchiRefrigeratorProfile,
        thinqconnect.devices.KimchiRefrigeratorSubProfile,
    ),
    DeviceType.MICROWAVE_OVEN: (thinqconnect.devices.MicrowaveOvenProfile, None),
    DeviceType.OVEN: (thinqconnect.devices.OvenProfile, thinqconnect.devices.OvenSubProfile),
    DeviceType.PLANT_CULTIVATOR: (
        thinqconnect.devices.PlantCultivatorProfile,
        thinqconnect.devices.PlantCultivatorSubProfile,
    ),
    DeviceType.REFRIGERATOR: (
        thinqconnect.devices.RefrigeratorProfile,
        thinqconnect.devices.RefrigeratorSubProfile,
    ),
    DeviceType.ROBOT_CLEANER: (thinqconnect.devices.RobotCleanerProfile, None),
    DeviceType.STICK_CLEANER: (thinqconnect.devices.StickCleanerProfile, None),
    DeviceType.STYLER: (thinqconnect.devices.StylerProfile, None),
    DeviceType.SYSTEM_BOILER: (thinqconnect.devices.SystemBoilerProfile, None),
    # DeviceType.WASHCOMBO_MAIN: ( thinqconnect.devices.WasherSubProfile, None),
    # DeviceType.WASHCOMBO_MINI: ( thinqconnect.devices.WasherSubProfile, None),
    # DeviceType.WASHCOMBO: ( thinqconnect.devices.WasherSubProfile, None),
    DeviceType.WASHER: (thinqconnect.devices.WasherProfile, thinqconnect.devices.WasherSubProfile),
    # DeviceType.WASHTOWER_WASHER: ( thinqconnect.devices.WasherProfile, None),
    # DeviceType.WASHTOWER_DRYER: ( thinqconnect.devices.DryerProfile, None),
    # DeviceType.WASHTOWER: ( thinqconnect.devices.WashTowerProfile, thinqconnect.devices.WasherSubProfile, thinqconnect.devices.DryerProfile),
    DeviceType.WATER_HEATER: (thinqconnect.devices.WaterHeaterProfile, None),
    DeviceType.WATER_PURIFIER: (thinqconnect.devices.WaterPurifierProfile, None),
    DeviceType.WINE_CELLAR: (thinqconnect.devices.WineCellarProfile, thinqconnect.devices.WineCellarSubProfile),
}
