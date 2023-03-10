import abc
from typing import Optional
from sqlite3 import Connection

# Visitor Design Patter
class DeviceVisitor:

    def handle_temperature_sensor(self, sensor):
        pass

    def handle_humidity_sensor(self, sensor):
        pass

    def handle_current_sensor(self, sensor):
        pass

    def handle_air_quality_sensor(self, sensor):
        pass

    def handle_heat_oven(self, actuator):
        pass

    def handle_light_bulp(self, actuator):
        pass

    def handle_outlet(self, actuator):
        pass

    def handle_car_charger(self, actuator):
        pass

    def handle_dehumidifier(self, actuator):
        pass

    def handle_floor_heating(self, actuator):
        pass

    def handle_heat_pump(self, actuator):
        pass


class Device:
    __slots__ = ['serial_no', 'producer', 'product_type', 'nickname']

    def __init__(self, serial_no: str, producer: str = None, product_type: str = None, nickname: str = None, device_id: int = None):
        self.serial_no = serial_no
        self.producer = producer
        self.product_type = product_type
        self.nickname = nickname
        self.device_id = device_id

    @abc.abstractmethod
    def get_status_message(self):
        pass

    @abc.abstractmethod
    def is_sensor(self):
        pass

    @abc.abstractmethod
    def is_actuator(self):
        pass

    def get_category(self):
        if self.is_sensor():
            return "Sensor"
        elif self.is_actuator():
            return "Aktuator"
        else:
            return None

    @abc.abstractmethod
    def get_type_name(self):
        pass

    @abc.abstractmethod
    def accept(self, visitor: DeviceVisitor):
        pass

    def __repr__(self):
        return f"{self.get_category()}({self.serial_no}) TYPE: {self.get_type_name()} STATUS: {self.get_status_message()} PRODUCT DETAILS: {self.producer} {self.product_type}"


class Sensor(Device):

    def __init__(self, serial_no: str, producer: str = None, product_type: str = None, nickname: str = None, device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)

    def get_status_message(self) -> str:
        return f"{round(self.get_current_value(), 2)} {self.get_unit()}"

    @abc.abstractmethod
    def get_current_value(self) -> Optional[float]:
        pass

    @abc.abstractmethod
    def get_unit(self) -> str:
        pass

    def is_sensor(self):
        return True

    def is_actuator(self):
        return False


class TemperatureSensor(Sensor):
    __slots__ = ['temperature']
    cursor = None
    conn = None

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 temperature: Optional[float] = None,
                 device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)
        self.temperature = temperature

    def get_current_value(self) -> Optional[float]:
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT value FROM device_state WHERE serial_no='{self.serial_no}'")

        self.temperature = cursor.fetchall()
        cursor.close()
        return self.temperature[0][2]

    def get_type_name(self):
        return "Temperatursensor"

    def get_unit(self):
        return "°C"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_temperature_sensor(self)


class HumiditySensor(Sensor):
    __slots__ = ['humidity']

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 humidity: Optional[float] = None,
                 device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)
        self.humidity = humidity

    def get_current_value(self) -> Optional[float]:
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT value FROM device_state WHERE serial_no='{self.serial_no}'")

        self.humidity = cursor.fetchall()
        cursor.close()
        return self.humidity[0][2]

    def get_type_name(self):
        return "Fuktighetssensor"

    def get_unit(self) -> str:
        return "%"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_humidity_sensor(self)


class SmartMeter(Sensor):
    __slots__ = ['energy_consumption']

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 energy_consumption: Optional[float] = None,
                 device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)
        self.energy_consumption = energy_consumption

    def get_current_value(self) -> Optional[float]:
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT value FROM device_state WHERE serial_no='{self.serial_no}'")

        self.energy_consumption = cursor.fetchall()
        cursor.close()
        return self.energy_consumption[0][2]

    def get_type_name(self):
        return "Strømmåler"

    def get_unit(self) -> str:
        return "kWh"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_current_sensor(self)


class AirQualitySensor(Sensor):
    __slots__ = ['air_quality']

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 air_quality: Optional[float] = None,
                 device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)
        self.air_quality = air_quality

    def get_current_value(self) -> float:
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT value FROM device_state WHERE serial_no='{self.serial_no}'")

        self.air_quality = cursor.fetchall()
        cursor.close()
        return self.air_quality[0][2]

    def get_type_name(self):
        return "Luftkvalitetssensor"

    def get_unit(self) -> str:
        return "g/m^2"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_air_quality_sensor(self)

