from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from struct import unpack
from typing import Any, Callable, Optional

from .const import *
from .inverter import Sensor, SensorKind
from .protocol import ProtocolResponse

DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


class Voltage(Sensor):
    """Sensor representing voltage [V] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "V", kind)

    def read_value(self, data: ProtocolResponse):
        return read_voltage(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        return encode_voltage(value)


class Current(Sensor):
    """Sensor representing current [A] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "A", kind)

    def read_value(self, data: ProtocolResponse):
        return read_current(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        return encode_current(value)


class Frequency(Sensor):
    """Sensor representing frequency [Hz] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "Hz", kind)

    def read_value(self, data: ProtocolResponse):
        return read_freq(data)


class Power(Sensor):
    """Sensor representing power [W] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "W", kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes2(data)


class Power4(Sensor):
    """Sensor representing power [W] value encoded in 4 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 4, "W", kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes4(data)


class Energy(Sensor):
    """Sensor representing energy [kWh] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "kWh", kind)

    def read_value(self, data: ProtocolResponse):
        value = read_bytes2(data)
        if value == -1:
            return None
        else:
            return float(value) / 10


class Energy4(Sensor):
    """Sensor representing energy [kWh] value encoded in 4 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 4, "kWh", kind)

    def read_value(self, data: ProtocolResponse):
        value = read_bytes4(data)
        if value == -1:
            return None
        else:
            return float(value) / 10


class Apparent(Sensor):
    """Sensor representing apparent power [VA] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "VA", kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes2(data)


class Apparent4(Sensor):
    """Sensor representing apparent power [VA] value encoded in 4 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "VA", kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes4(data)


class Reactive(Sensor):
    """Sensor representing reactive power [var] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "var", kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes2(data)


class Reactive4(Sensor):
    """Sensor representing reactive power [var] value encoded in 4 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind]):
        super().__init__(id_, offset, name, 2, "var", kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes4(data)


class Temp(Sensor):
    """Sensor representing temperature [C] value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 2, "C", kind)

    def read_value(self, data: ProtocolResponse):
        return read_temp(data)


