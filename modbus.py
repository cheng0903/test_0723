from pymodbus.client.tcp import ModbusTcpClient

class Modbus:
    def __init__(self, host, port, address, count):  # 建構子
        self.host = host
        self.port = port
        self.address = address
        self.count = count
    
    def read(self):
        modbus_reader = ModbusTcpClient( host=self.host , port =self.port)
        result = modbus_reader.read_input_registers( address= self.address, count=self.count)
        print(result.registers)

if __name__ == '__main__':
    modbus1= Modbus(host="127.0.0.1",port=502, address=0, count=3)
    modbus1.read()