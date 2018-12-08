def existing_var(string,vars):
    for j in range(len(vars)):
        if(string==vars[j]):
            return True
    return False

def index_of(string,vars):
    for j in range(len(vars)):
        if(string==vars[j]):
            return j
    return -1

def find_vars(string1):
    string=string1
    string=string.replace("(","")
    string=string.replace(")","")
    string=string.replace("/ ","")
    string=string.replace("+ ","")
    string=string.replace("== ","")
    string=string.replace("- ","")
    string=string.replace("!= ","")
    string=string.replace("* ","")
    string=string.replace("<= ","")
    string=string.replace(">= ","")
    string=string.replace("= ","")
    string=string.replace("< ","")
    string=string.replace("> ","")
    string=string.replace("  "," ")
    var=string.split(" ")
    x=0
    for j in range(len(var)):
        if(var[j-x]=="" or var[j-x][0]=="0" or var[j-x][0]=="1" or var[j-x][0]=="2" or var[j-x][0]=="3" or var[j-x][0]=="4" or var[j-x][0]=="5" or var[j-x][0]=="6" or var[j-x][0]=="7" or var[j-x][0]=="8" or var[j-x][0]=="9"):
            var.pop(j-x)
            x+=1
    return var


def current_time(time,vars,formula,operator,lhs):
    for variable in find_vars(formula):
        if(time[index_of(variable,vars)]==-1):
            vars.append(variable)
            time.append(1)
        if(operator=="=" and lhs==variable):
            new_var=variable+"_"+str(time[index_of(variable,vars)]-1)
        else:
            new_var=variable+"_"+str(time[index_of(variable,vars)])
        formula=formula.replace(variable+" ",new_var+" ")
        formula=formula.replace(variable+")",new_var+")")
        if(formula==variable):
            formula=new_var
    return formula


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
        l =  "(-".join([k,m]) + l[len(k+m)+2:]
    return l

def time_stamp(string,vars,time):
    oper=""
    for j in range(len(string)):
        if(string[j]==" "):
            k=j
            lhs=string[0:j]
            break
    for j in range(k+1,len(string)):
        if(string[j]==" "):
            operator=string[k+1:j]
            rhs=string[j+1:len(string)]
            break
    if (operator=="="):
        oper="="
        if(existing_var(lhs,vars)):
            time[index_of(lhs,vars)]+=1
        else:
            vars.append(lhs)
            time.append(1)
    kinky_stuff=0    
    if(operator=="=="):
        operator = "="
    elif(operator=="!="):
        kinky_stuff=1
        operator= "="
    if(not(existing_var(lhs,vars))):
        vars.append(lhs)
        time.append(1)
    if(kinky_stuff==1):
        return "(not ("+operator+" "+lhs+"_"+str(time[index_of(lhs,vars)])+" "+current_time(time,vars,infix_to_prefix(rhs),oper,lhs)+"))"
    else:
        return "("+operator+" "+lhs+"_"+str(time[index_of(lhs,vars)])+" "+current_time(time,vars,infix_to_prefix(rhs),oper,lhs)+")"