import unittest
import main


class SmartHouseTest(unittest.TestCase):
    house = main.build_demo_house()

    def test_no_of_rooms(self):
        self.assertEqual(12, SmartHouseTest.house.get_no_of_rooms())  # add assertion here

    def test_area(self):
        self.assertEqual(156.55, SmartHouseTest.house.get_total_area())

    def test_no_devices(self):
        self.assertEqual(31, SmartHouseTest.house.get_no_of_devices())
        self.assertEqual(8, SmartHouseTest.house.get_no_of_sensors())
        self.assertEqual(23, SmartHouseTest.house.get_no_of_actuators())

    def test_listings(self):
        rooms = SmartHouseTest.house.get_all_rooms()
        self.assertEqual(12, len(rooms))
        devices = SmartHouseTest.house.get_all_devices()
        self.assertEqual(31, len(devices))
        dev15 = SmartHouseTest.house.find_device_by_serial_no("c28b6e75-d565-4678")
        kitchen = SmartHouseTest.house.get_room_with_device(dev15)
        self.assertTrue(dev15 in devices)
        self.assertTrue(kitchen in rooms)

    def test_retrieving_devices(self):
        self.assertEqual("Aktuator(f11bb4fc-ba74-49cd) TYPE: Smart Lys STATUS: OFF PRODUCT DETAILS: Fritsch Group Tresom Bright 1.0", SmartHouseTest.house.find_device_by_serial_no("f11bb4fc-ba74-49cd").__repr__())
        self.assertEqual("Sensor(e237beec-2675-4cb0) TYPE: Temperatursensor STATUS: 1.3 °C PRODUCT DETAILS: Moen Inc Prodder Ute 1.2", SmartHouseTest.house.find_device_by_serial_no("e237beec-2675-4cb0").__repr__())
        self.assertEqual("Aktuator(4eca6387-0767-4e4e) TYPE: Varmepumpe STATUS: OFF PRODUCT DETAILS: Osinski Inc Fintone XCX4AB", SmartHouseTest.house.find_device_by_serial_no("4eca6387-0767-4e4e").__repr__())

    def test_devices_in_room(self):
        dev15 = SmartHouseTest.house.find_device_by_serial_no("c28b6e75-d565-4678")
        kitchen = SmartHouseTest.house.get_room_with_device(dev15)
        devices = SmartHouseTest.house.get_all_devices_in_room(kitchen)
        self.assertEqual(8, len(devices))
        dev16 = SmartHouseTest.house.find_device_by_serial_no("4eca6387-0767-4e4e")
        self.assertTrue(dev16 in devices)
        self.assertEqual(kitchen, SmartHouseTest.house.get_room_with_device(dev16))

    def test_move_device(self):
        dev4 = SmartHouseTest.house.find_device_by_serial_no("6a36c71d-4f48-4eb4")
        guest1 = SmartHouseTest.house.get_room_with_device(dev4)
        dev24 = SmartHouseTest.house.find_device_by_serial_no("73902f8f-10b4-4738")
        guest2 = SmartHouseTest.house.get_room_with_device(dev24)
        SmartHouseTest.house.move_device(dev4, guest1, guest2)
        self.assertEqual(1, len(SmartHouseTest.house.get_all_devices_in_room(guest1)))
        self.assertEqual(2, len(SmartHouseTest.house.get_all_devices_in_room(guest2)))
        self.assertTrue(dev4 in SmartHouseTest.house.get_all_devices_in_room(guest2))
        self.assertFalse(dev4 in SmartHouseTest.house.get_all_devices_in_room(guest1))

    def test_actuators(self):
        dev25 = SmartHouseTest.house.find_device_by_serial_no("627ff5f3-f4f5-47bd")
        master_bedroom = SmartHouseTest.house.get_room_with_device(dev25)
        self.assertEqual(16.1, SmartHouseTest.house.get_temperature_in_room(master_bedroom))
        SmartHouseTest.house.turn_on_lights_in_room(master_bedroom)
        self.assertEqual("Aktuator(627ff5f3-f4f5-47bd) TYPE: Smart Lys STATUS: ON PRODUCT DETAILS: Fritsch Group Alphazap 2", dev25.__repr__())
        SmartHouseTest.house.set_temperature_in_room(master_bedroom, 20.5)
        self.assertEqual("Aktuator(eed2cba8-eb13-4023) TYPE: Varmepumpe STATUS: 20.5 °C PRODUCT DETAILS: Osinski Inc Fintone XCX2FF", SmartHouseTest.house.find_device_by_serial_no("eed2cba8-eb13-4023").__repr__())
        SmartHouseTest.house.turn_off_lights_in_room(master_bedroom)
        self.assertEqual("Aktuator(627ff5f3-f4f5-47bd) TYPE: Smart Lys STATUS: OFF PRODUCT DETAILS: Fritsch Group Alphazap 2", dev25.__repr__())


if __name__ == '__main__':
    unittest.main()