class Byte(Sensor):
    """Sensor representing signed int value encoded in 1 byte"""

    def __init__(self, id_: str, offset: int, name: str, unit: str = "", kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 1, unit, kind)

    def read_value(self, data: ProtocolResponse):
        return read_byte(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        raise NotImplementedError()


class ByteH(Byte):
    """Sensor representing signed int value encoded in 1 byte (high 8 bits of 16bit register)"""

    def __init__(self, id_: str, offset: int, name: str, unit: str = "", kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, unit, kind)

    def read_value(self, data: ProtocolResponse):
        return read_byte(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        word = bytearray(register_value)
        word[0] = int.to_bytes(int(value), length=1, byteorder="big", signed=True)[0]
        return bytes(word)


class ByteL(Byte):
    """Sensor representing signed int value encoded in 1 byte (low 8 bits of 16bit register)"""

    def __init__(self, id_: str, offset: int, name: str, unit: str = "", kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, unit, kind)

    def read_value(self, data: ProtocolResponse):
        read_byte(data)
        return read_byte(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        word = bytearray(register_value)
        word[1] = int.to_bytes(int(value), length=1, byteorder="big", signed=True)[0]
        return bytes(word)


class Integer(Sensor):
    """Sensor representing signed int value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, name: str, unit: str = "", kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 2, unit, kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes2(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        return int.to_bytes(int(value), length=2, byteorder="big", signed=True)


class Long(Sensor):
    """Sensor representing signed int value encoded in 4 bytes"""

    def __init__(self, id_: str, offset: int, name: str, unit: str = "", kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 4, unit, kind)

    def read_value(self, data: ProtocolResponse):
        return read_bytes4(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        return int.to_bytes(int(value), length=4, byteorder="big", signed=True)


class Decimal(Sensor):
    """Sensor representing signed decimal value encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, scale: int, name: str, unit: str = "", kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 2, unit, kind)
        self.scale = scale

    def read_value(self, data: ProtocolResponse):
        return read_decimal2(data, self.scale)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        return int.to_bytes(int(value * self.scale), length=2, byteorder="big", signed=True)


class Float(Sensor):
    """Sensor representing signed int value encoded in 4 bytes"""

    def __init__(self, id_: str, offset: int, scale: int, name: str, unit: str = "", kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 4, unit, kind)
        self.scale = scale

    def read_value(self, data: ProtocolResponse):
        return round(read_float4(data) / self.scale, 3)


class Timestamp(Sensor):
    """Sensor representing datetime value encoded in 6 bytes"""

    def __init__(self, id_: str, offset: int, name: str, kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 6, "", kind)

    def read_value(self, data: ProtocolResponse):
        return read_datetime(data)

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        return encode_datetime(value)


class Enum(Sensor):
    """Sensor representing label from enumeration encoded in 1 bytes"""

    def __init__(self, id_: str, offset: int, labels: Dict, name: str, kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 1, "", kind)
        self._labels: Dict = labels

    def read_value(self, data: ProtocolResponse):
        return self._labels.get(read_byte(data))


class EnumH(Sensor):
    """Sensor representing label from enumeration encoded in 1 (high 8 bits of 16bit register)"""

    def __init__(self, id_: str, offset: int, labels: Dict, name: str, kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 1, "", kind)
        self._labels: Dict = labels

    def read_value(self, data: ProtocolResponse):
        return self._labels.get(read_byte(data))


class EnumL(Sensor):
    """Sensor representing label from enumeration encoded in 1 bytes (low 8 bits of 16bit register)"""

    def __init__(self, id_: str, offset: int, labels: Dict, name: str, kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 1, "", kind)
        self._labels: Dict = labels

    def read_value(self, data: ProtocolResponse):
        read_byte(data)
        return self._labels.get(read_byte(data))


class Enum2(Sensor):
    """Sensor representing label from enumeration encoded in 2 bytes"""

    def __init__(self, id_: str, offset: int, labels: Dict, name: str, kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 2, "", kind)
        self._labels: Dict = labels

    def read_value(self, data: ProtocolResponse):
        return self._labels.get(read_bytes2(data))


class EnumBitmap4(Sensor):
    """Sensor representing label from bitmap encoded in 4 bytes"""

    def __init__(self, id_: str, offset: int, labels: Dict, name: str, kind: Optional[SensorKind] = None):
        super().__init__(id_, offset, name, 4, "", kind)
        self._labels: Dict = labels

    def read_value(self, data: ProtocolResponse) -> Any:
        raise NotImplementedError()

    def read(self, data: ProtocolResponse):
        return decode_bitmap(read_bytes4(data, self.offset), self._labels)


class EnumBitmap22(Sensor):
    """Sensor representing label from bitmap encoded in 2+2 bytes"""

    def __init__(self, id_: str, offsetH: int, offsetL: int, labels: Dict, name: str,
                 kind: Optional[SensorKind] = None):
        super().__init__(id_, offsetH, name, 2, "", kind)
        self._labels: Dict = labels
        self._offsetL: int = offsetL

    def read_value(self, data: ProtocolResponse) -> Any:
        raise NotImplementedError()

    def read(self, data: ProtocolResponse):
        return decode_bitmap(read_bytes2(data, self.offset) << 16 + read_bytes2(data, self._offsetL), self._labels)


class EnumCalculated(Sensor):
    """Sensor representing label from enumeration of calculated value"""

    def __init__(self, id_: str, getter: Callable[[ProtocolResponse], Any], labels: Dict, name: str,
                 kind: Optional[SensorKind] = None):
        super().__init__(id_, 0, name, 0, "", kind)
        self._getter: Callable[[ProtocolResponse], Any] = getter
        self._labels: Dict = labels

    def read_value(self, data: ProtocolResponse) -> Any:
        raise NotImplementedError()

    def read(self, data: ProtocolResponse):
        return self._labels.get(self._getter(data))


class EcoMode(ABC):
    """Sensor representing Eco Mode Battery Power Group API"""

    @abstractmethod
    def encode_charge(self, eco_mode_power: int, eco_mode_soc: int = 100) -> bytes:
        """Answer bytes representing all the time enabled charging eco mode group"""

    @abstractmethod
    def encode_discharge(self, eco_mode_power: int) -> bytes:
        """Answer bytes representing all the time enabled discharging eco mode group"""

    @abstractmethod
    def encode_off(self) -> bytes:
        """Answer bytes representing empty and disabled eco mode group"""

    @abstractmethod
    def is_eco_charge_mode(self) -> bool:
        """Answer if it represents the emulated 24/7 fulltime discharge mode"""

    @abstractmethod
    def is_eco_discharge_mode(self) -> bool:
        """Answer if it represents the emulated 24/7 fulltime discharge mode"""


class EcoModeV1(Sensor, EcoMode):
    """Sensor representing Eco Mode Battery Power Group encoded in 8 bytes"""

    def __init__(self, id_: str, offset: int, name: str):
        super().__init__(id_, offset, name, 8, "", SensorKind.BAT)
        self.start_h: int | None = None
        self.start_m: int | None = None
        self.end_h: int | None = None
        self.end_m: int | None = None
        self.power: int | None = None
        self.on_off: int | None = None
        self.day_bits: int | None = None
        self.days: str | None = None
        self.soc: int = 100  # just to keep same API with V2

    def __str__(self):
        return f"{self.start_h}:{self.start_m}-{self.end_h}:{self.end_m} {self.days} " \
               f"{self.power}% " \
               f"{'On' if self.on_off != 0 else 'Off'}"

    def read_value(self, data: ProtocolResponse):
        self.start_h = read_byte(data)
        if (self.start_h < 0 or self.start_h > 23) and self.start_h != 48:
            raise ValueError(f"{self.id_}: start_h value {self.start_h} out of range.")
        self.start_m = read_byte(data)
        if self.start_m < 0 or self.start_m > 59:
            raise ValueError(f"{self.id_}: start_m value {self.start_m} out of range.")
        self.end_h = read_byte(data)
        if (self.end_h < 0 or self.end_h > 23) and self.end_h != 48:
            raise ValueError(f"{self.id_}: end_h value {self.end_h} out of range.")
        self.end_m = read_byte(data)
        if self.end_m < 0 or self.end_m > 59:
            raise ValueError(f"{self.id_}: end_m value {self.end_m} out of range.")
        self.power = read_bytes2(data)  # negative=charge, positive=discharge
        if self.power < -100 or self.power > 100:
            raise ValueError(f"{self.id_}: power value {self.power} out of range.")
        self.on_off = read_byte(data)
        if self.on_off not in (0, -1):
            raise ValueError(f"{self.id_}: on_off value {self.on_off} out of range.")
        self.day_bits = read_byte(data)
        self.days = decode_day_of_week(self.day_bits)
        if self.day_bits < 0:
            raise ValueError(f"{self.id_}: day_bits value {self.day_bits} out of range.")
        return self

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        if isinstance(value, bytes) and len(value) == 8:
            # try to read_value to check if values are valid
            if self.read_value(ProtocolResponse(value, None)):
                return value
        raise ValueError

    def encode_charge(self, eco_mode_power: int, eco_mode_soc: int = 100) -> bytes:
        """Answer bytes representing all the time enabled charging eco mode group"""
        return bytes.fromhex("0000173b{:04x}ff7f".format((-1 * abs(eco_mode_power)) & (2 ** 16 - 1)))

    def encode_discharge(self, eco_mode_power: int) -> bytes:
        """Answer bytes representing all the time enabled discharging eco mode group"""
        return bytes.fromhex("0000173b{:04x}ff7f".format(abs(eco_mode_power)))

    def encode_off(self) -> bytes:
        """Answer bytes representing empty and disabled eco mode group"""
        return bytes.fromhex("3000300000640000")

    def is_eco_charge_mode(self) -> bool:
        """Answer if it represents the emulated 24/7 fulltime discharge mode"""
        return self.start_h == 0 \
               and self.start_m == 0 \
               and self.end_h == 23 \
               and self.end_m == 59 \
               and self.on_off != 0 \
               and self.day_bits == 127 \
               and self.power < 0

    def is_eco_discharge_mode(self) -> bool:
        """Answer if it represents the emulated 24/7 fulltime discharge mode"""
        return self.start_h == 0 \
               and self.start_m == 0 \
               and self.end_h == 23 \
               and self.end_m == 59 \
               and self.on_off != 0 \
               and self.day_bits == 127 \
               and self.power > 0

    def as_eco_mode_v2(self) -> EcoModeV2:
        """Convert V1 to V2 EcoMode"""
        result = EcoModeV2(self.id_, self.offset, self.name)
        result.start_h = self.start_h
        result.start_m = self.start_m
        result.end_h = self.end_h
        result.end_m = self.end_m
        result.power = self.power
        result.on_off = self.on_off
        result.day_bits = self.day_bits
        result.days = decode_day_of_week(self.day_bits)
        result.soc = 100
        return result


class EcoModeV2(Sensor, EcoMode):
    """Sensor representing Eco Mode Battery Power Group encoded in 12 bytes"""

    def __init__(self, id_: str, offset: int, name: str):
        super().__init__(id_, offset, name, 12, "", SensorKind.BAT)
        self.start_h: int | None = None
        self.start_m: int | None = None
        self.end_h: int | None = None
        self.end_m: int | None = None
        self.on_off: int | None = None
        self.day_bits: int | None = None
        self.days: str | None = None
        self.power: int | None = None
        self.soc: int | None = None
        # 2 bytes padding 0000

    def __str__(self):
        return f"{self.start_h}:{self.start_m}-{self.end_h}:{self.end_m} {self.days} " \
               f"{self.power}% (SoC {self.soc}%) " \
               f"{'On' if self.on_off == -1 else 'Off' if self.on_off == 0 else 'Unset'}"

    def read_value(self, data: ProtocolResponse):
        self.start_h = read_byte(data)
        if (self.start_h < 0 or self.start_h > 23) and self.start_h != 48:
            raise ValueError(f"{self.id_}: start_h value {self.start_h} out of range.")
        self.start_m = read_byte(data)
        if self.start_m < 0 or self.start_m > 59:
            raise ValueError(f"{self.id_}: start_m value {self.start_m} out of range.")
        self.end_h = read_byte(data)
        if (self.end_h < 0 or self.end_h > 23) and self.end_h != 48:
            raise ValueError(f"{self.id_}: end_h value {self.end_h} out of range.")
        self.end_m = read_byte(data)
        if self.end_m < 0 or self.end_m > 59:
            raise ValueError(f"{self.id_}: end_m value {self.end_m} out of range.")
        self.on_off = read_byte(data)
        if self.on_off not in (0, -1, 85):
            raise ValueError(f"{self.id_}: on_off value {self.on_off} out of range.")
        self.day_bits = read_byte(data)
        self.days = decode_day_of_week(self.day_bits)
        if self.day_bits < 0:
            raise ValueError(f"{self.id_}: day_bits value {self.day_bits} out of range.")
        self.power = read_bytes2(data)  # negative=charge, positive=discharge
        if self.power < -100 or self.power > 100:
            raise ValueError(f"{self.id_}: power value {self.power} out of range.")
        self.soc = read_bytes2(data)
        if self.soc < 0 or self.soc > 100:
            raise ValueError(f"{self.id_}: SoC value {self.soc} out of range.")
        return self

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        if isinstance(value, bytes) and len(value) == 12:
            # try to read_value to check if values are valid
            if self.read_value(ProtocolResponse(value, None)):
                return value
        raise ValueError

    def encode_charge(self, eco_mode_power: int, eco_mode_soc: int = 100) -> bytes:
        """Answer bytes representing all the time enabled charging eco mode group"""
        return bytes.fromhex(
            "0000173bff7f{:04x}{:04x}0000".format((-1 * abs(eco_mode_power)) & (2 ** 16 - 1), eco_mode_soc))

    def encode_discharge(self, eco_mode_power: int) -> bytes:
        """Answer bytes representing all the time enabled discharging eco mode group"""
        return bytes.fromhex("0000173bff7f{:04x}00640000".format(abs(eco_mode_power)))

    def encode_off(self) -> bytes:
        """Answer bytes representing empty and disabled eco mode group"""
        return bytes.fromhex("300030000000006400640000")

    def is_eco_charge_mode(self) -> bool:
        """Answer if it represents the emulated 24/7 fulltime discharge mode"""
        return self.start_h == 0 \
               and self.start_m == 0 \
               and self.end_h == 23 \
               and self.end_m == 59 \
               and self.on_off == -1 \
               and self.day_bits == 127 \
               and self.power < 0

    def is_eco_discharge_mode(self) -> bool:
        """Answer if it represents the emulated 24/7 fulltime discharge mode"""
        return self.start_h == 0 \
               and self.start_m == 0 \
               and self.end_h == 23 \
               and self.end_m == 59 \
               and self.on_off == -1 \
               and self.day_bits == 127 \
               and self.power > 0

    def as_eco_mode_v1(self) -> EcoModeV1:
        """Convert V2 to V1 EcoMode"""
        result = EcoModeV1(self.id_, self.offset, self.name)
        result.start_h = self.start_h
        result.start_m = self.start_m
        result.end_h = self.end_h
        result.end_m = self.end_m
        result.power = self.power
        result.on_off = -1 if self.on_off == -1 else 0
        result.day_bits = self.day_bits
        result.days = self.days
        return result


class PeakShavingMode(Sensor):
    """Sensor representing Peak Shaving Mode encoded in 12 bytes"""

    def __init__(self, id_: str, offset: int, name: str):
        super().__init__(id_, offset, name, 12, "", SensorKind.BAT)
        self.start_h: int | None = None
        self.start_m: int | None = None
        self.end_h: int | None = None
        self.end_m: int | None = None
        self.on_off: int | None = None
        self.day_bits: int | None = None
        self.days: str | None = None
        self.import_power: float | None = None
        self.soc: int | None = None
        # 2 bytes padding 0000

    def __str__(self):
        return f"{self.start_h}:{self.start_m}-{self.end_h}:{self.end_m} {self.days} " \
               f"{self.import_power}kW (SoC {self.soc}%) " \
               f"{'On' if self.on_off == -4 else 'Off' if self.on_off == 3 else 'Unset'}"

    def read_value(self, data: ProtocolResponse):
        self.start_h = read_byte(data)
        if (self.start_h < 0 or self.start_h > 23) and self.start_h != 48:
            raise ValueError(f"{self.id_}: start_h value {self.start_h} out of range.")
        self.start_m = read_byte(data)
        if self.start_m < 0 or self.start_m > 59:
            raise ValueError(f"{self.id_}: start_m value {self.start_m} out of range.")
        self.end_h = read_byte(data)
        if (self.end_h < 0 or self.end_h > 23) and self.end_h != 48:
            raise ValueError(f"{self.id_}: end_h value {self.end_h} out of range.")
        self.end_m = read_byte(data)
        if self.end_m < 0 or self.end_m > 59:
            raise ValueError(f"{self.id_}: end_m value {self.end_m} out of range.")
        self.on_off = read_byte(data)
        if self.on_off not in (-4, 3, 85):
            raise ValueError(f"{self.id_}: on_off value {self.on_off} out of range.")
        self.day_bits = read_byte(data)
        self.days = decode_day_of_week(self.day_bits)
        if self.day_bits < 0:
            raise ValueError(f"{self.id_}: day_bits value {self.day_bits} out of range.")
        self.import_power = read_decimal2(data, 100)
        if self.import_power < 0 or self.import_power > 500:
            raise ValueError(f"{self.id_}: import_power value {self.import_power} out of range.")
        self.soc = read_bytes2(data)
        if self.soc < 0 or self.soc > 100:
            raise ValueError(f"{self.id_}: soc value {self.soc} out of range.")
        return self

    def encode_value(self, value: Any, register_value: bytes = None) -> bytes:
        if isinstance(value, bytes) and len(value) == 12:
            # try to read_value to check if values are valid
            if self.read_value(ProtocolResponse(value, None)):
                return value
        raise ValueError

    def encode_off(self) -> bytes:
        """Answer bytes representing empty and disabled eco mode group"""
        return bytes.fromhex("300030000000006400640000")


class Calculated(Sensor):
    """Sensor representing calculated value"""

    def __init__(self, id_: str, getter: Callable[[ProtocolResponse], Any], name: str, unit: str,
                 kind: Optional[SensorKind] = None):
        super().__init__(id_, 0, name, 0, unit, kind)
        self._getter: Callable[[ProtocolResponse], Any] = getter

    def read_value(self, data: ProtocolResponse) -> Any:
        raise NotImplementedError()

    def read(self, data: ProtocolResponse):
        return self._getter(data)


def read_byte(buffer: ProtocolResponse, offset: int = None) -> int:
    """Retrieve single byte (signed int) value from buffer"""
    if offset is not None:
        buffer.seek(offset)
    return int.from_bytes(buffer.read(1), byteorder="big", signed=True)


def read_bytes2(buffer: ProtocolResponse, offset: int = None) -> int:
    """Retrieve 2 byte (signed int) value from buffer"""
    if offset is not None:
        buffer.seek(offset)
    return int.from_bytes(buffer.read(2), byteorder="big", signed=True)


def read_bytes4(buffer: ProtocolResponse, offset: int = None) -> int:
    """Retrieve 4 byte (signed int) value from buffer"""
    if offset is not None:
        buffer.seek(offset)
    return int.from_bytes(buffer.read(4), byteorder="big", signed=True)


def read_decimal2(buffer: ProtocolResponse, scale: int, offset: int = None) -> float:
    """Retrieve 2 byte (signed float) value from buffer"""
    if offset is not None:
        buffer.seek(offset)
    return float(int.from_bytes(buffer.read(2), byteorder="big", signed=True)) / scale


def read_float4(buffer: ProtocolResponse, offset: int = None) -> float:
    """Retrieve 4 byte (signed float) value from buffer"""
    if offset is not None:
        buffer.seek(offset)
    data = buffer.read(4)
    if len(data) == 4:
        return unpack('>f', data)[0]
    else:
        return float(0)


def read_voltage(buffer: ProtocolResponse, offset: int = None) -> float:
    """Retrieve voltage [V] value (2 bytes) from buffer"""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=True)
    return float(value) / 10


def encode_voltage(value: Any) -> bytes:
    """Encode voltage value to raw (2 bytes) payload"""
    return int.to_bytes(int(value * 10), length=2, byteorder="big", signed=True)


def read_current(buffer: ProtocolResponse, offset: int = None) -> float:
    """Retrieve current [A] value (2 bytes) from buffer"""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=True)
    return float(value) / 10


