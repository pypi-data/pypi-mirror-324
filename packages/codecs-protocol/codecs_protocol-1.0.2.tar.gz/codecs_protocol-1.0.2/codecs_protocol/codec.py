import codecs
import asyncio
from .helper import handle_decoded_packet
import time
import struct


mapp = {'id': 0, 'value':0}
class Codec8:
    def __init__(self, data_packet) -> None:
        self.data_packet = data_packet
        
    async def get_timestamp(self, timestamp_data):
        return time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(int(str(int(timestamp_data, 16))[:-3])))
    
    async def decode_io_data(self, iodata, offset):
        io_data = {
            "event_id"          : 0,
            "total_io_elements" : 0,
            "one_byte_io"       : [],
            "two_byte_io"       : [],
            "four_byte_io"      : [],
            "eight_byte_io"     : []
        }
        
        io_data["event_id"] = int(iodata[offset : offset + 2], 16)
        offset += 2 
        
        io_data["total_io_elements"] = int(iodata[offset : offset + 2], 16)
        offset += 2
        
        one_byte_count = int(iodata[offset : offset+2], 16)
        offset += 2
        for _ in range(one_byte_count):
            io_data['one_byte_io'].append({
                "id"    : int(iodata[offset : offset + 2], 16),
                "value" : int(iodata[offset + 2 : offset + 4], 16)
            })
            offset += 4
            
        two_byte_count = int(iodata[offset : offset+2], 16)
        offset += 2
        for _ in range(two_byte_count):
            io_data['two_byte_io'].append({
                "id"    : int(iodata[offset : offset + 2], 16),
                "value" : int(iodata[offset + 2 : offset + 6], 16)
            })
            offset += 6
            
        four_byte_count = int(iodata[offset : offset+2], 16)
        offset += 2
        for _ in range(four_byte_count):
            io_data['four_byte_io'].append({
                "id"    : int(iodata[offset : offset + 2], 16),
                "value" : int(iodata[offset + 2 : offset + 10], 16)
            })
            offset += 10
            
        eight_byte_count = int(iodata[offset : offset+2], 16) if iodata[offset : offset+2] else 0
        offset += 2
        for _ in range(eight_byte_count):
            io_data['eight_byte_io'].append({
                "id"    : int(iodata[offset : offset + 2], 16),
                "value" : int(iodata[offset + 2 : offset + 18], 16)
            })
            offset += 18
        
        
        return io_data, offset
        
    
    async def decode_avl_packet(self, records, avl_data, number_of_records):
        offset  = 0
        for _ in range(number_of_records):
            timestamp = await self.get_timestamp(avl_data[offset:offset + 16])
            offset += 16
            
            priority = int(avl_data[offset : offset + 2], 16)
            offset += 2
            
            longitude = int(avl_data[offset : offset + 8], 16) / 10000000.0
            offset += 8
            
            latitude = int(avl_data[offset : offset + 8], 16) / 10000000.0 
            offset += 8
            
            altitude = int(avl_data[offset : offset + 4], 16)
            offset += 4
            
            angle = int(avl_data[offset : offset + 4], 16)
            offset += 4
            
            satellites = int(avl_data[offset : offset + 2], 16)
            offset += 2
            
            speed = int(avl_data[offset : offset + 4], 16)
            offset += 4
            
            io_data, offset = await self.decode_io_data(avl_data, offset)
            
            records["records"].append({
                "timestamp"     : timestamp,
                "priority"      : priority,
                "longitude"     : longitude,
                "latitude"      : latitude,
                "altitude"      : altitude,
                "angle"         : angle,
                "satellites"    : satellites,
                "speed"         : speed,
                "io_data"       : io_data
            })
            
        return records
        
    async def decode_data(self):
        # Removing zero bytes and data size
        response = {"records" : []}
        self.data_packet = self.data_packet[16:]
        
        codec_id = self.data_packet[:2]
        if not int(codec_id, 16) == 8:
            return response, '00'
        
        number_of_records = int(self.data_packet[2:4], 16)
        
        response = await self.decode_avl_packet(response, self.data_packet[4:-10], number_of_records)
        
        return response, struct.pack(">I", number_of_records).hex()
    
