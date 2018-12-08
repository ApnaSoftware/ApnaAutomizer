from timestamp import infix_to_prefix
from mathsat import *


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
def replace_with(formula, variable, new_variable,x):
    formula=formula.replace(variable+" ",new_variable+" ")
    formula=formula.replace(variable+")",new_variable+")")
    n=formula.find(variable)
    if(not(n==-1) and x==1):
        if(formula[n:len(formula)]==variable):
            formula=formula[:n]+new_variable
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

def remove_time_stamps(formula):
    for vars in find_vars(formula):
        n=vars.find("_")
        if(not(n==-1) and not(vars[n+1:]=="real")):
            new_var=vars[:n]
            formula=replace_with(formula,vars,new_var,0)
    return formula

# return the list of all the variables in 'string'
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


# def is_valid_hoare_triple(pre,statement,post):
def is_valid_hoare_triple(env,pre,statement,post,verbose):

    int_tp = msat_get_integer_type(env)

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
    
    # push
    msat_push_backtrack_point(env)
    
    if(operator=="="):
        lhs_init=lhs
        if(pre==post):
            lhs_temp=find_var_with_time(pre,lhs)
            if(lhs_temp=="error"):
                lhs=lhs+"_0"
                d = msat_declare_function(env, lhs, int_tp)
                assert(not(MSAT_ERROR_DECL(d)))
            else:
                lhs=change_time(lhs_temp,1)
                post=replace_with(post,lhs_temp,lhs,0)
            for var in find_vars(rhs):
                new_var=find_var_with_time(pre,var)
                if(new_var=="error"):
                    d = msat_declare_function(env, var, int_tp)
                    assert(not(MSAT_ERROR_DECL(d)))
                else:
                    rhs=replace_with(rhs,var,new_var,1)
        else:
            lhs_temp=find_var_with_time(pre,lhs)
            if(lhs_temp=="error"):
                lhs_temp=find_var_with_time(post,lhs)
                if(lhs_temp=="error"):
                    lhs=lhs+"_0"
                    for vars in find_vars(post):
                        n=vars.find("_")
                        if(not(n==-1)):
                            new=vars[:n]
                        else:
                            new=vars
                        new_var = find_var_with_time(pre,new)
                        if(not(new_var=="error")):
                            post=replace_with(post,vars,new_var,0)
                    d = msat_declare_function(env, lhs, int_tp)
                    assert(not(MSAT_ERROR_DECL(d)))
                else:
                    lhs=lhs_temp
            else:
                lhs=change_time(lhs_temp,1)

            for var in find_vars(rhs):
                
                new_var=find_var_with_time(pre,var)
                if(new_var=="error"):
                    new_var=find_var_with_time(post,var)
                    if(new_var=="error"):
                        d = msat_declare_function(env, lhs, int_tp)
                        assert(not(MSAT_ERROR_DECL(d)))
                    else:
                        if(var==lhs_init):
                            new_var=change_time(lhs,-1)
                            rhs=replace_with(rhs,var,new_var,1)
                            continue
                        # new_var=change_time(new_var,-1)
                        d = msat_declare_function(env, new_var, int_tp)
                        assert(not(MSAT_ERROR_DECL(d)))
                        rhs=replace_with(rhs,var,new_var,1)
                else:
                    rhs=replace_with(rhs,var,new_var,1)
    else:
        pre=remove_time_stamps(pre)
        post=remove_time_stamps(post)
        # for vars in find_vars(pre):
        #     d = msat_declare_function(env, vars, int_tp)
        #     assert(not(MSAT_ERROR_DECL(d)))
        # for vars in find_vars(post):
        #     d = msat_declare_function(env, vars, int_tp)
        #     assert(not(MSAT_ERROR_DECL(d)))
        for vars in find_vars(statement):
            d = msat_declare_function(env, vars, int_tp)
            assert(not(MSAT_ERROR_DECL(d)))

        # lhs_temp=find_var_with_time(pre,lhs)
        # if(lhs_temp=="error"):
        #     lhs_temp=find_var_with_time(post,lhs)
        #     if(lhs_temp=="error"):
        #         d = msat_declare_function(env, lhs, int_tp)
        #         assert(not(MSAT_ERROR_DECL(d)))
        #     else:
        #         lhs=lhs_temp
        # else:
        #     lhs=lhs_temp
        # for var in find_vars(rhs):
        #     new_var=find_var_with_time(pre,var)
        #     if(new_var=="error"):
        #         new_var=find_var_with_time(post,var)
        #         if(new_var=="error"):
        #             d = msat_declare_function(env, lhs, int_tp)
        #             assert(not(MSAT_ERROR_DECL(d)))
        #         else:
        #             rhs=replace_with(rhs,var,new_var)
        #     else:
        #         rhs=replace_with(rhs,var,new_var)

    # replacing "==" by "="
    kinky_stuff=0
    if(operator=="=="):
        operator="="
    elif(operator=="!="):
        operator="="
        kinky_stuff=1

    # writing statement in smtlib2 term
    if(kinky_stuff==1):
        statement="(not ("+operator+" "+lhs+" "+infix_to_prefix(rhs)+"))"
    else:
        statement="("+operator+" "+lhs+" "+infix_to_prefix(rhs)+")"
    # print statement

    # for Debugging
    if verbose:
        print "[DEBUG] check Hoare Triple : {"+pre+"} "+statement+" {"+post+"}"

    

    # creating msat terms from pre, statement, post
    statement=msat_from_string(env,statement)
    assert(not(MSAT_ERROR_TERM(statement)))
    pre=msat_from_string(env,pre)
    assert(not(MSAT_ERROR_TERM(pre)))
    post=msat_from_string(env,post)
    assert(not(MSAT_ERROR_TERM(post)))

    # asserting (pre) and (statement) and (not (post))
    res=msat_assert_formula(env, pre)
    assert(res==0)
    res=msat_assert_formula(env, statement)
    assert(res==0)
    res=msat_solve(env)
    # if(res==MSAT_UNSAT):
    #     if(msat_to_smtlib2_term(env,post)=="false"):
    #         print "[DEBUG] Hoare Triple is valid.   diff"        
    #         msat_pop_backtrack_point(env)
    #         return True
    #     print "[DEBUG] Hoare Triple is NOT valid.   diff"        
    #     msat_pop_backtrack_point(env)
    #     return False

    res=msat_assert_formula(env,msat_make_not(env,post))
    assert(res==0)

    # for madarchod in msat_get_asserted_formulas(env):
    #     print "assetrion formula "+msat_to_smtlib2_term(env,madarchod)

    # if env is SAT then return False else return True
    res=msat_solve(env)
    if(res==MSAT_SAT):
        if verbose:
            print "[DEBUG] Hoare Triple is NOT valid."

        # pop
        msat_pop_backtrack_point(env)
    	return False
    else:
        if verbose:
            print "[DEBUG] Hoare Triple is valid."

        #pop
        msat_pop_backtrack_point(env)
        return True
                    
    # print lhs
    # print operator
    # print rhs
    # print pre
    # print post
                    


# is_valid_hoare_triple("(= x_1 1)","x = x + 1","(= x_2 1)")



    

    