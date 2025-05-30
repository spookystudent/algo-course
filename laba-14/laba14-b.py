import sys

def query(func):
    print(func)
    sys.stdout.flush()
    return int(input())

class Function:
    func = ""
    modified_func = ""

    dictionary = {}
    variables = []
    length = 0

    table = []
    items = []

    results = []


    def __init__(self, F: str, n: int):
        self.func = F
        self.results = [None] * n

        self.set_dictionary()


    def set_dictionary(self):
        """
        Делаем таблицу переменных с учетом их индекса
        >> {'x': '!x', 'x1': '!x1'}
        """
        dictionary = dict()
        F = self.func
        F = F.replace(" ", "").replace("+", "").replace("*", "").replace("~", "").replace("(", "").replace(")", "")

        var = ""
        variables = []
        numbers = "0123456789"

        for i in range(len(F)):
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

    
    def solve(self):
        F = self.func
        var = 1
        for i in range(len(self.results)):
            modified_func = F.replace(f'{self.variables[i]}', f'{var}')
            
            response = query(modified_func)

            if response == 1:
                self.results[i] = var
            else:
                self.results[i] = int(not var)

            
        if self.results.count(None) == 0 or not all(self.results):
            print("satisfiable")
            print(' '.join(map(str, self.results)))
        else:
            print("unsatisfiable")



# n = 3
# func = 'x1*~(x3+~x2)'


n = int(input())
func = input().strip()

manager = Function(func, n)
manager.solve()