def encode_current(value: Any) -> bytes:
    """Encode current value to raw (2 bytes) payload"""
    return int.to_bytes(int(value * 10), length=2, byteorder="big", signed=True)


def read_freq(buffer: ProtocolResponse, offset: int = None) -> float:
    """Retrieve frequency [Hz] value (2 bytes) from buffer"""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=True)
    return float(value) / 100


def read_temp(buffer: ProtocolResponse, offset: int = None) -> float:
    """Retrieve temperature [C] value (2 bytes) from buffer"""
    if offset is not None:
        buffer.seek(offset)
    value = int.from_bytes(buffer.read(2), byteorder="big", signed=True)
    return float(value) / 10


def read_datetime(buffer: ProtocolResponse, offset: int = None) -> datetime:
    """Retrieve datetime value (6 bytes) from buffer"""
    if offset is not None:
        buffer.seek(offset)
    year = 2000 + int.from_bytes(buffer.read(1), byteorder='big')
    month = int.from_bytes(buffer.read(1), byteorder='big')
    day = int.from_bytes(buffer.read(1), byteorder='big')
    hour = int.from_bytes(buffer.read(1), byteorder='big')
    minute = int.from_bytes(buffer.read(1), byteorder='big')
    second = int.from_bytes(buffer.read(1), byteorder='big')
    return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)


