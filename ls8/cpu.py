"""
CPU functionality.
"""

import sys

class CPU:
    """
    Main CPU class.
    """
    def __init__(self):
        """
        Construct a new CPU.
        """
        # Opcodes
        self.op = 0
        # RAM memory
        self.ram = [0]*255
        # Registers
        self.reg = [0]*8
        self.reg[7] = 0xF4
        # Program Counter
        self.pc = 0
        # Instruction Register
        self.ir = 0
        # Memory Address Register
        self.mar = 0
        # Memory Data Register
        self.mdr = 0
        # Flag Register
        self.fl = 0
        # Set Running Loop
        self.running = True
        # Stack Pointer
        self.sp = 7

        # in CPU opcodes
        # Loads registerA with the value at 
        # the memory address stored in registerB.
        self.LD = 0b10000011        # LD RegA, regB
        # Set the value of a register to an integer.
        self.LDI = 0b10000010       # LDI regA, integer
        self.PRN = 0b01000111       # PRN regA
        self.PRA = 0b01001000       # PRA regA
        # Halt the CPU (and exit the emulator).
        self.HLT = 0b00000001       # HLT
        # Add the value in two registers 
        # and store the result in registerA
        self.ADD = 0b10100000       # ADD regA, regB
        self.MUL = 0b10100010       # MUL regA, regB
        self.SUB = 0b10100001       # SUB regA, regB
        # Decrement (subtract 1 from) 
        # the value in the given register.
        self.DEC = 0b01100110       # DEC regA
        # ncrement (add 1 to) 
        # the value in the given register.
        self.INC = 0b01100101       # INC regA
        # divide the value in the first register
        # by the value in the second register,
        # storing the result in the first register
        self.DIV = 0b10100011       # DIV regA, regB     
        self.PUSH = 0b01000101      # PUSH regA
        self.POP = 0b01000110       # POP regA
        self.SHL = 0b10101100       # SHL regA, regB
        # Calls a subroutine (function) 
        # at the address stored in the register.
        self.CALL = 0b01010000      # CALL regA
        self.RET = 0b00010001       # RET
        # Compare the values in two registers.
        self.CMP = 0b10100111       # CMP regA, regB
        # Divide the value in the first register 
        # by the value in the second, storing 
        # the remainder of the result in registerA.
        self.MOD = 0b10100100       # MOD regA, regB
        #self.ADDI = 0b      # ADDI regA, regB
        # Bitwise-AND the values in registerA 
        # and registerB, then store the result in registerA.
        self.AND = 0b10101000       # AND regA, regB
        self.NOT = 0b01101001       # NOT regA
        self.OR  = 0b10101010       # OR regA, regB
        self.XOR = 0b10101011       # XOR regA, regB
        self.SHR = 0b10101101       # SHR regA, regB
        # Jump to the address stored 
        # in the given register.
        self.JPM = 0b01010100       # JMP regA
        # If equal flag is set (true), 
        # jump to the address stored in the given register.
        self.JEQ = 0b01010101       # JEQ regA
        # If greater-than flag or equal flag 
        # is set (true), jump to the address 
        # stored in the given register.
        self.JGE = 0b01011010       # JGE regA
        # If greater-than flag is set (true), 
        # jump to the address stored in the given 
        # register. 
        self.JGT = 0b01010111       # JGT regA
        # If less-than flag is set (true), 
        # jump to the address stored in the given 
        # register.
        self.JLT = 0b01011000       # JLT regA
        # If E flag is clear (false, 0), 
        # jump to the address stored in the given 
        # register.
        self.JNE = 0b01010110       # JNE regA
        # Issue the interrupt number stored 
        # in the given register. 
        self.INT = 0b01010010       # INT regA
        # Return from an interrupt handler.
        self.IRET = 0b00010011      # IRET 


    def load(self, file_name):
        """
        Load a program into memory.
        """
        address = 0
                
        # with open(file_name[1]) as file:
        with open(file_name) as file:
            
            for line in file.readlines():
                #str = line.strip().partition("#")[0]
                str = line.split("#")[0].strip()
                if len(str) == 0:
                    continue
                
                self.ram_write(address, int(str, 2))
                
                address +=1


    def alu(self, op, oper1, oper2):
        """
        ALU operations.
        """
        if op == "ADD":
            self.reg[oper1] += self.reg[oper2]

        # elif op == "ADDI":
        #      self.reg[oper1] += self.reg[oper2]

        elif op == "MUL":
            self.reg[oper1] *= self.reg[oper2]

        elif op == "SUB": 
            self.reg[oper1] -= self.reg[oper2]

        elif op == "DEC": 
            self.reg[oper1] -= self.reg[oper2]

        elif op == "DIV":
            if oper2 == 0:
                print('Error: Empty address, unable to complete computation')
                self.HLT()
            else:
                self.reg[oper1] //= self.reg[oper2]
             
        elif op == "MOD":
            if oper2 == 0:
                print('Error: Empty address, unable to complete computation')
                self.HLT()
            else:
                self.reg[oper1] %= self.reg[oper2]

        elif op == "CMP":
            # `FL` bits: `00000LGE`
            if self.reg[oper1] < self.reg[oper2]:
                self.fl = 0b00000100
            elif self.reg[oper1] > self.reg[oper2]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000001

        else:
            raise Exception("Unsupported ALU Operation")

    def trace(self):
        """
        Handy function to print out the CPU state. 
        You might want to call this from run() 
        if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
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
            
            instruction = execute_cmd & 0b00111111  # select opcode and mask
            operand_count = execute_cmd >> 6 
            opcode_size = (operand_count) +1        # shift to right 
            op_position = self.pc
            # operands = (self.ram_read(op_position + i) for i in range(operand_count))
                        
            oper1 = self.ram_read(self.pc+1) #next(operands) 
            oper2 = self.ram_read(self.pc+2) #next(oper1) 

            if execute_cmd == self.LDI: # 0b10000010            
                self.reg[oper1] = oper2

            elif execute_cmd == self.PRN: #0b01000111
                print(self.reg[oper1])

            elif execute_cmd == self.HLT: #0b00000001
                self.running = False

            elif execute_cmd == self.ADD:            
                self.alu("ADD", oper1, oper2)

            # elif execute_cmd == self.ADDI:            
            #     self.alu("ADDI", oper1, oper2)

            elif execute_cmd == self.MUL:
                self.alu("MUL", oper1, oper2)

            elif execute_cmd == self.SUB:
                self.alu("SUB", oper1, oper2)

            elif execute_cmd == self.DIV:
                self.alu("DIV", oper1, oper2)

            elif execute_cmd == self.CMP:
                self.alu("CMP", oper1, oper2)

            elif execute_cmd == self.MOD:            
                self.alu("MOD", oper1, oper2)

            elif execute_cmd == self.PUSH:
                # decrement
                self.reg[self.sp] -=1
                # add to stack at memory address assigned by 
                # decremented stack pointer
                self.ram[self.reg[self.sp]] = self.reg[oper1]

            elif execute_cmd == self.POP:
                # copy value at memory address assigned by 
                # stack pointer 
                self.reg[oper1] = self.ram[self.reg[self.sp]]
                # increment
                self.reg[self.sp] +=1

            elif execute_cmd == self.CALL:
                # get the address of the next instruction by adding 2 to 
                # the current instruction
                addr_next_inst = self.pc +2
                # decrement
                self.reg[self.sp] -=1
                # push the address of next instruction onto stack
                # for use in the Return instruction
                self.ram[self.reg[self.sp]] = addr_next_inst

                reg_index = oper1
                addr = self.reg[reg_index]
                self.pc = addr

            elif execute_cmd == self.RET:
                # copy value at memory address assigned by 
                # stack pointer into the pc 
                self.pc = self.ram[self.reg[self.sp]]
                # increment
                self.reg[self.sp] +=1

            elif execute_cmd == self.JPM:
                self.pc = self.reg[oper1]
                
            elif execute_cmd == self.JEQ:
                if self.fl == 0b00000001:
                    self.JMP()
                else:
                    self.pc += self.opcode_size

            elif execute_cmd == self.JNE:
                if self.fl != 0b00000001:
                    self.JMP()
                else:
                    self.pc += self.opcode_size

            elif execute_cmd == self.AND:
                self.reg[oper1] &= self.reg[oper2]

            elif execute_cmd == self.OR:
                self.reg[oper1] |= self.reg[oper2]

            elif execute_cmd == self.XOR:
                self.reg[oper1] ^= self.reg[oper2]

            elif execute_cmd == self.NOT:
                self.reg[oper1] != self.reg[oper2]

            elif execute_cmd == self.SHL:
                self.reg[oper1] <<= self.reg[oper2]

            elif execute_cmd == self.SHR:
                self.reg[oper1] >>= self.reg[oper2]

            else:
                self.trace()
                raise Exception(f'Unrecognized Instruction')

            # increment program counter as determined by opcode size
            if execute_cmd & 0b00010000 == 0:
                self.pc += opcode_size
                

    def ram_read(self, address):
        """
        Loads registerA with the value at the memory address 
        stored in registerB. This opcode reads from memory.
        """
        return self.ram[address]


    def ram_write(self, address, data):
        """
        Set the value of a register to an integer.
        """
        self.ram[address] = data


    def halt(self):
        """
        Halt the CPU and exit the emulator.
        """
        self.running = False
        sys.exit(0)
