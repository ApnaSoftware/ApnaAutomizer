import os
import automata_operations


def generate_trace(input_file,iteration):


    automata_operations.execute_automatascript(input_file, "temp.txt", "trace",iteration)

    file = open("temp/temp.txt", "r")
    p = "print(getAcceptedWord(nfa"
    k = ""
    while p not in k:
        k = file.readline()
    s = file.readline()
    f = [line for line in [line.strip() for line in s.split("\"")] if line]
    return f

    # f=[]
    # f.append("(= x 0)")
    # f.append("(= x1 (+ x 1))")
    # f.append("(< x1 1)")

