import string
import os
import re
#sets of lowercasr and uppercase letters
lower_case = string.ascii_lowercase
upper_case = string.ascii_uppercase

#The goal of this class is to show LL1 parsing and code generation
class LL1_parser_codegenerator():
    def __init__(self, grammer, input_str):
        self.allowed_ligicaloperators = ['&', '|', '<', '<=', '>', '>=', '==', '!=']
        self.logical_operators = []
        self.grammer = grammer
        self.input_str = input_str
        self.processed_input = []
        self.LL1_stack = []
        self.temp_startaddress = 600
        self.variable_startaddress = 400
        self.variable_address = {}
        self.ss = []
        self.terminals = ''
        self.PB = []
        self.i = 0   

     
    #returns a temperoray variable's address
    def get_temp(self):
        temp_address = self.temp_startaddress
        self.temp_startaddress += 1
        return temp_address

    #processes the input and changes terminals into "id" and logical operators into "(co)". Also adds the logical_operators in to it's list
    def terminal_string_generator(self):
        self.input_str = self.input_str.replace(" " , "")
        #split the input with this separators and put themselfs into the list
        temp_processed_input = re.split('(\)|\(|\+|\:=|\*|\==|\!=|\>|\<|\<=|\>=|\&&|if|while|do)|\n|\t',self.input_str)
        #filters the None elements from the lists
        temp_processed_input = list(filter(None, temp_processed_input))
        for i in temp_processed_input:
            if i in self.allowed_ligicaloperators:
                self.logical_operators.append(i)
                self.processed_input.append('(co)')
            elif i in lower_case:
                self.terminals += i
                self.processed_input.append('id')
                if i not in self.variable_address:
                    self.variable_address[i] = self.variable_startaddress
                    self.variable_startaddress +=1
            else:
                self.processed_input.append(i)
        self.processed_input.append('$')



    def match(self):
        self.LL1_stack.pop(0)
        self.processed_input.pop(0)

    # returns the address of the given variable
    def find_address(self, variable):
        return self.variable_address[variable]

    def pid(self):
        terminal = self.terminals[0]
        self.terminals = self.terminals[1:]
        address = self.find_address(terminal)
        self.ss.append(address)
        self.LL1_stack.pop(0)

    def assign(self):
        self.PB.append('(:= ,' + str(self.ss[-1]) + ',' + '   ' + ',' + str(self.ss[-2]) + ')')
        self.ss.pop(-1)
        self.ss.pop(-1)
        self.LL1_stack.pop(0)
        self.i += 1

    def add(self):
        t = self.get_temp()
        self.PB.append('(+ ,' + str(self.ss[-2]) + ',' + str(self.ss[-1]) + ',' + str(t) + ')')
        self.ss.pop(-1)
        self.ss.pop(-1)
        self.LL1_stack.pop(0)
        self.ss.append(t)
        self.i += 1
    
    def mult(self):
        t = self.get_temp()
        self.PB.append('(* ,' + str(self.ss[-2]) + ',' + str(self.ss[-1]) + ',' + str(t) + ')')
        self.ss.pop(-1)
        self.ss.pop(-1)
        self.LL1_stack.pop(0)
        self.ss.append(t)
        self.i += 1

    def label(self):
        self.ss.append(self.i)
        self.LL1_stack.pop(0)


    def save(self):
        self.ss.append(self.i)
        self.LL1_stack.pop(0)
        self.PB.append('')
        self.i += 1


    def jmpf(self):
        self.PB[self.ss[-1]] = '(jmpf ,' + str(self.ss[-2]) + ',' + '   ' + ',' + str(self.i) + ')'
        self.LL1_stack.pop(0)
        self.ss.pop(-1)
        self.ss.pop(-1)


    def jmpt(self):
        self.PB[self.i] = '(jmpt ,' + str(self.ss[-1]) + ',' + '   ' + ',' + str(self.ss[-2]) + ')'
        self.LL1_stack.pop(0)
        self.i += 1
        self.ss.pop(-1)
        self.ss.pop(-1)

    def jmp_save(self):
        self.PB[self.ss[-1]] = '(jmpf ,' + str(self.ss[-2]) + ',' + '   ' + ',' + str((self.i)+1) + ')'
        self.LL1_stack.pop(0)
        self.ss.pop(-1)
        self.ss.pop(-1)
        self.ss.append(self.i)
        self.i += 1


    def jmp_jmpf(self):
        self.PB.append('(jmp ,' + '   ' + ',' + '   ' + ',' + str(self.ss[-3]) + ')')
        self.i += 1
        self.PB[self.ss[-1]] = '(jmpf ,' + str(self.ss[-2]) + ',' + '   ' + ',' + str(self.i) +')'
        self.LL1_stack.pop(0)
        self.ss.pop(-1)
        self.ss.pop(-1)
        self.ss.pop(-1)

    #this function generates code for logical calculations
    def BE(self):
        t = self.get_temp()
        self.PB.append('(' +str(self.logical_operators[0]) +' ,' + str(self.ss[-2]) + ',' + str(self.ss[-1]) + ',' + str(t) + ')')
        self.ss.pop(-1)
        self.ss.pop(-1)
        self.logical_operators.pop(0)
        self.LL1_stack.pop(0)
        self.ss.append(t)
        self.i += 1


    #This function LL1Parse the input and generates 3 address code and also prints them
    def parse(self):
        self.LL1_stack.append('S')
        self.LL1_stack.append('$')

        self.terminal_string_generator()

        while self.processed_input != []:
            if self.LL1_stack[0] == self.processed_input[0]:
                self.match()
            elif self.LL1_stack[0] == '@pid':
                self.pid()
            elif self.LL1_stack[0] == '@assign':
                self.assign()
            elif self.LL1_stack[0] == '@add':
                self.add()
            elif self.LL1_stack[0] == '@mult':
                self.mult()
            elif self.LL1_stack[0] == '@label':
                self.label()
            elif self.LL1_stack[0] == '@save':
                self.save()
            elif self.LL1_stack[0] == '@jmpf':
                self.jmpf()
            elif self.LL1_stack[0] == '@jmpt':
                self.jmpt()
            elif self.LL1_stack[0] == '@jmp-save':
                self.jmp_save()
            elif self.LL1_stack[0] == '@jmp-jmpf':
                self.jmp_jmpf()
            elif self.LL1_stack[0] == '@BE':
                self.BE()
            elif self.LL1_stack[0] in upper_case:
                key = self.LL1_stack[0]
                self.LL1_stack.pop(0)
                temp_list = []

                for j in self.LL1_stack:
                    temp_list.append(j)
                self.LL1_stack = []
                
                for i in self.grammer[key][self.processed_input[0]]:
                    self.LL1_stack.append(i)

                for k in temp_list:
                    self.LL1_stack.append(k)
            #not needed
            # elif self.processed_input[0] in self.allowed_ligicaloperators:


            else:
                print("Error!")
                print("LL1 stack = ", self.LL1_stack)
                print("input = ", self.processed_input)
                break
            
            #this prints the LL1 parse
            # print(self.LL1_stack, '\t', self.processed_input)
        #this prints the 3 address code
        for i in self.PB:
            print(i)
        print('\n\n\n')

            

