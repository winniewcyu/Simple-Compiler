class SymbolTableNode:
    def __init__(self, name, type_, type_pointer, scope, size):
        self.name = name
        self.type = type_
        self.type_pointer = type_pointer
        self.scope = scope
        self.size = size
        self.left = None
        self.right = None

class TypePointerNode:
    def __init__(self, name, type_, type_pointer, offset):
        self.name = name
        self.type = type_
        self.type_pointer = type_pointer
        self.offset = offset
        self.left = None
        self.right = None
    
class ArraryTableNode:
    def __init__(self, type_, type_pointer, length, size):
        self.type = type_
        self.type_pointer = type_pointer
        self.length = length
        self.size = size
        self.left = None
        self.right = None
    
class FunctionTableNode:
    def __init__(self, return_type, params_num, params_pointer, local_var):
        self.return_type = return_type
        self.params_num = params_num
        self.params_pointer = params_pointer
        self.local_var = local_var
        self.left = None
        self.right = None
    
class FunctionSymbolTableNode:
    def __init__(self, name, type_, type_pointer, scope, size):
        self.name = name
        self.type = type_
        self.type_pointer = type_pointer
        self.scope = scope
        self.size = size
        self.left = None
        self.right = None

class SymbolTable:
    def __init__(self):
        self.root = None
        self.type_table = None
        self.array_table = None
        self.function_table = None
        self.function_symbol_table = None

    def calculate_size(self, type_ , length):
        if length > 0:
            if type_ == "int":
                return length * 4
            elif type_ == "double":
                return length * 8
            elif type_ == "char":
                return length
            else:
                print("Invalid type")
                return None
        else:
            print("Invalid length")
            return None

    def insert(self, name, type_, type_pointer, scope, size):
        new_node = SymbolTableNode(name, type_, type_pointer, scope, size)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if name < current.name:  # Insert left
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:  # Insert right
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
    
    def insert_type_pointer(self, name, type_, type_pointer, offset):
        new_node = TypePointerNode(name, type_, type_pointer, offset)
        return new_node

    def insert_array(self, type_, type_pointer, length, size):
        new_node = ArraryTableNode(type_, type_pointer, length, size)
        return new_node
                
    def insert_function(self, return_type, params_num, params_pointer, local_var):
        new_node = FunctionTableNode(return_type, params_num, params_pointer, local_var)
        return new_node

    def insert_function_symbol(self, name, type_, type_pointer, scope, size):
        new_node = FunctionSymbolTableNode(name, type_, type_pointer, scope, size)
        return new_node
    
    def search(self, name):
        current = self.root
        while current:
            if name == current.name:
                return current
            current = current.left if name < current.name else current.right
        return None
    
    def search_type_pointer(self, name):
        current = self.type_table
        while current:
            if name == current.name:
                return current
            current = current.left if name < current.name else current.right
        return None
    
    def search_array(self, name):
        current = self.array_table
        while current:
            if name == current.name:
                return current
            current = current.left if name < current.name else current.right
        return None
    
    def search_function(self, name):
        current = self.function_table
        while current:
            if name == current.name:
                return current
            current = current.left if name < current.name else current.right
        return None
    
    def search_function_symbol(self, name):
        current = self.function_symbol_table
        while current:
            if name == current.name:
                return current
            current = current.left if name < current.name else current.right
        return None
    
    def display(self):
        print("\nSymbol Table:")
        for name, attributes in self.symbols.items():
            print(f"{name} -> {attributes}")
    
# test case
"""
int x ; 
int add ( int a , int b ){
    int sum = a + b ;
    return sum ;
}
"""

# Example usage
if __name__ == "__main__":
    sym_table = SymbolTable()
    sym_table.insert("x", "int", "NULL", 2, 4)
    param1 = sym_table.insert_function_symbol("a", "int", "NULL", 2, 4)
    param2 = sym_table.insert_function_symbol("b", "int", "NULL", 2, 4)
    return_var = sym_table.insert_function_symbol("sum", "int", "NULL", 2, 4)
    func = sym_table.insert_function("int", 2, [param1, param2], return_var)
    sym_table.insert("add", "funct", func, 1, None)
    
    print(sym_table.search("x").type)
