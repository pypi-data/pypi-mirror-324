import codecs
import asyncio
from helper import handle_decoded_packet
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
        cmd = codecs.encode(self.data_packet, 'hex').decode('utf-8')
        cmq2 = "01"

        center_value = f"{codec_id}{cmq1}{cmd_type}{cmd_size}{cmd}{cmq2}"

        data_size = await self.decimal_to_hex_4byte(len(center_value) // 2)  # Divide by 2 because hex size
        crc16 = await self.decimal_to_hex_4byte(await self.crc16_ibm(bytes.fromhex(center_value)))

        message = f"{zero_byte}{data_size}{center_value}{crc16}"

        binary_message = bytes.fromhex(message)

        return binary_message
    
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


async def handle():
    # message_handler = Codec12("{setparam }")
    
    # message = await message_handler.encode_data()

    # print(message)
    
    # message_decoder = Codec12("00000000000000370C01060000002F4449313A31204449323A30204449333A302041494E313A302041494E323A313639323420444F313A3020444F323A3101000066E3")
    
    # message = await message_decoder.decode_data()

    # print(message)
    
    # codec8_response = Codec8("00000000000004ba080d000001948cdd2dd2012df7772810eea4f200000000000000001407ef01f00150011500c8004502716409b50000b60000420000180000cd0000ce0000430fea4400000d000004f100000000c700000000100000086e0c0000000000000001948cdd4920012df7772810eea4f200000000000000fd1508ef01f00150011500c80045027164fd0309b50000b60000420000180000cd0000ce0000430f8a4400000d000004f100000000c700000000100000086e0c0000000000000001948cdd609a012df7772810eea4f200000000000000fd1508ef01f00150011500c80045027164fd0209b50000b60000420000180000cd0000ce00a3430f6a4400000d000004f100000000c700000000100000086e0c0000000000000001948cdd6478012df7772810eea4f200000000000000fd1508ef01f00150011500c80045027164fd0309b50000b60000420000180000cd0000ce00a3430f684400000d000004f100000000c700000000100000086e0c0000000000000001948cdd7418012df7772810eea4f200000000000000fd1508ef01f00150011504c80045027163fd0209b50000b60000420000180000cdf68cce00a3430f3e4400000d000004f100009ddac700000000100000086e0c0000000000000001948cdd8f70012df7772810eea4f200000000000000fd1508ef01f00150011504c80045027163fd0309b50000b60000420000180000cdbfbece00a3430f444400000d000004f100009ddac700000000100000086e0c0000000000000001948cdd9358012df7772810eea4f200000000000000fd1508ef01f00150011504c80045027163fd0209b50000b60000420000180000cdbfbece00a3430ef14400000d000004f100009ddac700000000100000086e0c0000000000000001948cdd9b28012df7772810eea4f200000000000000fd1508ef01f00150011505c80045027162fd0309b50000b60000420000180000cdbfbece00a3430efc4400000d000004f100009ddac700000000100000086e0c0000000000000001948cddca12012df7772810eea4f200000000000000fd1508ef01f00150011505c80045027161fd0309b50000b60000420000180000cdbfbece00a3430f2e4400000d000004f100009ddac700000000100000086e0c0000000000000001948cdde182012df7772810eea4f200000000000000fd1508ef01f00150011505c80045027161fd0309b50000b60000420000180000cdbfbece00a3430f2c4400000d000004f100009ddac700000000100000086e0c0000000000000001948cdde196012df7772810eea4f200000000000000fd1508ef01f00150011505c80045027161fd0309b50000b60000420000180000cdbfbece00a3430ee94400000d000004f100009ddac70000000010000008")
    # response = await codec8_response.decode_data()
    
    # print(response)

    codec8_response = Codec8E("00000000000000588e010000019472cec4c8012df747f510eea0a600fb01270c00000185000d000700f00100150500c800004501007128007401018522000500b5000900b600070018000000430e6601820000000100f100009dda00000000010000335a")
    response = await codec8_response.decode_data()
    
    print(response)


    
asyncio.run(handle())