def encode_datetime(value: Any) -> bytes:
    """Encode datetime value to raw (6 bytes) payload"""
    timestamp = value
    if isinstance(value, str):
        timestamp = datetime.fromisoformat(value)

    result = bytes([
        timestamp.year - 2000,
        timestamp.month,
        timestamp.day,
        timestamp.hour,
        timestamp.minute,
        timestamp.second,
    ])
    return result


def read_grid_mode(buffer: ProtocolResponse, offset: int = None) -> int:
    """Retrieve 'grid mode' sign value from buffer"""
    value = read_bytes2(buffer, offset)
    if value < -90:
        return 2
    elif value >= 90:
        return 1
    else:
        return 0


def read_unsigned_int(data: bytes, offset: int) -> int:
    """Retrieve 2 byte (unsigned int) value from bytes at specified offset"""
    return int.from_bytes(data[offset:offset + 2], byteorder="big", signed=False)


def decode_bitmap(value: int, bitmap: Dict[int, str]) -> str:
    bits = value
    result = []
    for i in range(32):
        if bits & 0x1 == 1:
            result.append(bitmap.get(i, f'err{i}'))
        bits = bits >> 1
    return ", ".join(result)


def decode_day_of_week(data: int) -> str:
    bits = bin(data)[2:]
    daynames = list(DAY_NAMES)
    days = ""
    for each in bits[::-1]:
        if each == '1':
            if len(days) > 0:
                days += ","
            days += daynames[0]
        daynames.pop(0)
    return days
