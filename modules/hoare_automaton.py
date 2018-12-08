from mathsat import *
from collections import OrderedDict
from library.valid_hoare_triple import is_valid_hoare_triple

def floyd_hoare(env,alpha,interpolants,ats_file,iter_c,verbose):

	new_ats_tr = []	#transition list in new floyd-hoare automaton

	interpolants = list(OrderedDict.fromkeys(interpolants))

	pre_state = interpolants[0]

	alphabet = []
	break_alph = []
	for item in alpha:
		if "break" not in item:
			alphabet.append(item)
		else:
			break_alph.append(item)

	alpha = alphabet

	for state_no, state in enumerate(interpolants):	#most "unsmart" way to get all hoare triples
		for letter in alpha:
			state_string=msat_to_smtlib2_term(env,state)
			pre_state_string=msat_to_smtlib2_term(env,pre_state)
			# print "[DEBUG] check hoare triple : {"+pre_state_string+"} "+letter+" {"+pre_state_string+"}"
			if is_valid_hoare_triple(env,state_string,letter,state_string,verbose):
				new_ats_tr.append("q"+str(state_no)+" \""+letter+"\" "+"q"+str(state_no))
			# print "[DEBUG] check hoare triple : {"+pre_state_string+"} "+letter+" {"+state_string+"}"			
			if is_valid_hoare_triple(env,pre_state_string,letter,state_string,verbose) and state_no > 0:
				new_ats_tr.append("q"+str(state_no-1)+" \""+letter+"\" "+"q"+str(state_no))	

		for letter in break_alph:
			new_ats_tr.append("q"+str(state_no)+" \""+letter+"\" "+"q"+str(state_no))
			# if state_no>0:
				# new_ats_tr.append("q"+str(state_no-1)+" \""+letter+"\" "+"q"+str(state_no))	


		pre_state = state


	alphabet = set(alpha+break_alph)

	new_ats =  open(ats_file, "a")

	new_ats.write("\nFiniteAutomaton fha_"+str(iter_c)+" = (\n")

	s = "     alphabet = {"
	for letter in alphabet:
		s = s + "\""+letter + "\" "
	s = s + "},\n"
	new_ats.write(s)

	s = "     states = {"

	for i in range (0,len(interpolants)):
		s = s + "q"+str(i) + " "
	s = s + "},\n"
	new_ats.write(s)

	new_ats.write("     initialStates = {q0},\n")
	new_ats.write("     finalStates = {q"+str(len(interpolants)-1)+"},\n")
	new_ats.write("     transitions = {\n")

	for transition in new_ats_tr:
		new_ats.write("         ("+transition+")\n")

	new_ats.write("     }\n")
	new_ats.write(");\n")
	# new_ats.write("print(getAcceptedWord(nfa1));")


# tr = ["x = 0", "y = 0", "x = x + 1", "x == (-1)"]

# floyd_hoare(tr,tr)
	












