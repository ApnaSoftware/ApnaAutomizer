def find_vars(string):
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
        if(var[j-x][0]=="0" or var[j-x][0]=="1" or var[j-x][0]=="2" or var[j-x][0]=="3" or var[j-x][0]=="4" or var[j-x][0]=="5" or var[j-x][0]=="6" or var[j-x][0]=="7" or var[j-x][0]=="8" or var[j-x][0]=="9"):
            var.pop(j-x)
            x+=1
    return var

print find_vars("(<= (+ i_1 (* (- 1) n_1))")