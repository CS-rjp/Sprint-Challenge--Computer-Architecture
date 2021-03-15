"""
CPU functionality.
"""

import sys

class CPU:
    """
    Main CPU class.
    """
    def __init__(self, op, reg_a, reg_b, pc):
        """
        Construct a new CPU.
        """
        # Opcodes
        self.op = op
        # RAM memory
        self.ram = ram = [0]*255
        # Registers
        self.reg_a = reg_a = [0]*8
        self.reg_b = reg_b = [0]*8
        # Program Counter
        self.pc = pc = 0
        # Instruction Register
        self.ir = ir = 0
        # Memory Address Register
        self.mar = mar = 0
        # Memory Data Register
        self.mdr = mdr = 0
        # Flag Register
        self.fl = fl = 0
        # Set Running Loop
        self.running = running = True
     

    def load(self):
        """
        Load a program into memory.
        """
        address = 0

        # hardcoded opcodes
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # NOP
            0b00001000,
            0b01000111, # PRN R0
            0b00000000, # NOP
            0b00000001, # HLT
        ]

        # create an 
        for instruction in program:
            # find address of the currently executing instruction
            self.ram[address] = instruction
            # increment the program counter
            address += 1


    def alu(self, op, reg_a, reg_b):
        """
        ALU operations.
        """
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. 
        You might want to call this from run() 
        if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """
        Run the CPU. ()
        """
        while self.running:
            execute_cmd = self.ram_read(self.pc)

            if execute_cmd == 0b10000010: #LDI
                oper1 = self.ram_read(self.pc+1)
                oper2 = self.ram_read(self.pc+2)

                self.reg[oper1] = oper2
                self.pc +=3

            elif execute_cmd == 0b01000111: #PRN
                oper1 = self.ram_read(self.pc +1)
                print(self.reg[oper1])
                self.pc += 2

            elif execute_cmd == 0b00000001: #HLT
                self.running = False
                self.pc +=1
                

    def ram_read(self, address):
        """
        Loads registerA with the value at the memory address 
        stored in registerB. This opcode reads from memory.
        """
        return self.ram[address]

    def ram_write(self, address):
        """
        Set the value of a register to an integer.
        """
        self.ram[address] = data

    def halt(self):
        running = False
