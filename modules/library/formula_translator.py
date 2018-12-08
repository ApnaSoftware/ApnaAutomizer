# OPERATORS = set(['+', '-', '*', '/', '(', ')', '=', '==', '>', '>=', '<', '<='])
# PRIORITY = {'+':1, '-':1, '*':2, '/':2, '=':3, '==':0, '>':3, '>=':0, '<':3, '<=':3}

OPERATORS = set(['+', '-', '*', '/', '(', ')', '==', '>', '>=', '<', '<=', '!='])
PRIORITY = {'+':1, '-':1, '*':2, '/':2,  '==':0, '>':0, '>=':0, '<':0, '<=':0, '!=':0}

### INFIX ===> PREFIX ###
def infix_to_prefix(formula):
    op_stack = []
    exp_stack = []
    formula = formula.split()
    for ch in formula:
        if not ch in OPERATORS:
            exp_stack.append(ch)
        elif ch == '(':
            op_stack.append(ch)
        elif ch == ')':
            while op_stack[-1] != '(':
                op = op_stack.pop()
                a = exp_stack.pop()
                b = exp_stack.pop()
                exp_stack.append( '('+op+' '+b+' '+a+')')
            op_stack.pop() # pop '('
        else:
            while op_stack and op_stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[op_stack[-1]]:
                op = op_stack.pop()
                a = exp_stack.pop()
                b = exp_stack.pop()
                exp_stack.append('('+op+' '+b+' '+a+')' )
            op_stack.append(ch)
    
    # leftover
    while op_stack:
        op = op_stack.pop()
        a = exp_stack.pop()
        b = exp_stack.pop()
        exp_stack.append( '('+op+' '+b+' '+a+')' )
    k = l = exp_stack[-1]
    while k.rsplit("(-",1)[0] != k:
        [k,m] = k.rsplit("(-",1) 
        l =  "(- ".join([k,m]) + l[len(k+m)+2:]
    return l
