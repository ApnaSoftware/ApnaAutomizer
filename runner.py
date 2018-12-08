import os
import sys
import time
import argparse

import modules.gentrace as gentrace 
import modules.geninterpolants as geninterpolants
import modules.hoare_automaton as hoare_automaton
import modules.automata_operations as automata_operations

#input_file is program automaton
#automaton must be named "nfa" ()
#result is result of verification

# for usage instructions : python runner.py -h




def runner(args):
    # fha = "floyd_hoare.ats"
    iteration = 0
    verification_done = False
    input_file = "temp/input.ats"
    os.system("cp "+args.filename+" ./"+input_file)
    alp = automata_operations.getalphabet(input_file)
    lib_automata_time = 0
    mathsat_time = 0
    while not verification_done:
        time_0 = time.time()
        print"\n\n[DEBUG] iteration count = "+ str(iteration)
        tr = gentrace.generate_trace(input_file,iteration)
        time_1 = time.time()
        print "[DEBUG] Trace generated : "+str(tr)
        iteration += 1
        if (tr == []):
            verification_done = True
            # print "\n[RESULT] Program is correct.\n"
            print "\nVerification Successful.\n"
        else:
            time_2 = time.time()
            if args.manual:
                (env,itp,jeez) = geninterpolants.get_interpolant_put_invariant(tr,args.interpol) #itp of msat type. env is the environment
            else:
                (env,itp,jeez) = geninterpolants.get_interpolant(tr,args.interpol) #itp of msat type. env is the environment
            time_3 = time.time()

            if(jeez==1):    # Program is incorrect
                # print "\n[RESULT] Program is incorrect.\n"
                print "\nVerification Failed.\n"
                verification_done = True
            else:
                time_4 = time.time()
                # if args.manual:
                    # hoare_automaton.floyd_hoare_with_breaks(env,alp,itp,input_file,iteration,args.hoare)
                # else:
                hoare_automaton.floyd_hoare(env,alp,itp,input_file,iteration,args.hoare)
                time_5 = time.time()
                res = automata_operations.cover_check(input_file, iteration) #this modifies input_file too, as input \ floyd_hoare
                time_6 = time.time()
                if res:
                    verification_done = True
                    print "\nVerification Successful.\n"
                        
            #slice_automaton(input_file)   #Do we need this?
        if args.time:
            print "[TIME] Generating traces took       : "+ str(time_1 - time_0)+" sec"
            print "[TIME] Generating interpolants took : "+ str(time_3 - time_2)+" sec"
            print "[TIME] Creating Floyd Hoare took    : "+ str(time_5 - time_4)+" sec"
            print "[TIME] checking Automata Inclusion  : "+ str(time_6 - time_5)+" sec"
            print "[TIME] Automata Library took total  : "+ str(time_6 - time_5 + time_1 - time_0)+" sec"
            lib_automata_time += time_6 - time_5 + time_1 - time_0
            print "[TIME] MathSAT took total           : "+ str(time_5 - time_4 + time_3 - time_2)+" sec"
            mathsat_time += time_5 - time_4 + time_3 - time_2
        
        if args.pause:
            raw_input('\n\nPress enter to continue: ')
    if args.time:
        print "\n\n[TIME] Automata Library took finally : "+ str(lib_automata_time)+" sec"
        print "[TIME] MathSAT took finally          : "+ str(mathsat_time)+" sec"



def running_options():

    parser = argparse.ArgumentParser(description='Verify Programs! Sorry, Program Automatons :(')

    parser.add_argument("-t", dest="time", action='store_true',
                        help="Show time required by different processes.")

    parser.add_argument('-i', dest='interpol', action='store_true',
                        help='Show the interpolants')

    parser.add_argument('-ht', dest='hoare', action='store_true',
                        help='Show the Hoare triple being checked')

    parser.add_argument('-s', dest='smart', action='store_true',
                        help='Use smart hoare triple checking procedure')

    parser.add_argument('-p', dest='pause', action='store_true',
                        help='Pause program after each iteration')

    parser.add_argument('-m', dest='manual', action='store_true',
                        help='Use manual invariant addition')
    parser.add_argument('filename', 
                        help='.ats Filename')

    args = parser.parse_args()
    
    return args

args = running_options()
runner(args) 