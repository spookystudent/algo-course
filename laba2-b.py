import itertools

F = [int(input()) for i in range(8)]
# F = [0]*8
# F = [0,
# 1,
# 0,
# 1,
# 1,
# 1,
# 0,
# 1,
# ]

class Function:
    func = ''
    chained_items = ''
    
    raw_variations = {'x': '(not(x))', 'y': '(not(y))', 'z': '(not(z))'}
    variations = {
        '(not(x))': '!x',
        '(not(y))': '!y',
        '(not(z))': '!z'
    }
        
    F = []
    items = []
    
    
    def __init__(self, F: list[int]) -> None:
        self.F = F
        self.items = []


    def run_function(self, func: str, data: tuple) -> bool:
        f, x, y, z = data
        
        func = func.replace('x', str(x)).replace('y', str(y)).replace('z', str(z))

        return eval(func)
    
    
    def add_item(self, item) -> None:
        chained_items = ' * '.join([*self.items, item])
        self.items.append(item)
        self.chained_items = chained_items
        
    
    def delete_trash(self, table) -> list:
        for line in table:
            f, x, y, z = line
            
            if f:
                for item in self.items:
                    if not self.run_function(item, line):
                        self.items.remove(item)


    def create_item(self, F, x, y, z) -> str:
        variables = {'x': x, 'y': y, 'z': z}

        prepared = []
        result = []
        
        for variant in self.raw_variations:
            if variables[variant]:
                prepared.append(variant) # x
                
            elif not variables[variant]:
                prepared.append(self.raw_variations[variant]) # not(x)   

        item = f'({"+".join(prepared)})'
        
        return item
    
    
    def prepare_items(self) -> str:
        self.chained_items = ' * '.join(self.items)
        for key in self.variations:
            self.chained_items = self.chained_items.replace(key, self.variations[key])
        
        return self.chained_items
        
    
    
    def get_function(self) -> str:
        table = []
        i = 0
        for x, y, z in itertools.product([0,1], repeat=3):
            table.append((self.F[i], x, y, z))
            i += 1
            
        for line in table:
            f, x, y, z = line

            item = self.create_item(f, x, y, z)
            self.add_item(item)
                
        self.delete_trash(table)
        
        return self.prepare_items()


manager = Function(F)
func = manager.get_function()

print(func)
