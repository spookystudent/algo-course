import itertools


class Function:
    func = ""
    funcType = ""

    dictionary = {"x": "!x", "y": "!y", "z": "!z"}
    variables = []
    length = 0

    table = []
    items = []



    def __init__(self, F: str, FType: str):
        self.func = F
        self.funcType = FType

        self.set_dictionary()

        self.set_items()
        self.set_table()



    def set_variables(self, custom_variables):
        self.variables = []

        for var in custom_variables:
            if var in self.dictionary:
                self.variables.append(var)
            else:
                raise Exception(f'Переменной {var} нет в словаре!')
            
        self.set_items()
        self.set_table()


    def set_items(self):
        func = self.func
        items = []
        
        if self.funcType == 'DNF':
            items = func.replace(" ", "").split("+")
            items = list(map(lambda d: d.split("*"), items))
            
        elif self.funcType == 'KNF':
            items = func.replace(" ", "").replace("(", "").replace(")", "").split("*")
            items = list(map(lambda d: d.split("+"), items))
        self.items = items


    def set_table(self):
        table = []

        for values in itertools.product([0, 1], repeat=self.length):
            line = (values, self.run_function(values))
            table.append(line)

        self.table = table
        
        
    def set_dictionary(self):
        """
        Делаем таблицу переменных с учетом их индекса
        >> {'x': '!x', 'x1': '!x1'}
        """
        dictionary = dict()
        F = self.func
        F = F.replace(" ", "").replace("+", "").replace("*", "").replace("!", "").replace("(", "").replace(")", "")

        var = ""
        variables = []
        numbers = "0123456789"

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
            if var:
                variables.append(var)

        for var in set(variables):
            dictionary[var] = f"!{var}"

        self.dictionary = dictionary
        self.length = len(dictionary)
        self.variables = sorted(list(dictionary))


    def run_function(self, data):
        disjunct_values = []
        dictionary = self.variables
        not_dictionary = [self.dictionary[key] for key in dictionary]

        if self.funcType == "DNF":
            for disjunct in self.items:
                values = []

                for index, var in enumerate(disjunct):
                    if var in self.dictionary:
                        values.append(
                            data[dictionary.index(var)]
                        )
                    else:
                        values.append(
                            not(data[not_dictionary.index(var)])
                        )
                    
                disjunct_values.append(all(values))

            return any(disjunct_values)

        elif self.funcType == "KNF":
            for disjunct in self.items:
                values = []
                for index, var in enumerate(disjunct):
                    if var in self.dictionary:
                        values.append(data[index])
                    else:
                        values.append(not (data[index]))

                disjunct_values.append(any(values))

            return all(disjunct_values)


    def gluing(self, resultFuncType='DNF'):
        def gluing_groups(groups):
            process_groups = {}
            group_id = 1

            keys = sorted(list(groups))
            combinations = [
                (keys[i], keys[i + 1])
                for i in range(0, len(keys) - 1)
                if abs(keys[i] - keys[i + 1]) == 1
            ]

            was_combined = set()
            cant_combined = set()

            for key1, key2 in combinations:
                if not (key1 >= 0 and key2 >= 0):
                    continue
                group1, group2 = groups[key1], groups[key2]

                for minterm1 in group1:
                    flag = False


                    for minterm2 in group2:
                        diff_count = sum(
                            1 for a, b in zip(minterm1, minterm2) if a != b
                        )

                        if diff_count == 1:
                            was_combined.add("".join(minterm1))
                            was_combined.add("".join(minterm2))

                            new_minterm = []
                            for a, b in zip(minterm1, minterm2):
                                if a == b:
                                    new_minterm.append(str(a))
                                else:
                                    new_minterm.append("-")

                            flag = True

                            new_minterm = "".join(new_minterm)

                            if group_id not in process_groups:
                                process_groups[group_id] = set()

                            elif -group_id not in process_groups:
                                process_groups[-group_id] = set()

                            process_groups[group_id].add(new_minterm)

                    flag = False
                group_id += 1
    
            

            for key in groups:
                for minterm in groups[key]:
                    if minterm not in was_combined:
                        cant_combined.add(minterm)

            return process_groups, cant_combined


        minterms = []
        for line in self.table:
            values, f = line
            if f and resultFuncType == 'DNF':
                minterms.append(values)
            elif not f and resultFuncType == 'KNF':
                minterms.append(values)

        groups = {minterm.count(1): set() for minterm in minterms}

        for minterm in minterms:
            groups[minterm.count(1)].add("".join([str(i) for i in minterm]))

        result_groups = []
        result_minterms = set()

        new_groups, minterms = gluing_groups(groups)

        while new_groups:
            groups = new_groups

            new_groups, minterms = gluing_groups(groups)

            [result_minterms.add(minterm) for minterm in minterms]
        else:
            for key in groups:
                [result_minterms.add(minterm) for minterm in groups[key] if key > 0]
                [result_minterms.add(minterm) for minterm in minterms]

        result_minterms = self.check_minterms(result_minterms, resultFuncType=resultFuncType)
        
        return result_minterms


    def check_minterms(self, minterms, resultFuncType = 'DNF'):
        cover_minterms = {}
        for line in self.table:
            values, f = line
            if f and resultFuncType == "DNF":
                consitute = ''.join([str(i) for i in values])
                
                for minterm in minterms:
                    flag = True
                    for a, b in zip(consitute, minterm):
                        if a != b and b != '-':
                            flag = False
                    if flag:
                        if consitute not in cover_minterms: cover_minterms[consitute] = [minterm]
                        else: cover_minterms[consitute].append(minterm)
    
            elif not f and resultFuncType == 'KNF':
                consitute = ''.join([str(i) for i in values])
                
                for minterm in minterms:
                    flag = True
                    for a, b in zip(consitute, minterm):
                        if a != b and b != '-':
                            flag = False
                    if flag:
                        if consitute not in cover_minterms: cover_minterms[consitute] = [minterm]
                        else: cover_minterms[consitute].append(minterm)
        
        result_minterms = set()
        for key in cover_minterms:
            if len(cover_minterms[key]) == 1: result_minterms.add(cover_minterms[key][0])
        
        return result_minterms


    

    def change_variables(self, custom_dictionary):
        sorted_dictionary = self.variables
        func = self.func

        for a, b in zip(sorted_dictionary, custom_dictionary):
            func = func.replace(a, f'#{a}#')

        for a, b in zip(sorted_dictionary, custom_dictionary):
            func = func.replace(f'#{a}#', b)
        
        self.func = func



    def create_function(self, minterms, resultFuncType="DNF"):
        dictionary = self.variables
        items: list[list] = []

        for minterm in minterms:
            item = list(minterm)
            for index, bit in enumerate(minterm):
                if bit != "-":
                    if bit == "1":
                        item[index] = dictionary[index]
                    elif bit == "0":
                        item[index] = self.dictionary[dictionary[index]]

            while '-' in item: item.remove("-")
            items.append(item)

        raw_items = items
        items = []

        if resultFuncType == 'DNF':
            for item in raw_items:
                items.append("*".join(item))

            return " + ".join(items)
        
        elif resultFuncType == 'KNF':
                
            result = ''
            for item in raw_items:
                if len(item) == 1:
                    items.append(''.join(item))
                else:
                    items.append(f'({" + ".join(item)})')
                    
            return '*'.join(items)



    def minimize(self, resultFuncType='DNF'):
        minterms = self.gluing(resultFuncType=resultFuncType)

        self.func = self.create_function(minterms, resultFuncType=resultFuncType)


# func = '!x*y*z + x*y*!z + x*y*z'
# func = '(x + !y + z) * !x * (y + z)'

func = '!x * y * z + x * y * !z + x * y * z'
# func = '!x * !y * z + !x * !y * !z + x * y * !z + x * y * z'
# func = 'x * y * !z * !q + x * !y * !z * !q + x * y * !z * q + !x * y * !z * q + !x * y * !z * !q + !x * !y * !z * !q'
funcType = "DNF"

# func = '(X1 + !X4)*(X2 + !X4)*(!X1+!X2+X4)'
# funcType = "KNF"



manager = Function(func, funcType)
# manager.set_variables(['x', 'y', 'z', 'w'])

# print(manager.variables, "F")
# for line in manager.table:
#     print(line)

# print()
manager.minimize(resultFuncType='KNF')
print(manager.func)
# print(manager.items)
# for line in manager.table:
#     print(line)
# print(manager.dictionary)
