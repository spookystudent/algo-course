

class Function:

    func = ''
    funcType = ''
    variables = {'x': '!x', 'y': '!y', 'z': '!z'}
    available_variables = []
    
    def __init__(self, F, FType):
        self.func = F
        self.funcType = FType
    
    
    
    



func = 'x*y*z + x*y*!z + x*y*z'
funcType = 'DNF'


manager = Function(func, funcType)
