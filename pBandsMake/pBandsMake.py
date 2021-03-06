#!/usr/bin/env python3
import pBandsTools as pbt
import pTerminalTools as ptt
import pBandsQuestions as pbq
import sys



# print a title of program

ptt.ProgramTitle('pBandsMake', 'pessoinha', 'pessoinha@mail.com')

# load input file from argv list without verification
if len(sys.argv) < 2:
	ptt.box(">>> ERROR: fisrt argument must be a SETUP file", align = 'left', top = False)
	exit()


# load setup file from project 	
setup = pbt.loadSetup(sys.argv[1])

# states of files in setup
states = pbt.read_states(setup)

# make panora of project
pbt.panorama(states)

states = pbt.FilterRoutines(states)


ptt.box("Your Selections")
for itens in states:
    print(itens)

