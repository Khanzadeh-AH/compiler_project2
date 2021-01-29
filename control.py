#stack data structure
class Stack():
    def __init__(self):
        self.stack = []

    #returns top object of the stack
    def top(self, num=0):
        n = -1 + num
        return self.stack[n]

    #for pushing objects into stack
    def push(self,obj):
        self.stack.append(obj)

    #for popping objects from stack    
    def pop(self, num=1):
        for i in range(num):
            self.stack.pop()


#The goal of this class is to show LL1 parsing and code generation
class LL1_parser_codegenerator():
    def __init__(self, grammer, input_str):
        self.grammer = grammer
        self.input_str = input_str
        self.temp_startaddress = 600
        self.variable_startaddress = 400
        self.ss = Stack()
        self.variable_adresses = {}
        self.PB = []
        self.i = 0   
     
    #returns a temperoray variable's address
    def get_temp(self):
        temp_address = self.temp
        self.temp += 1
        return temp_address

    #generate a code for each variable
    def generate_address(self, variable):
        address = self.variable_startaddress
        self.variable_startaddress += 1
        self.variable_adresses[variable] = address

    # returns the address of the given variable
    def find_address(self, variable):
        return self.variable_adresses[variable]

    def pid(self, id):
        address = self.findaddress(id)
        self.ss.push(address)

    def assign(self):
        self.PB.append('(= ,' + str(self.ss.top()) + ',' + '    ' + ',' + str(self.ss.top(-1)) + ')')

    def add(self):
        t = self.get_temp()
        self.PB.append('(+ ,' + str(self.ss.top(-1)) + ',' + str(self.ss.top()) + ',' + str(t) + ')')
        self.ss.pop(2)
        self.ss.push(t)
        self.i += 1
    
    def mult(self):
        t = self.get_temp()
        self.PB.append('(* ,' + str(self.ss.top(-1)) + ',' + str(self.ss.top()) + ',' + str(t) + ')')
        self.ss.pop(2)
        self.ss.push(t)
        self.i += 1

    # def label(self):

    # def save(slef):

    # def jmpf(self):

    # def jmpt(self):

    # def jmp_save(self):

    # def jmp_jmpf(self):

    # #This function LL1Parse the input
    # def parse(self):

    # #This function generates three address code
    # def generate(self):


#The purpose of this class is to get grammer and input then toggle the LL1_parser_codegenerator class
class Activate():
    def __init__(self):
        self.grammer_dic = {}
        self.input_str = ''


    def grammer(self):
        grammer_file_address = input('Please enter your grammer file address: ')
        with open(grammer_file_address, 'r') as grammer_file:
            grammer_file.read()
            grammer_dic = eval(grammer_file)
            self.grammer_dic = grammer_dic

    def input_str(self):
        input_file_address = input('Please enter your input file address: ')
        with open(input_file_address, 'r') as input_file:
            input_string = input_file.read() + '$'
            self.input_str = input_string

    def LL1_parse(self):
        parse_code_object = LL1_parser_codegenerator()
        parse_code_object.parse()

    def code_generate(self):
        parse_code_object = LL1_parser_codegenerator()
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
            activator.input_str()
        elif choice == '3':
            activator.LL1_parse()
        elif activator == '4':
            activator.code_generate()
