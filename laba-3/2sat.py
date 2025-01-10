class Solver2SAT:
  
  var = 'x'
  
  def get(self, arr, key):
    if key in arr: return arr[key]
  
  
  def implecator(self, f: str) -> str:
    # (a ∨ b) ∧ (a ∨ c) ∧ (~b ∨ c) ∧ (~b ∨ a)
    
    blocks = list(
      map(
        lambda x: x.replace('(', '').replace(')', '').strip(),
        f.split('AND')
      )
    )
  
    components = list(
      map(
        lambda block: block.replace(' ', '').split('OR'),
        blocks
      )
    )
    
    new_components = []
    for component in components:
      var1, var2 = component
      
      _var1, _var2 = list(map(
        lambda var: var.replace('~', '') if '~' in var else f'~{var}',
        component
      ))
      
      
      new_components.append((_var1, var2))
      new_components.append((_var2, var1))
      
    
    print(components)
    components = new_components
    print(components)
    
  
  def solve(self, f: str) -> str:
    self.implecator(f)
    
    

    
    
    

TwoSAT = Solver2SAT()

# TwoSAT.solve('(x1 OR x2) AND (x1 OR x3) AND (~x2 OR x3) AND (~x2 OR x1)')
TwoSAT.solve('(a OR b) AND (a OR c) AND (~b OR c) AND (~b OR a)')
