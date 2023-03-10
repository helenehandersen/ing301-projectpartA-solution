from sqlite3 import Connection
from devices import Device
from smarthouse import Room
from typing import Optional, List, Dict, Tuple
from datetime import date, datetime


class SmartHousePersistence:

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = Connection(db_file)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.rollback()
        self.connection.close()

    def save(self):
        self.connection.commit()

    def reconnect(self):
        self.connection.close()
        self.connection = Connection(self.db_file)
        self.cursor = self.connection.cursor()

    def check_tables(self) -> bool:
        self.cursor.execute("SELECT name FROM sqlite_schema WHERE type = 'table';")
        result = set()
        for row in self.cursor.fetchall():
            result.add(row[0])
        return 'rooms' in result and 'devices' in result and 'measurements' in result


class SmartHouseAnalytics:

    def __init__(self, persistence: SmartHousePersistence):
        self.persistence = persistence

    def get_most_recent_sensor_reading(self, sensor: Device) -> Optional[float]:
        """
        Retrieves the most recent (i.e. current) value reading for the given
        sensor device.
        Function may return None if the given device is an actuator or
        if there are no sensor values for the given device recorded in the database.
        """
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM measurements WHERE serial_no = '{sensor.serial_no}' ORDER BY time_stamp DESC LIMIT 1 ")
        measurement = cursor.fetchall()
        if not measurement: return None

        return measurement[0][2]


    def get_coldest_room(self) -> Room:
        """
        Finds the room, which has the lowest temperature on average.
        """
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT r.name FROM rooms r inner join devices d  ON r.id = d.room  Inner JOIN measurements m ON d.serial_no = m.serial_no GROUP by r.name order by avg(m.value)")
        measurement = cursor.fetchall()

        conn.close()

        return measurement[0][0]

    def get_sensor_readings_in_timespan(self, sensor: Device, from_ts: datetime, to_ts: datetime) -> List[float]:
        """
        Returns a list of sensor measurements (float values) for the given device in the given timespan.
        """
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT m.value FROM measurements m WHERE REPLACE(m.time_stamp, 'T', ' ') BETWEEN ? AND ? AND m.serial_no = ?", (from_ts, to_ts, sensor.serial_no))
        measurement = cursor.fetchall()

        svar = [x[0] for x in measurement]

        conn.close()

        return svar

    def describe_temperature_in_rooms(self) -> Dict[str, Tuple[float, float, float]]:
        """
        Returns a dictionary where the key are room names and the values are triples
        containing three floating point numbers:
        - The first component [index=0] being the _minimum_ temperature of the room.
        - The second component [index=1] being the _maximum_ temperature of the room.
        - The third component [index=2] being the _average_ temperature of the room.

        This function can be seen as a simplified version of the DataFrame.describe()
        function that exists in Pandas:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html?highlight=describe
        """
        conn = Connection('db.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT r.name, CAST(MIN(m.value) as float), CAST(MAX(m.value) as float), CAST(AVG(m.value) as float) as Verdier FROM rooms r Inner JOIN measurements m ON d.serial_no = m.serial_no inner join devices d  ON r.id = d.room GROUP by r.name")
        measurement = cursor.fetchall()

        navn = [x[0] for x in measurement]
        minverdi = [x[1] for x in measurement]
        maxverdi = [x[2] for x in measurement]
        gjennomsnitt = [x[3] for x in measurement]

        svar = {
            navn[3]: (minverdi[3], maxverdi[3], gjennomsnitt[3]),
            navn[2]: (minverdi[2], maxverdi[2], gjennomsnitt[2]),
            navn[4]: (minverdi[4], maxverdi[4], gjennomsnitt[4])
        }

        conn.close()

        return svar

    def get_hours_when_humidity_above_average(self, room: Room, day: date) -> List[int]:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number respresenting hours [0-23].
        """

        NotImplemented