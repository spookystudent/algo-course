import itertools

F = [int(input()) for i in range(8)]


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

        return eval(func.replace('x', str(x)).replace('y', str(y)).replace('z', str(z)))
    
    
    def add_item(self, item) -> None:
        chained_items = ' + '.join([*self.items, item])
        self.items.append(item)
        self.chained_items = chained_items
    
    
    def check_item(self, item: str, data: tuple) -> bool:
        f, x, y, z = data

        if item not in self.items:
            chained_items = ' + '.join([*self.items, item])

            if self.run_function(chained_items, data) == f:
                self.add_item(item)
                self.chained_items = chained_items
        
                return True
        else:
            pass
            
            
        
    def create_item(self, F, x, y, z) -> str:
        variables = {'x': x, 'y': y, 'z': z}

        prepared = []
        result = []
        
        for variant in self.raw_variations:
    
            if variables[variant]:
                prepared.append(variant) # x
                
            elif not variables[variant]:
                prepared.append(self.raw_variations[variant]) # not(x)
                    

        result.append('*'.join(prepared))
        
        return result
    
    
    def prepare_items(self) -> str:
        for key in self.variations:
            self.chained_items = self.chained_items.replace(key, self.variations[key])
    
    
    def get_function(self) -> str:
        table = []
        i = 0
        for x, y, z in itertools.product([0,1], repeat=3):
            table.append((self.F[i], x, y, z))
            i += 1
            
        for line in table:
            f, x, y, z = line

            if f:
                variations_of_item = self.create_item(f, x, y, z)
                for item in variations_of_item:

                    if not self.items:
                        self.add_item(item)
                    else:
                        self.check_item(item, line)

                

        self.prepare_items()
        
        return self.chained_items 


manager = Function(F)
print(manager.get_function())