#The purpose of this class is to get grammer and input then toggle the LL1_parser_codegenerator class
class Activate():
    def __init__(self):
        self.grammer_dic = {}
        self.input_str = ''

    def grammer(self, grammer_file_address):
        try:
            with open(grammer_file_address, 'r') as grammer_file:
                grammer_read = grammer_file.read()
                grammer_dic = eval(grammer_read)
                self.grammer_dic = grammer_dic
        except IOError:
            print("File does not exist!")

    def input_string(self):
        input_file_address = input('Please enter your input file address: ')
        try:
            with open(input_file_address, 'r') as input_file:
                input_string = input_file.read()
                self.input_str = input_string
        except IOError:
            print("File does not exist!")

    def LL1_parse(self):
        parse_code_object = LL1_parser_codegenerator(self.grammer_dic, self.input_str)
        parse_code_object.parse()

    def code_generate(self):
        parse_code_object = LL1_parser_codegenerator(self.grammer_dic, self.input_str)
        parse_code_object.generate()


def menu():
    print("Welcome!")
    
    activator = Activate()

    #default grammer
    activator.grammer('grammers/ekhtiyari.txt')

    while True:
        print(" 1.Enter your grammer file address (optional) \n 2.Enter your input file address (mandatory) \n 3.LL1 parse \n 0.Exit")
        choice = input()

        if choice == '0':
            print("Khosh galdin!")
            break
        elif choice == '1':
            grammer_file_address = input('Please enter your grammer file address: ')
            activator.grammer(grammer_file_address)
        elif choice == '2':
            activator.input_string()
        elif choice == '3':
            if activator.input_str != '':
                clear = lambda: os.system('cls')
                clear()
                activator.LL1_parse()
            else:
                print("Enter the input file first!")
        else:
            print("Wrong Input!")
