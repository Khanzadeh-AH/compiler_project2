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
    def __init__(self):
        self.temp_startaddress = 600
        self.variable_startaddress = 400
        self.ss = Stack()
        self.variable_adresses = {}


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
        s

    def add(self):

    
    def multiply(self):

    
    def label(self):


    def save(slef):



    def jmpf(self):


    def jmpt(self):


    def jmp_save(self):



    def jmp_jmpf(self):

