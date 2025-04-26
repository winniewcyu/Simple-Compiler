import sortedcontainers

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
        self.length = scope
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
    
    def inorder_traversal(self, node=None):
        if node is None:
            node = self.root
        if node:
            self.inorder_traversal(node.left)
            print(f"Name: {node.name}, Type: {node.type}, Scope: {node.scope}, Size: {node.size}")
            self.inorder_traversal(node.right)
       
    def type_pointer_inorder_traversal(self, node=None):
        if node is None:
            node = self.type_table
        if node:
            self.type_pointer_inorder_traversal(node.left)
            print(f"Name: {node.name}, Type: {node.type}, Offset: {node.offset}")
            self.type_pointer_inorder_traversal(node.right)

    def array_inorder_traversal(self, node=None):
        if node is None:
            node = self.array_table
        if node:
            self.array_inorder_traversal(node.left)
            print(f"Type: {node.type}, Length: {node.length}, Size: {node.size}")
            self.array_inorder_traversal(node.right)
         
    def function_inorder_traversal(self, node=None):
        if node is None:
            node = self.function_symbol_table
        if node:
            self.function_inorder_traversal(node.left)
            print(f"Name: {node.name}, Type: {node.type}, Scope: {node.scope}, Size: {node.size}")
            self.function_inorder_traversal(node.right)
    
    def function_pointer_inorder_traversal(self, node=None):
        if node is None:
            node = self.function_table
        if node:
            self.function_pointer_inorder_traversal(node.left)
            print(f"Name: {node.name}, Type: {node.type}, Offset: {node.offset}")
            self.function_pointer_inorder_traversal(node.right)

# Example usage
if __name__ == "__main__":
    sym_table = SymbolTable()
    sym_table.insert("x", "double", None, 2, 8) 
    sym_table.insert("y", "int", None, 2, 4)
    sym_table.insert("z", "char", None, 2, 1)
    sym_table.insert_function("int",1 ,sym_table.insert_function_symbol("c", "int", None, 2, 4) ,sym_table.insert_function_symbol("b", "double", None, 2, 8) )
    
    sym_table.inorder_traversal()
    print(sym_table.search("x").size)
