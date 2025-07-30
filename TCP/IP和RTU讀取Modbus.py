from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.client.serial import ModbusSerialClient
import time 
import threading 

class ModbusTCPserver:
    def __init__(self, host:str, port:int, address:int, count:int, name:str, method:str):
        self.host = host
        self.port = port
        self.address = address
        self.count = count
        self.name= name
        self.method = method
        

    def _readInputReg(self):
        modbus_TCP_reader = ModbusTcpClient( host=self.host , port =self.port)
        result = modbus_TCP_reader.read_input_registers(address=self.address, count=self.count)
        return result
    
    def _readHodingReg(self):
        modbus_TCP_reader = ModbusTcpClient( host=self.host , port =self.port)
        result = modbus_TCP_reader.read_holding_registers(address=self.address, count=self.count)
        return result

    def Excute(self):
        if self.method == 'Input':
            result = self._readInputReg()
        elif self.method == 'Hold':
            result = self._readHodingReg()
        else:
            print("Method Error")
        return result
       



class ModbusRTUClient:
    def __init__(self, port, baudrate:int,bytesize:int, parity,
                 stopbits:int, slave:int,address:int,count:int, name:str, method:str):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.slave = slave
        self.address = address
        self.count = count
        self.name= name
        self.method = method
        print(port)
        self.modbus_RTU_reader = ModbusSerialClient(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity,
                 stopbits=self.stopbits)
    def _readInputReg(self):
        result = self.modbus_RTU_reader.read_input_registers(address=self.address, count=self.count, slave=self.slave)
        return result
    
    def _readHodingReg(self):
        result = self.modbus_RTU_reader.read_holding_registers(address=self.address, count=self.count,  slave=self.slave)
        return result

    def Excute(self):
        if self.method == 'Input':
            result = self._readInputReg()
        elif self.method == 'Hold':
            result = self._readHodingReg()
        else:
            print("Method Error")
        return result

if __name__ == '__main__':
    System= ModbusTCPserver(host="127.0.0.1",port=502, address=0, count=14, name="System", method="Input")
    print(System.Excute())
    PCS= ModbusTCPserver(host="127.0.0.1",port=503, address=0, count=14, name="PCS", method="Input")
    print(PCS.Excute())
    BMS=ModbusRTUClient(port="COM2", baudrate=9600, bytesize=8, parity="N",
                 stopbits=1, slave=98,address=0, count=8, name="BMS", method="Input")
    print(BMS.Excute())
    METER=ModbusRTUClient( port="COM4", baudrate=9600, bytesize=8, parity="N",
                 stopbits=1, slave=99,address=0, count=33, name="METER", method="Hold")
    print(METER.Excute())


   