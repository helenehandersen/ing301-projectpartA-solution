from devices import Device, LightBulb, TemperatureSensor, HeatOven, Sensor, Actuator, HeatPump, DeviceVisitor
from typing import List, Optional


class Room:

    def __init__(self, area: float, name: str = None):
        self.area = area
        self.name = name
        self.devices = []

    def find_device(self, serial_no: str) -> Optional[Device]:
        for device in self.devices:
            if device.serial_no == serial_no:
                return device
        return None

    def get_devices(self) -> List[Device]:
        return self.devices

    def register_device(self, device: Device):
        self.devices.append(device)

    def unregister_device(self, device: Device):
        self.devices.remove(device)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.find_device(item)
        else:
            return None

    def __contains__(self, item):
        return item in self.devices

    def __len__(self):
        return len(self.devices)

    # Iterator Pattern: Room is a collection of devices
    def __iter__(self):
        return self.devices.__iter__()

    def __repr__(self):
        return f"{self.name} ({self.area} m^2)"


class Floor:

    def __init__(self, floor_no: int):
        self.floor_no = floor_no
        self.rooms = []

    def get_no_of_rooms(self):
        return len(self.rooms)

    def __len__(self):
        return self.get_no_of_rooms()

    # Iterator Pattern: Floor is a collection of rooms
    def __iter__(self):
        return self.rooms.__iter__()

    def get_floor_area(self):
        result = 0.0
        for room in self.rooms:
            result += room.area
        return result

    def find_device(self, serial_no: str) -> Optional[Device]:
        for room in self.rooms:
            device = room.find_device(serial_no)
            if device:
                return device
        return None


class TurnOnLightsVisitor(DeviceVisitor):

    def handle_light_bulp(self, actuator):
        actuator.turn_on()


class TurnOffLightsVisitor(DeviceVisitor):

    def handle_light_bulp(self, actuator):
        actuator.turn_off()


class GetTemperatureVisitor(DeviceVisitor):

    def __init__(self):
        self.temperature = None

    def handle_temperature_sensor(self, sensor):
        self.temperature = sensor.get_current_value()

    def get_result(self) -> Optional[float]:
        return self.temperature


class SetTemperatureVisitor(DeviceVisitor):

    def __init__(self, temperature: float):
        self.temperature = temperature

    def handle_floor_heating(self, actuator):
        actuator.set_temperature(self.temperature)

    def handle_heat_pump(self, actuator):
        actuator.set_temperature(self.temperature)

    def handle_heat_oven(self, actuator):
        actuator.set_temperature(self.temperature)


# Composite Pattern: A house consists of floors which consists of rooms which consists of devices
class SmartHouse:

    def __init__(self):
        self.floors = []

    def create_floor(self) -> Floor:
        f = Floor(len(self.floors) + 1)
        self.floors.append(f)
        return f

    def create_room(self, floor_no: int, area: float, name: str = None) -> Room:
        if not floor_no <= len(self.floors) or floor_no <= 0:  # We do not have basements right now
            raise LookupError(f"Floor with no {floor_no} does not exist!")
        f = self.floors[floor_no - 1]
        r = Room(area, name)
        f.rooms.append(r)
        return r

    def get_no_of_rooms(self) -> int:
        result = 0
        for floor in self.floors:
            result += len(floor)
        return result

    def get_all_devices(self) -> List[Device]:
        result = []
        for floor in self.floors:
            for room in floor:
                result.extend(room.devices)
        return result

    def get_all_rooms(self) -> List[Room]:
        result = []
        for floor in self.floors:
            result.extend(floor.rooms)
        return result

    def get_total_area(self) -> float:
        result = 0.0
        for floor in self.floors:
            result += floor.get_floor_area()
        return result

    def register_device(self, device: Device, room: Room):
        room.register_device(device)

    def get_no_of_devices(self):
        counter = 0
        for floor in self.floors:
            for room in floor:
                counter += len(room)
        return counter

    def get_no_of_sensors(self):
        counter = 0
        for floor in self.floors:
            for room in floor:
                counter += sum([1 for d in room if isinstance(d, Sensor)])
        return counter

    def get_no_of_actuators(self):
        counter = 0
        for floor in self.floors:
            for room in floor:
                counter += sum([1 for d in room if isinstance(d, Actuator)])
        return counter

    def move_device(self, device: Device, from_room: Room, to_room: Room):
        from_room.unregister_device(device)
        to_room.register_device(device)

    def find_device_by_serial_no(self, serial_no: str) -> Optional[Device]:
        for floor in self.floors:
            device = floor.find_device(serial_no)
            if device:
                return device
        return None

    def get_room_with_device(self, device: Device):
        for floor in self.floors:
            for room in floor:
                if device in room:
                    return room
        return None

    def get_all_devices_in_room(self, room: Room) -> List[Device]:
        return room.get_devices()

    def turn_on_lights_in_room(self, room: Room):
        v = TurnOnLightsVisitor()
        for device in [d for d in room if isinstance(d, LightBulb)]:
            device.accept(v)

    def turn_off_lights_in_room(self, room: Room):
        v = TurnOffLightsVisitor()
        for device in [d for d in room if isinstance(d, LightBulb)]:
            device.accept(v)

    def get_temperature_in_room(self, room: Room) -> float:
        v = GetTemperatureVisitor()
        for device in self.get_all_devices_in_room(room):
            device.accept(v)
        return v.get_result()

    def set_temperature_in_room(self, room: Room, temperature: float):
        v = SetTemperatureVisitor(temperature)
        for device in self.get_all_devices_in_room(room):
            device.accept(v)