class Codec8E:
    def __init__(self, data_packet) -> None:
        self.data_packet = data_packet
        
    async def get_timestamp(self, timestamp_data):
        return time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(int(str(int(timestamp_data, 16))[:-3])))
    
    async def decode_io_data(self, iodata, offset):
        button_action = False
        io_data = {
            "event_id"          : 0,
            "total_io_elements" : 0,
            "one_byte_io"       : [],
            "two_byte_io"       : [],
            "four_byte_io"      : [],
            "eight_byte_io"     : []
        }
        io_data["event_id"] = int(iodata[offset : offset + 4], 16)
        offset += 4
        
        io_data["total_io_elements"] = int(iodata[offset : offset + 4], 16)
        offset += 4
        
        one_byte_count = int(iodata[offset : offset + 4], 16)
        offset += 4
        for _ in range(one_byte_count):
            io_data['one_byte_io'].append({
                "id"    : int(iodata[offset : offset + 4], 16),
                "value" : int(iodata[offset + 4 : offset + 6], 16) if int(iodata[offset : offset + 4], 16) != 389 else int(iodata[offset + 4 : offset + 6])
            })
            button_action =  True if int(iodata[offset : offset + 4], 16) == 389 and button_action != True else False
            offset += 6
            
        two_byte_count = int(iodata[offset : offset+4], 16)
        offset += 4
        for _ in range(two_byte_count):
            io_data['two_byte_io'].append({
                "id"    : int(iodata[offset : offset + 4], 16),
                "value" : int(iodata[offset + 4 : offset + 8], 16) 
            })
            offset += 8

        four_byte_count = int(iodata[offset : offset+4], 16)
        offset += 4
        for _ in range(four_byte_count):
            io_data['four_byte_io'].append({
                "id"    : int(iodata[offset : offset + 4], 16),
                "value" : int(iodata[offset + 4 : offset + 12], 16)
            })
            offset += 12
            
        eight_byte_count = int(iodata[offset : offset+4], 16) if iodata[offset : offset+4] else 0
        offset += 4
        for _ in range(eight_byte_count):
            io_data['eight_byte_io'].append({
                "id"    : int(iodata[offset : offset + 4], 16),
                "value" : int(iodata[offset + 4 : offset + 20], 16)
            })
            offset += 20
        
        offset += 4
        
        return io_data, offset, button_action
        
    
    async def decode_avl_packet(self, records, avl_data, number_of_records):
        offset  = 0
        for _ in range(number_of_records):
            timestamp = await self.get_timestamp(avl_data[offset:offset + 16])
            offset += 16
            
            priority = int(avl_data[offset : offset + 2], 16)
            offset += 2
            
            longitude = int(avl_data[offset : offset + 8], 16) / 10000000.0
            offset += 8
            
            latitude = int(avl_data[offset : offset + 8], 16) / 10000000.0 
            offset += 8
            
            altitude = int(avl_data[offset : offset + 4], 16)
            offset += 4
            
            angle = int(avl_data[offset : offset + 4], 16)
            offset += 4
            
            satellites = int(avl_data[offset : offset + 2], 16)
            offset += 2
            
            speed = int(avl_data[offset : offset + 4], 16)
            offset += 4
            
            io_data, offset, button_action = await self.decode_io_data(avl_data, offset)
            
            records["records"].append({
                "button_action" : button_action,
                "timestamp"     : timestamp,
                "priority"      : priority,
                "longitude"     : longitude,
                "latitude"      : latitude,
                "altitude"      : altitude,
                "angle"         : angle,
                "satellites"    : satellites,
                "speed"         : speed,
                "io_data"       : io_data
            })
            
        return records
        
    async def decode_data(self):
        # Removing zero bytes and data size
        response = {"records" : []}
        self.data_packet = self.data_packet[16:]
        
        codec_id = self.data_packet[:2]
        if codec_id not in ['8E','8e']:
            return response, '00'
        
        number_of_records = int(self.data_packet[2:4], 16)
        
        response = await self.decode_avl_packet(response, self.data_packet[4:-10], number_of_records)
        
        return response, struct.pack(">I", number_of_records).hex()


class Codec12:
    def __init__(self, data_packet):
        self.data_packet = data_packet
        
    async def crc16_ibm(self, data) -> int:
        crc = 0x0000  # Initialize CRC to 0
        polynomial = 0xA001  # Polynomial used for CRC-16/IBM
    
        for byte in data:
            crc ^= byte  # XOR current byte with CRC
            for _ in range(8):  # Process each bit
                carry = crc & 0x0001  # Check the least significant bit
                crc >>= 1  # Shift CRC to the right by 1 bit
                if carry:
                    crc ^= polynomial  # XOR with the polynomial if carry is set
    
        return crc

    async def decimal_to_hex_4byte(self, decimal_value):
        hex_value = f"{decimal_value:08X}"
        formatted_hex = "".join(hex_value[i:i+2] for i in range(0, 8, 2))
        return str(formatted_hex)
        
    async def encode_data(self):
        zero_byte = await self.decimal_to_hex_4byte(0)
        
        codec_id = "0C"
        cmq1 = "01"
        cmd_type = "05"
        cmd_size = await self.decimal_to_hex_4byte(len(self.data_packet))
        cmd = codecs.encode(self.data_packet.encode(), 'hex').decode('utf-8')
        cmq2 = "01"

        center_value = f"{codec_id}{cmq1}{cmd_type}{cmd_size}{cmd}{cmq2}"

        data_size = await self.decimal_to_hex_4byte(len(center_value) // 2)  # Divide by 2 because hex size
        crc16 = await self.decimal_to_hex_4byte(await self.crc16_ibm(bytes.fromhex(center_value)))

        message = f"{zero_byte}{data_size}{center_value}{crc16}"

        return message
    
    async def decode_data(self):
        # Removing zero bytes and data size
        response = {"response" : {}}
        self.data_packet = self.data_packet[16:]
        
        codec_id = self.data_packet[:2]
        if not int(codec_id, 16) == 12:
            return response, '00'
        
        res_size = int(self.data_packet[6:14], 16)
        res = codecs.decode(self.data_packet[14:14+(res_size*2)], 'hex').decode('utf-8')
        
        response = await handle_decoded_packet(response, res.split(" "))
        
        return response, '01'
