# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
import binascii
from enum import Enum

def hex_string(data):
    return str(binascii.hexlify(data).upper())[2:-1]


class CTGPGhosts(KaitaiStruct):

    class Controllers(Enum):
        wii_wheel = 0
        wii_remote = 1
        classic_controller = 2
        gamecube_controller = 3

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = (self._io.read_bytes(4)).decode(u"utf-8")
        self.finishing_time_minutes = self._io.read_bits_int_be(7)
        self.finishing_time_seconds = self._io.read_bits_int_be(7)
        self.finishing_time_milliseconds = self._io.read_bits_int_be(10)
        self.track_id = self._io.read_bits_int_be(6)
        self.unknown_1 = self._io.read_bits_int_be(2)
        self.vehicle_id = self._io.read_bits_int_be(6)
        self.character_id = self._io.read_bits_int_be(6)
        self.ghost_sent_year = self._io.read_bits_int_be(7)
        self.ghost_sent_month = self._io.read_bits_int_be(4)
        self.ghost_sent_day = self._io.read_bits_int_be(5)
        self.controller_id = KaitaiStream.resolve_enum(MkwGhosts.Controllers, self._io.read_bits_int_be(4))
        self.unknown_2 = self._io.read_bits_int_be(4)
        self.compressed_flag = self._io.read_bits_int_be(1) != 0
        self.unknown_3 = self._io.read_bits_int_be(2)
        self.ghost_type = self._io.read_bits_int_be(7)
        self.drift_type = self._io.read_bits_int_be(1) != 0
        self.unknown_4 = self._io.read_bits_int_be(1) != 0
        self._io.align_to_byte()
        self.input_data_length = self._io.read_u2be()
        self.lap_count = self._io.read_u1()
        self.lap_split_time = [None] * (5)
        for i in range(5):
            self.lap_split_time[i] = CTGPGhosts.LapSplit(self._io, self, self._root)



        self.unknown_5 = self._io.read_bytes(20)
        self.country_code = self._io.read_u1()
        self.region_code = self._io.read_u1()
        self.location_code = self._io.read_u2be()
        self.unknown_6 = self._io.read_u4be()
        self.driver_mii_data = self._io.read_bytes(74)
        self.crc16_mii = self._io.read_bytes(2)
        self.data = self._io.read_bytes(((self._io.size() - self._io.pos()) - 216))
        self.security_data = self._io.read_bytes(76)
        self.track_sha1 = hex_string(self._io.read_bytes(20))
        self.ctgp_pid = hex_string(self._io.read_bytes(8))
        self.truetime_float = self._io.read_u4be()
        self.ctgp_ver_1 = int.from_bytes(self._io.read_bytes(1), 'big')
        self.ctgp_ver_2 = int.from_bytes(self._io.read_bytes(1), 'big')
        self.ctgp_ver_3 = self._io.read_bytes(2)
        self.garbagelol = self._io.read_bytes(32)
        self.truelaptime_floats = self._io.read_bytes(28)
        self.rtc_race_end = self._io.read_bytes(8)
        self.rtc_race_begin = self._io.read_bytes(8)
        self.rtc_time_paused = self._io.read_bytes(8)
        self.padding = self._io.read_bits_int_be(4)
        self.my_stuff_enabled = bool(self._io.read_bits_int_be(1))
        self.my_stuff_used = bool(self._io.read_bits_int_be(1))
        self.usb_gcn = bool(self._io.read_bits_int_be(1))
        self.final_lap_dubious = bool(self._io.read_bits_int_be(1))
        self.shroom3 = self._io.read_bits_int_be(8)
        self.shroom2 = self._io.read_bits_int_be(8)
        self.shroom1 = self._io.read_bits_int_be(8)
        self.sc_def_ver = self._io.read_bytes(1)
        self.cannoned = bool(self._io.read_bits_int_be(1))
        self.oob = bool(self._io.read_bits_int_be(1))
        self.slowdown = bool(self._io.read_bits_int_be(1))
        self.rapid_fire = bool(self._io.read_bits_int_be(1))
        self.dubious_intersection = bool(self._io.read_bits_int_be(1))
        self.mii_data_replaced = bool(self._io.read_bits_int_be(1))
        self.has_name_replaced = bool(self._io.read_bits_int_be(1))
        self.respawns = bool(self._io.read_bits_int_be(1))
        self.category = int.from_bytes(self._io.read_bytes(1), 'big')
        self.footer_version = int.from_bytes(self._io.read_bytes(1), 'big')
        self.ctgp_length = int.from_bytes(self._io.read_bytes(4), 'big')
        self.ctgp_magic = self._io.read_bytes(4).decode('utf-8')
        self.crc32 = int.from_bytes(self._io.read_bytes(4), 'big')

    class LapSplit(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.finishing_time_minutes = self._io.read_bits_int_be(7)
            self.finishing_time_seconds = self._io.read_bits_int_be(7)
            self.finishing_time_milliseconds = self._io.read_bits_int_be(10)


class MkwGhosts(KaitaiStruct):

    class Controllers(Enum):
        wii_wheel = 0
        wii_remote = 1
        classic_controller = 2
        gamecube_controller = 3

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = (self._io.read_bytes(4)).decode(u"utf-8")
        self.finishing_time_minutes = self._io.read_bits_int_be(7)
        self.finishing_time_seconds = self._io.read_bits_int_be(7)
        self.finishing_time_milliseconds = self._io.read_bits_int_be(10)
        self.track_id = self._io.read_bits_int_be(6)
        self.unknown_1 = self._io.read_bits_int_be(2)
        self.vehicle_id = self._io.read_bits_int_be(6)
        self.character_id = self._io.read_bits_int_be(6)
        self.ghost_sent_year = self._io.read_bits_int_be(7)
        self.ghost_sent_month = self._io.read_bits_int_be(4)
        self.ghost_sent_day = self._io.read_bits_int_be(5)
        self.controller_id = KaitaiStream.resolve_enum(MkwGhosts.Controllers, self._io.read_bits_int_be(4))
        self.unknown_2 = self._io.read_bits_int_be(4)
        self.compressed_flag = self._io.read_bits_int_be(1) != 0
        self.unknown_3 = self._io.read_bits_int_be(2)
        self.ghost_type = self._io.read_bits_int_be(7)
        self.drift_type = self._io.read_bits_int_be(1) != 0
        self.unknown_4 = self._io.read_bits_int_be(1) != 0
        self._io.align_to_byte()
        self.input_data_length = self._io.read_u2be()
        self.lap_count = self._io.read_u1()
        self.lap_split_time = [None] * (5)
        for i in range(5):
            self.lap_split_time[i] = MkwGhosts.LapSplit(self._io, self, self._root)

        self.unknown_5 = self._io.read_bytes(20)
        self.country_code = self._io.read_u1()
        self.region_code = self._io.read_u1()
        self.location_code = self._io.read_u2be()
        self.unknown_6 = self._io.read_u4be()
        self.driver_mii_data = self._io.read_bytes(74)
        self.crc16_mii = self._io.read_bytes(2)
        self.data = self._io.read_bytes((self._io.size() - self._io.pos()) - 4)
        self.position = self._io.pos()
        self.crc32 = int.from_bytes(self._io.read_bytes(4), 'big')

    class LapSplit(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.finishing_time_minutes = self._io.read_bits_int_be(7)
            self.finishing_time_seconds = self._io.read_bits_int_be(7)
            self.finishing_time_milliseconds = self._io.read_bits_int_be(10)



