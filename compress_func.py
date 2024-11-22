import itertools

class Function:
    
    func = ''
    funcType = ''
    
    dictionary = {'x': '!x', 'y': '!y', 'z': '!z'}
    length = 0
    
    table = []
    items = []
    
    
    def __init__(self, F: str, FType: str):
        self.func = F
        self.funcType = FType
        
        
        self.set_dictionary()
        
        self.set_items()
        self.set_table()
        
            
    def run_function(self, data):
        disjunct_values = []

        if self.funcType == 'DNF':
            for disjunct in self.items:
                values = []
                for index, var in enumerate(disjunct):
                    if var in self.dictionary:
                        values.append(data[index])
                    else:
                        values.append(not(data[index]))
                        
                disjunct_values.append(all(values))
                
            return any(disjunct_values)
        else:
            for disjunct in self.items:
                values = []
                for index, var in enumerate(disjunct):
                    if var in self.dictionary:
                        values.append(data[index])
                    else:
                        values.append(not(data[index]))
                        
                disjunct_values.append(any(values))
                
            return all(disjunct_values)
        
        

    def set_dictionary(self):
        """
            Делаем таблицу переменных с учетом их индекса
            >> {'x': '!x', 'x1': '!x1'}
        """
        dictionary = dict()
        F = self.func
        F = F \
            .replace(' ', '') \
            .replace('+', '') \
            .replace('*', '') \
            .replace('!', '')
            
        var = ''
        variables = []
        numbers = '0123456789'
        
        for i in range(0, len(F)):
            char = F[i]
            
            if char not in numbers and not var:
                var = char

            elif char not in numbers and var:
                variables.append(var)
                var = char 
            
            elif char in numbers and var:
                var += char
        else:
            if var: variables.append(var)

        
        for var in set(variables): dictionary[var] = f'!{var}'
            
        self.dictionary = dictionary
        self.length = len(dictionary)
        
    # https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%9A%D1%83%D0%B0%D0%B9%D0%BD%D0%B0_%E2%80%94_%D0%9C%D0%B0%D0%BA-%D0%9A%D0%BB%D0%B0%D1%81%D0%BA%D0%B8#%D0%A8%D0%B0%D0%B3_2:_%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%8B%D1%85_%D0%B8%D0%BC%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D0%BD%D1%82
        
    def gluing(self):
        minterms = []
        for line in self.table:
            values, f = line
            if f: minterms.append(values)

        minterms_by_count = {minterm.count(1): [] for minterm in minterms}
    
        for minterm in minterms:
            minterms_by_count[minterm.count(1)].append(minterm)
            
        print(minterms_by_count)
        # Получение импликантов 1 ого уровня
        combined = []
        not_combined = []
        keys = list(minterms_by_count)
        combinations = [(keys[i], keys[i + 1]) for i in range(0, len(keys) - 1)]
        
        
        for key1, key2 in combinations:
            group1, group2 = minterms_by_count[key1], minterms_by_count[key2]
            
            for minterm1 in group1:
                for minterm2 in group2:
                    diff_count = sum(1 for a, b in zip(minterm1, minterm2) if a != b)
                    
                    if diff_count == 1:
                        combined_minterms = []
                        for a, b in zip(minterm1, minterm2):
                            if a == b: combined_minterms.append(a)
                            else: combined_minterms.append('-')
                        combined.append(combined_minterms)
                    else:
                        not_combined.append(minterm1)
        print(combined)
        print(minterms)
            
            
        # for i in range(len(minterms_by_count)):
        #     for j in range(i + 1, len(minterms_by_count)):
        #         m1, m2 = minterms[i], minterms[j]
                
        #         diff_count = sum(1 for a, b in zip(m1, m2) if a != b)
                
        #         if diff_count == 1:
        #             combined_minterms = []
        #             for a, b in zip(m1, m2):
        #                 if a == b: combined_minterms.append(a)
        #                 else: combined_minterms.append(-1)
        #             combined.append(combined_minterms)
        return 'combined'
    
    def set_items(self):
        func = self.func
        items = func.replace(' ', '').split('+')
        items = list(map(
            lambda d: d.split('*'),
            items
        ))
            
        self.items = items
    
    def set_table(self):
        table = []
        
        for values in itertools.product([0,1],repeat=self.length):
            line = (values, self.run_function(values))
            table.append(line)
            
        self.table = table
    



# func = '!x*y*z + x*y*!z + x*y*z'
# func = '!x*y*!z*!t + x*!y*!z*!t + x*!y*z*!t + x*!y*z*t + x*y*!z*!t + x*y*z*t'
# func =  a b c d  a b c d  a bcd  a b c d  abcd abcd  ab cd.
func = '!a*!b*!c*!d + !a*b*c* + !a*b*c*d + a*b*!c*d + a*b*c*d + a*b*c*!d + a*b*c*!d + a*!b'
funcType = 'DNF'


manager = Function(func, funcType)
# manager.gluing()
print(sorted(list(manager.dictionary)), 'F')
for line in manager.table:
    print(line)

