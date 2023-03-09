from persistence import SmartHousePersistence
from smarthouse import SmartHouse
from devices import *
from pathlib import Path


def load_demo_house_devices_map():
    file_path = str(Path(__file__).parent.absolute()) + "/demohus-devices.csv"
    result = {}
    with open(file_path, "r") as f:
        f.readline()  # header line: No,Typ,Produsent,Produkt Navn,Serienummer
        for line in f.readlines():
            data = line.split(",")
            result[int(data[0])] = (data[2], data[3], data[4].strip())  # Supplier, Product, Serial No
    return result


def load_demo_house(persistence: SmartHousePersistence) -> SmartHouse:
    # Get all rooms
    rooms_query = "SELECT id, floor, area, name FROM rooms"
    rooms_data = persistence.cursor.execute(rooms_query).fetchall()

    #Get all devices
    devices_query = "SELECT id, room, type, producer, product_name, serial_no FROM devices"
    devices_data = persistence.cursor.execute(devices_query).fetchall()

    result = SmartHouse()

    # Register rooms
    floors = {}
    for room_row in rooms_data:
        room_id, floor_no, area, name = room_row
        if floor_no not in floors:
            floor = result.create_floor()
            floors[floor_no] = floor
        else:
            floor = floors[floor_no]
        room = result.create_room(floor_no, area, name)

    #Register devices
    devices = {}
    for device_row in devices_data:
        device_id, room_id, device_type, producer, product_name, serial_no = device_row
        if device_id not in devices:
            device = result.register_device(device_id, room)
        device = result.get_no_of_devices()


    # TODO read rooms, devices and their locations from the database
    return result


def build_demo_house() -> SmartHouse:
    house = SmartHouse()

    # Creating two floors
    house.create_floor()
    house.create_floor()

    # Creating rooms
    stue = house.create_room(1, 39.75, "Living Room / Kitchen")
    entre = house.create_room(1, 13.5, "Entrance")
    guest1 = house.create_room(1, 8, "Guest Room 1")
    bath1 = house.create_room(1, 6.3, "Bathroom 1")
    garage = house.create_room(1, 19, "Garage")
    office = house.create_room(2, 11.75, "Office")
    bath2 = house.create_room(2, 9.25, "Bathroom 2")
    guest2 = house.create_room(2, 8, "Guest Room 2")
    house.create_room(2, 10, "Gang")
    guest3 = house.create_room(2, 10, "Guest Room 3")
    dress = house.create_room(2, 4, "Dressing Room")
    bed = house.create_room(2, 17, "Master Bedroom")

    # Loading Product information and serial numbers from a CSV file so that I do not have to type them
    devices_map = load_demo_house_devices_map()

    # Creating 31 devices
    device1 = LightBulb(serial_no=devices_map[1][2], producer=devices_map[1][0], product_type=devices_map[1][1])
    device2 = LightBulb(serial_no=devices_map[2][2], producer=devices_map[2][0], product_type=devices_map[2][1])
    device3 = HumiditySensor(serial_no=devices_map[3][2], producer=devices_map[3][0], product_type=devices_map[3][1])
    device4 = LightBulb(serial_no=devices_map[4][2], producer=devices_map[4][0], product_type=devices_map[4][1])
    device5 = LightBulb(serial_no=devices_map[5][2], producer=devices_map[5][0], product_type=devices_map[5][1])
    device6 = SmartCharger(serial_no=devices_map[6][2], producer=devices_map[6][0], product_type=devices_map[6][1])
    device7 = HeatOven(serial_no=devices_map[7][2], producer=devices_map[7][0], product_type=devices_map[7][1])
    device8 = TemperatureSensor(serial_no=devices_map[8][2], producer=devices_map[8][0], product_type=devices_map[8][1])
    device9 = LightBulb(serial_no=devices_map[9][2], producer=devices_map[9][0], product_type=devices_map[9][1])
    device10 = LightBulb(serial_no=devices_map[10][2], producer=devices_map[10][0], product_type=devices_map[10][1])
    device11 = SmartMeter(serial_no=devices_map[11][2], producer=devices_map[11][0], product_type=devices_map[1][1])
    device12 = TemperatureSensor(serial_no=devices_map[12][2], producer=devices_map[12][0],
                                 product_type=devices_map[12][1])
    device13 = LightBulb(serial_no=devices_map[13][2], producer=devices_map[13][0], product_type=devices_map[13][1])
    device14 = SmartMeter(serial_no=devices_map[14][2], producer=devices_map[14][0], product_type=devices_map[14][1])
    device15 = SmartOutlet(serial_no=devices_map[15][2], producer=devices_map[15][0], product_type=devices_map[15][1])
    device16 = HeatPump(serial_no=devices_map[16][2], producer=devices_map[16][0], product_type=devices_map[16][1])
    device17 = AirQualitySensor(serial_no=devices_map[17][2], producer=devices_map[17][0],
                                product_type=devices_map[17][1])
    device18 = SmartOutlet(serial_no=devices_map[18][2], producer=devices_map[18][0], product_type=devices_map[18][1])
    device19 = HeatOven(serial_no=devices_map[19][2], producer=devices_map[19][0], product_type=devices_map[19][1])
    device20 = SmartOutlet(serial_no=devices_map[20][2], producer=devices_map[20][0], product_type=devices_map[20][1])
    device21 = HumiditySensor(serial_no=devices_map[21][2], producer=devices_map[21][0],
                              product_type=devices_map[21][1])
    device22 = Dehumidifier(serial_no=devices_map[22][2], producer=devices_map[22][0], product_type=devices_map[22][1])
    device23 = FloorHeatingPanel(serial_no=devices_map[23][2], producer=devices_map[23][0],
                                 product_type=devices_map[23][1])
    device24 = HeatOven(serial_no=devices_map[24][2], producer=devices_map[24][0], product_type=devices_map[24][1])
    device25 = LightBulb(serial_no=devices_map[25][2], producer=devices_map[25][0], product_type=devices_map[25][1])
    device26 = LightBulb(serial_no=devices_map[26][2], producer=devices_map[26][0], product_type=devices_map[26][1])
    device27 = HeatPump(serial_no=devices_map[27][2], producer=devices_map[27][0], product_type=devices_map[27][1])
    device28 = TemperatureSensor(serial_no=devices_map[28][2], producer=devices_map[28][0],
                                 product_type=devices_map[28][1])
    device29 = LightBulb(serial_no=devices_map[29][2], producer=devices_map[29][0], product_type=devices_map[29][1])
    device30 = LightBulb(serial_no=devices_map[30][2], producer=devices_map[30][0], product_type=devices_map[30][1])
    device31 = HeatOven(serial_no=devices_map[31][2], producer=devices_map[31][0], product_type=devices_map[31][1])

    # Sensor start values according to: https://github.com/selabhvl/ing301public/blob/main/project/demo.md#startverdier
    device3.moisture = 68
    device8.temperature = 1.3
    device11.energy_consumption = 0
    device12.temperature = 18.1
    device14.energy_consumption = 1.5
    device17.air_quality = 0.08
    device21.humidity = 52
    device28.temperature = 16.1

    # Registering devices in the right room
    house.register_device(device1, stue)
    house.register_device(device2, stue)
    house.register_device(device3, bath1)
    house.register_device(device4, guest1)
    house.register_device(device5, garage)
    house.register_device(device6, garage)
    house.register_device(device7, guest1)
    house.register_device(device8, entre)
    house.register_device(device9, entre)
    house.register_device(device10, entre)
    house.register_device(device11, stue)
    house.register_device(device12, stue)
    house.register_device(device13, entre)
    house.register_device(device14, entre)
    house.register_device(device15, stue)
    house.register_device(device16, stue)
    house.register_device(device17, stue)
    house.register_device(device18, stue)
    house.register_device(device19, office)
    house.register_device(device20, office)
    house.register_device(device21, bath2)
    house.register_device(device22, bath2)
    house.register_device(device23, bath2)
    house.register_device(device24, guest2)
    house.register_device(device25, bed)
    house.register_device(device26, bed)
    house.register_device(device27, bed)
    house.register_device(device28, bed)
    house.register_device(device29, bed)
    house.register_device(device30, dress)
    house.register_device(device31, guest3)

    return house


