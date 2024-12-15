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


    def run_function(self, data):
        disjunct_values = []
        dictionary = self.variables
        not_dictionary = [self.dictionary[key] for key in dictionary]

        # print(self.variables)
        # print(not_dictionary)

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



    def set_dictionary(self):
        """
        Делаем таблицу переменных с учетом их индекса
        >> {'x': '!x', 'x1': '!x1'}
        """
        dictionary = dict()
        F = self.func
        F = F.replace(" ", "").replace("+", "").replace("*", "").replace("!", "")

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



    def gluing(self):
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

                    # print(f'Check minterm {minterm1}')
                    for minterm2 in group2:
                        diff_count = sum(
                            1 for a, b in zip(minterm1, minterm2) if a != b
                        )
                        print(f' Сравниваем {minterm1} & {minterm2} from {key1} & {key2} diff count = {diff_count}')
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

                            print(f' - Получили {new_minterm}')

                            if group_id not in process_groups:
                                process_groups[group_id] = set()

                            elif -group_id not in process_groups:
                                process_groups[-group_id] = set()

                            process_groups[group_id].add(new_minterm)

                            # print(process_groups)

                            # if -group_id in was_combined:
                            #     if new_minterm in process_groups[-group_id]:
                            #         process_groups[-group_id].remove(new_minterm)

                        else:
                            pass
                            # if "".join(minterm2) not in was_combined:
                            #     if -group_id not in process_groups:
                            #         process_groups[-group_id] = set()

                            #     process_groups[-group_id].add("".join(minterm2))
                        print(f' Сравнили {minterm1} & {minterm2} from {key1} & {key2} {"*" if flag else ""} diff count = {diff_count}')
                    print()

                    # if not flag:
                    #     cant_combined.add("".join(minterm1))
                    flag = False
                group_id += 1
            
            [print(k, groups[k]) for k in sorted(groups)]
            print()
            [print(k, process_groups[k]) for k in sorted(process_groups)]
            print()

            print('Были изнасилованы', was_combined)
            

            for key in groups:
                for minterm in groups[key]:
                    if minterm not in was_combined:
                        cant_combined.add(minterm)

            print('Остались', cant_combined)
            return process_groups, cant_combined

        # =================
        minterms = []
        for line in self.table:
            values, f = line
            if f:
                minterms.append(values)

        groups = {minterm.count(1): set() for minterm in minterms}

        for minterm in minterms:
            groups[minterm.count(1)].add("".join([str(i) for i in minterm]))

        result_groups = []
        result_minterms = set()

        new_groups, minterms = gluing_groups(groups)
        print(minterms)
        while new_groups:
            groups = new_groups

            [print(k, groups[k]) for k in sorted(groups)]
            print()

            new_groups, minterms = gluing_groups(groups)
            print(minterms)
            [result_minterms.add(minterm) for minterm in minterms]
        else:
            for key in groups:
                [result_minterms.add(minterm) for minterm in groups[key] if key > 0]
                [result_minterms.add(minterm) for minterm in minterms]

        return result_minterms



    def set_items(self):
        func = self.func
        items = func.replace(" ", "").split("+")
        items = list(map(lambda d: d.split("*"), items))

        self.items = items



    def set_table(self):
        table = []

        for values in itertools.product([0, 1], repeat=self.length):
            line = (values, self.run_function(values))
            table.append(line)

        self.table = table

    

    def change_variables(self, custom_dictionary):
        sorted_dictionary = self.variables
        func = self.func

        for a, b in zip(sorted_dictionary, custom_dictionary):
            func = func.replace(a, f'#{a}#')

        for a, b in zip(sorted_dictionary, custom_dictionary):
            func = func.replace(f'#{a}#', b)
        
        self.func = func



    def create_function(self, minterms):
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

        for item in raw_items:
            items.append("*".join(item))

        return " + ".join(items)



    def minimize(self):
        minterms = self.gluing()

        self.func = self.create_function(minterms)


# func = '!x*y*z + x*y*!z + x*y*z'
# func = '!x*y*!z*!t + x*!y*!z*!t + x*!y*z*!t + x*!y*z*t + x*y*!z*!t + x*y*z*t'
# func =  a b c d  a b c d  a bcd  a b c d  abcd abcd  ab cd.
# func = '!a*!b*!c*!d + !a*b*c* + !a*b*c*d + a*b*!c*d + a*b*c*d + a*b*c*!d + a*b*c*!d + a*!b'
# func = "A*!B*!C + A*!B*!D + A*C*!D"
# func = "!x1*!x2*x3*x4 + !x1*x2*!x3*x4 + !x1*x2*x3*x4 + x1*!x2*!x3*!x4 + x1*!x2*x3*!x4 + x1*!x2*x3*x4 + x1*x2*!x3*!x4 + x1*x2*x3*!x4"
func = "!x1*!x3*!x4 + x2*!x3*!x4 + x1*x3 + x1*x2"
func = "!x*!y*!z*!w + !x*y*!z*!w + x*!y*z*!w + x*!y*z*w + x*y*!z*!w + x*y*!z*w + x*y*z*!w + x*y*z*w"

funcType = "DNF"


manager = Function(func, funcType)
manager.set_variables(['x', 'y', 'z', 'w'])

print(manager.variables, "F")
for line in manager.table:
    print(line)

# print()
manager.minimize()

print(manager.func)

