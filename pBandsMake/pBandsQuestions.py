import inquirer
import pBandsTools as pbt

def ProgramMode(atom_n: list):
    
    questions = [
      inquirer.List('Mode',
                    message="pre-selection mode?",
                    choices=['yes', 'no'],
                    default = 'no'
                ),
    ]
    
    answers = inquirer.prompt(questions)
    
    if answers['Mode'] == 'yes':
        return pbt.getInput("List of Atoms Numbers: ", atom_n)
        
    elif answers['Mode'] == 'no':
        return ['all']
        
    
def AtomListQ(atom_s: list):
    ListQ = []
    for itens in atom_s:
        ListQ.append(itens)
        
    question = [
        inquirer.Checkbox('AtomsSelection',
                message = "Select Atoms",
                choices = ListQ,
                default = ListQ)
    ]
    
    answers = inquirer.prompt(question)
    
    return answers['AtomsSelection']


def EachAll(kind: str):
    question = [
        inquirer.List('Mode',
            message="[Each] or [All] from {} selection?".format(kind),
            choices=['each', 'all'],
            default = 'all'
        ),
    ]
    
    return inquirer.prompt(question)['Mode']


def OrbitalListQ(orbitals: list):
    ListQ = []
    for itens in orbitals:
        ListQ.append(itens)    

    question = [
            inquirer.Checkbox('OrbitalSelection',
                    message = "Select Orbitals",
                    choices = ListQ,
                    default = ListQ)
        ]
        
    answers = inquirer.prompt(question)
    
    return answers['OrbitalSelection']

def JListQ(J: list):
    ListQ = []
    for itens in J:
        ListQ.append(itens)    

    question = [
            inquirer.Checkbox('JSelection',
                    message = "Select J",
                    choices = ListQ,
                    default = ListQ)
        ]
        
    answers = inquirer.prompt(question)
    
    return answers['JSelection']
