import string
#sets of lowercasr and uppercase letters
lower_case = string.ascii_lowercase
upper_case = string.ascii_uppercase

#The goal of this class is to show LL1 parsing and code generation
class LL1_parser_codegenerator():
    def __init__(self, grammer, input_str):
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

    #generate a code for each variable
    def terminal_string_generator(self):
        temp_processed_input = self.input_str.split()
        for i in temp_processed_input:
            if i in lower_case:
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
        self.PB.append('(= ,' + str(self.ss[-1]) + ',' + '   ' + ',' + str(self.ss[-2]) + ')')
        self.ss.pop(-1)
        self.ss.pop(-1)
        self.LL1_stack.pop(0)

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

    # def label(self):

    # def save(slef):

    # def jmpf(self):

    # def jmpt(self):

    # def jmp_save(self):

    # def jmp_jmpf(self):

    #This function LL1Parse the input
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
            elif self.LL1_stack[0] == '@pid':
                self.pid()
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

            else:
                print("Error!")
                break

            print(self.LL1_stack, '\t', self.processed_input)
        print(self.PB)
            
    #This function generates three address code
    def generate(self):
        print(self.PB)


#The purpose of this class is to get grammer and input then toggle the LL1_parser_codegenerator class
class Activate():
    def __init__(self):
        self.grammer_dic = {}
        self.input_str = ''

    def grammer(self):
        grammer_file_address = input('Please enter your grammer file address: ')
        with open(grammer_file_address, 'r') as grammer_file:
            grammer_read = grammer_file.read()
            grammer_dic = eval(grammer_read)
            self.grammer_dic = grammer_dic

    def input_string(self):
        input_file_address = input('Please enter your input file address: ')
        with open(input_file_address, 'r') as input_file:
            input_string = input_file.read()
            self.input_str = input_string

    def LL1_parse(self):
        parse_code_object = LL1_parser_codegenerator(self.grammer_dic, self.input_str)
        parse_code_object.parse()

    def code_generate(self):
        parse_code_object = LL1_parser_codegenerator(self.grammer_dic, self.input_str)
        parse_code_object.generate()


def menu():
    print("Welcome!")
    
    activator = Activate()

    while True:
        print("Choices: \n 1.Enter your grammer file address \n 2.Enter your input file address \n 3.LL1 parse \n 4.Generate three address code \n 0.Exit")
        choice = input('Your choice: ')

        if choice == '0':
            print("Khosh galdin!")
            break
        elif choice == '1':
            activator.grammer()
        elif choice == '2':
            activator.input_string()
        elif choice == '3':
            activator.LL1_parse()
        elif activator == '4':
            activator.code_generate()

