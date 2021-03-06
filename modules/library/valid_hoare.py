

def find_var_with_time(formula, variable):
    start=formula.find(variable+"_")
    if(start==-1):
        return "error"
    # if(start==-1):
    #     start1=formula.find(variable+" ")
    #     start1=formula.find(variable+")")
    #     if(start1==-1):
    #         start=start2
    #     elif(start2==-1):
    #         start=start1
    #     else:
    #         start=min(start1,start2)
    #     if(start==-1):
    #         return -1
    start+=len(variable)
    end1=formula[start:].find(" ")
    end2=formula[start:].find(")")
    end=-1
    if(end1==-1):
        end=end2
    elif(end2==-1):
        end=end1
    else:
        end=min(end1,end2)
    if(end==-1):
        print "[Syntax Error] : Error in find_var_with_time in valid_hoare.py for formula "+formula
        return ""
    return formula[start-len(variable):end+start]
# print find_var_with_time("(jgggj_56 asd_123 ah_76)", "ah")

# return formula with changed variable 
# input should be given with time stamps
def replace_with(formula, variable, new_variable):
    formula=formula.replace(variable+" ",new_variable+" ")
    formula=formula.replace(variable+")",new_variable+")")
    return formula
# print replace_with("(= x_2 0)", "x_2", "x_1")

# return variable with changed time stamp
def change_time(variable,change):
    n=variable.find("_")+1
    if(n==0):
        return variable+"_"+str(change-1)
    time=int(variable[n:])
    new_time=time+change
    return variable[:n]+str(new_time)
# print change_time("zdfsg_1",3)

# return the list of all the variables in 'string'
def find_vars(string):
    string=string.replace("(","")
    string=string.replace(")","")
    string=string.replace("= ","")
    string=string.replace("+ ","")
    string=string.replace("== ","")
    string=string.replace("- ","")
    string=string.replace("* ","")
    string=string.replace("< ","")
    string=string.replace("<= ","")
    string=string.replace(">= ","")
    string=string.replace("> ","")
    string=string.replace("!= ","")
    var=string.split(" ")
    for j in range(len(var)):
        if(var[j][0]=="0" or var[j][0]=="1" or var[j][0]=="2" or var[j][0]=="3" or var[j][0]=="4" or var[j][0]=="5" or var[j][0]=="6" or var[j][0]=="7" or var[j][0]=="8" or var[j][0]=="9"):
            var.pop(j)
    return var


def is_valid_hoare_triple(pre,statement,post):
# def is_valid_hoare_triple(env,pre,statement,post):

    # int_tp = msat_get_integer_type(env)

    for j in range(len(statement)):
        if(statement[j]==" "):
            k=j
            lhs=statement[0:j]
            break
    for j in range(k+1,len(statement)):
        if(statement[j]==" "):
            operator=statement[k+1:j]
            rhs=statement[j+1:len(statement)]
            break
    
    if(operator=="="):
        if(pre==post):
            lhs_temp=find_var_with_time(pre,lhs)
            if(lhs_temp=="error"):
                print "declare"
                # d = msat_declare_function(env, lhs, int_tp)
                # assert(not(MSAT_ERROR_DECL(d)))
            else:
                lhs=change_time(lhs_temp,1)
                post=replace_with(post,lhs_temp,lhs)
            for var in find_vars(rhs):
                new_var=find_var_with_time(pre,var)
                if(new_var=="error"):
                    print "declare"
                    # d = msat_declare_function(env, var, int_tp)
                    # assert(not(MSAT_ERROR_DECL(d)))
                else:
                    rhs=replace_with(rhs,var,new_var)
        else:
            lhs_temp=find_var_with_time(pre,lhs)
            if(lhs_temp=="error"):
                lhs_temp=find_var_with_time(post,lhs)
                if(lhs_temp=="error"):
                    print "declare"
                    # d = msat_declare_function(env, lhs, int_tp)
                    # assert(not(MSAT_ERROR_DECL(d)))
                else:
                    lhs=lhs_temp
            else:
                lhs=change_time(lhs_temp,1)

            for var in find_vars(rhs):
                new_var=find_var_with_time(pre,var)
                if(new_var=="error"):
                    new_var=find_var_with_time(post,var)
                    if(new_var=="error"):
                        print "declare"
                        # d = msat_declare_function(env, lhs, int_tp)
                        # assert(not(MSAT_ERROR_DECL(d)))
                    else:
                        new_var=change_time(new_var,-1)
                        rhs=replace_with(rhs,var,new_var)
                else:
                    rhs=replace_with(rhs,var,new_var)
    else:
        print "kush"

        lhs_temp=find_var_with_time(pre,lhs)
        if(lhs_temp=="error"):
            lhs_temp=find_var_with_time(post,lhs)
            if(lhs_temp=="error"):
                print "declare"
                # d = msat_declare_function(env, lhs, int_tp)
                # assert(not(MSAT_ERROR_DECL(d)))
            else:
                lhs=lhs_temp
        else:
            lhs=lhs_temp
        for var in find_vars(rhs):
            new_var=find_var_with_time(pre,var)
            if(new_var=="error"):
                new_var=find_var_with_time(post,var)
                if(new_var=="error"):
                    print "declare"
                    # d = msat_declare_function(env, lhs, int_tp)
                    # assert(not(MSAT_ERROR_DECL(d)))
                else:
                    rhs=replace_with(rhs,var,new_var)
            else:
                rhs=replace_with(rhs,var,new_var)
                    
    print lhs
    print operator
    print rhs
    print pre
    print post
                    


is_valid_hoare_triple("(= x_1 1)","x = x + 1","(= x_2 1)")



    

    