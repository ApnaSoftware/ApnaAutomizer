# from read_smt import *
from timestamp import infix_to_prefix
from mathsat import *

# for rhs
# function to replace time stamp of 'variable' in 'formula' according to 'pre' 
def replace_with_time(formula, pre, post, variable, joke): 
    n=pre.find(variable)
    if(n==-1):
        return formula
    elif(pre[n+len(variable)]=="_"):
        j1=pre[n+len(variable):].find(" ")
        j2=pre[n+len(variable):].find(")")
        if(j1==-1):
            j=j2
        elif(j2==-1):
            j=j1
        else:
            j=min(j1,j2)
        if(not(j==-1)):
            new_var=pre[n:n+j+1]
        else:
            new_var=pre[n:len(pre)]
        formula=formula.replace(variable+" ",new_var+" ")
        formula=formula.replace(variable+")",new_var+")")
        n1=post.find(variable)
        if(post[n1+len(variable)]=="_" and joke ==0):
            for j in range(len(new_var)):
                if(new_var[j]=="_"):
                    x=j
            madar=variable+"_"+str(int(new_var[x+1:])+1)
            post=post.replace(new_var+" ",madar+" ")
            post=post.replace(new_var+")",madar+")")
        if(formula==variable):
            formula=new_var
    return (formula,post)

# function to check if 'var' is a variable in 'string'
def var_in(string, var):
    n=string.find(var)
    if(string[n+len(var)]=="_"):
        return True
    else:
        return False

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

# for lhs
# returns 'new_var' with current appropriate time stamp
# num=0 means assignment operator
# eg: pre = "< x_1 0" , post = "= x_2 0" , var = "x" , num = 0
# then returns "x_2"
# if num = 1 then returns "x_1"
def current_time(var,pre,post,num):
    if(var_in(pre,var)):
        var_new,post=replace_with_time(var,pre,post,var,1)
        if(num==0):
            time_of_var=var_new.replace(var+"_","")
            var_new=var+"_"+str(int(time_of_var)+1)
    elif(var_in(post,var)):
        var_new,post=replace_with_time(var,post,post,var,1)
        if(num==0):
            time_of_var=var_new.replace(var+"_","")
            var_new=var+"_"+str(int(time_of_var))
    else:
        var_new=var
    return var_new        

def is_valid_hoare_triple(env,pre,statement,post):
	#implement this
	#pre and post are msat declare types
	#f is of form in which they are in ats file transitions
    int_tp = msat_get_integer_type(env)

    # declare all the variables in statement
    for var in find_vars(statement):
        d = msat_declare_function(env, var, int_tp)
        assert(not(MSAT_ERROR_DECL(d)))

    # break statement into lhs, operator and rhs 
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

    # checking if operator is assignment then adding time stamps to lhs
    if(operator=="="):
        lhs=current_time(lhs,pre,post,0)
    else:
        lhs=current_time(lhs,pre,post,1)


    # adding time stamps in rhs
    chutiya=0

    for var in find_vars(rhs):
        if(var_in(pre,var)):
            chutiya+=1
            print "chutiyapanti"
            rhs,post=replace_with_time(rhs, pre, post, var, 0)
        elif(var_in(post,var)):
            chutiya+=1
            rhs,post=replace_with_time(rhs, post, post, var, 1)
            if (operator=="="):
                rhs

    # if(chutiya==0):
    #     return True

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
    print "[DEBUG] check Hoare Triple : {"+pre+"} "+statement+" {"+post+"}"

    # push
    msat_push_backtrack_point(env)

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
    res=msat_assert_formula(env,msat_make_not(env,post) )
    assert(res==0)

    # for madarchod in msat_get_asserted_formulas(env):
        # print "assetrion formula "+msat_to_smtlib2_term(env,madarchod)

    # if env is SAT then return False else return True
    res=msat_solve(env)
    if(res==MSAT_SAT):
        print "[DEBUG] Hoare Triple is NOT valid."

        # pop
        msat_pop_backtrack_point(env)
    	return False
    else:
        print "[DEBUG] Hoare Triple is valid."

        #pop
        msat_pop_backtrack_point(env)
        return True