class Actuator(Device):

    def __init__(self, serial_no: str, producer: str = None, product_type: str = None, nickname: str = None, device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)

    def is_actuator(self):
        return True

    def is_sensor(self):
        return False

    def get_category(self):
        return "Aktuator"


class SimpleOnOffActuator(Actuator):
    __slots__ = ['is_active']

    def __init__(self, serial_no: str, producer: str = None, product_type: str = None, nickname: str = None, device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)
        self.is_active = False

    def turn_on(self):
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE device_state SET value = 1 WHERE serial_no = '{self.serial_no}'")
        conn.commit()

        cursor.close()
        self.is_active = True

    def turn_off(self):
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE device_state SET value = 0 WHERE serial_no = '{self.serial_no}'")
        conn.commit()

        cursor.close()
        self.is_active = False

    def get_status_message(self):
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT value FROM device_state WHERE serial_no='{self.serial_no}'")

        self.is_active = cursor.fetchall()
        cursor.close()

        if self.is_active[0][0] == 1:
            return "ON"
        elif self.is_active[0][0] == 0:
            return "OFF"
        else:
            return "OFF"


class HeatControlActuator(Actuator):
    __slots__ = ['temperature']

    def __init__(self, serial_no: str, producer: str = None, product_type: str = None, nickname: str = None, device_id: int = None):
        super().__init__(serial_no, producer, product_type, nickname, device_id)
        self.temperature = None

    def get_status_message(self):
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT value FROM device_state WHERE serial_no = '{self.serial_no}'")

        self.temperature = cursor.fetchall()
        cursor.close()

        if self.temperature is not 0:
            return str(self.temperature[0][0]) + " °C"
        elif self.temperature == 0:
            return "OFF"
        else:
            return "OFF"

    def set_temperature(self, temperature: float):
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE device_state SET value = {str(temperature)} WHERE serial_no = '{self.serial_no}'")
        conn.commit()

        cursor.close()
        self.temperature = temperature

    def turn_off(self):
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"UPDATE device_state SET value = 0 WHERE serial_no = '{self.serial_no}'")
        conn.commit()

        cursor.close()
        self.temperature = 0


class HeatOven(HeatControlActuator):

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 device_id: int = None):
        super().__init__(serial_no, producer=producer, product_type=product_type, nickname=nickname, device_id=device_id)

    def get_type_name(self):
        return "Paneloven"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_heat_oven(self)


class LightBulb(SimpleOnOffActuator):

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 device_id: int = None):
        super().__init__(serial_no, producer=producer, product_type=product_type, nickname=nickname, device_id=device_id)

    def get_type_name(self):
        return "Smart Lys"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_light_bulp(self)


class SmartCharger(SimpleOnOffActuator):

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 device_id: int = None):
        super().__init__(serial_no, producer=producer, product_type=product_type, nickname=nickname, device_id=device_id)

    def get_type_name(self):
        return "Billader"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_car_charger(self)


class SmartOutlet(SimpleOnOffActuator):

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 device_id: int = None):
        super().__init__(serial_no, producer=producer, product_type=product_type, nickname=nickname, device_id=device_id)

    def get_type_name(self):
        return "Smart Stikkkontakt"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_outlet(self)


class HeatPump(HeatControlActuator):

    def __init__(self, serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 device_id: int = None):
        super().__init__(serial_no, producer=producer, product_type=product_type, nickname=nickname, device_id=device_id)

    def get_type_name(self):
        return "Varmepumpe"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_heat_pump(self)


class Dehumidifier(SimpleOnOffActuator):

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 device_id: int = None):
        super().__init__(serial_no, producer=producer, product_type=product_type, nickname=nickname, device_id=device_id)

    def get_type_name(self):
        return "Luftavfukter"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_dehumidifier(self)


class FloorHeatingPanel(HeatControlActuator):

    def __init__(self,
                 serial_no: str,
                 producer: str = None,
                 product_type: str = None,
                 nickname: str = None,
                 device_id: int = None):
        super().__init__(serial_no, producer=producer, product_type=product_type, nickname=nickname, device_id=device_id)

    def get_type_name(self):
        return "Gulvvarmepanel"

    def accept(self, visitor: DeviceVisitor):
        visitor.handle_floor_heating(self)