def do_device_list(smart_house: SmartHouse):
    print("Listing Devices...")
    idx = 0
    for d in smart_house.get_all_devices():
        print(f"{idx}: {d}")
        idx += 1


def do_room_list(smart_house: SmartHouse):
    print("Listing Rooms...")
    idx = 0
    for r in smart_house.get_all_rooms():
        print(f"{idx}: {r}")
        idx += 1


def do_find(smart_house: SmartHouse):
    print("Please enter serial no: ")
    serial_no = input()
    device = smart_house.find_device_by_serial_no(serial_no)
    if device:
        devices = smart_house.get_all_devices()
        rooms = smart_house.get_all_rooms()
        room = smart_house.get_room_with_device(device)
        device_idx = devices.index(device)
        room_idx = rooms.index(room)
        print(f"Device No {device_idx}:")
        print(device)
        print(f"is located in room No {room_idx}:")
        print(room)
    else:
        print(f"Could not locate device with serial no {serial_no}")


def do_move(smart_house):
    devices = smart_house.get_all_devices()
    rooms = smart_house.get_all_rooms()
    print("Please choose device:")
    device_id = input()
    device = None
    if device_id.isdigit():
        device = devices[int(device_id)]
    else:
        device = smart_house.find_device_by_serial_no(device_id)
    if device:
        print("Please choose target room")
        room_id = input()
        if room_id.isdigit() and rooms[int(room_id)]:
            to_room = rooms[int(room_id)]
            from_room = smart_house.get_room_with_device(device)
            smart_house.move_device(device, from_room, to_room)
        else:
            print(f"Room with no {room_id} does not exist!")
    else:
        print(f"Device wit id '{device_id}' does not exist")


def main(smart_house: SmartHouse):
    print("************ Smart House Control *****************")
    print(f"No of Rooms:       {smart_house.get_no_of_rooms()}")
    print(f"Total Area:        {smart_house.get_total_area()}")
    print(
        f"Connected Devices: {smart_house.get_no_of_devices()} ({smart_house.get_no_of_sensors()} Sensors | {smart_house.get_no_of_actuators()} Actuators)")
    print("**************************************************")
    print()
    print("Management Interface v.0.1")
    while (True):
        print()
        print("Please select one of the following options:")
        print("- List all devices in the house (l)")
        print("- List all rooms in the house (r) ")
        print("- Find a device via its serial number (f)")
        print("- Move a device from one room to another (m)")
        print("- Quit (q)")
        char = input()
        if char == "l":
            do_device_list(smart_house)
        elif char == "r":
            do_room_list(smart_house)
        elif char == "f":
            do_find(smart_house)
        elif char == "m":
            do_move(smart_house)
        elif char == "q":
            break
        else:
            print(f"Error! Could not interpret input '{char}'!")


if __name__ == '__main__':
    house = build_demo_house()
    main(house)
