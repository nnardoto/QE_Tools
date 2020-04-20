import numpy as np


def get_parameters(cell_vectors: list) -> dict:
    parameters = {}
    
    v1 = np.array(cell_vectors[0])
    v2 = np.array(cell_vectors[1])
    v3 = np.array(cell_vectors[2])
    
    a = np.linalg.norm(cell_vectors[0])
    b = np.linalg.norm(cell_vectors[1])
    c = np.linalg.norm(cell_vectors[2])
    
    cosAB = v1.dot(v2)/(a*b)
    cosAC = v1.dot(v3)/(a*c)
    cosBC = v2.dot(v3)/(b*c)
    
    parameters['A'] = a
    parameters['B'] = b
    parameters['C'] = c
    parameters['cosAB'] = cosAB
    parameters['cosAC'] = cosAC
    parameters['cosBC'] = cosBC
    parameters['gamma'] = np.degrees(np.arccos(cosAB))
    parameters['beta'] = np.degrees(np.arccos(cosAC))
    parameters['alpha'] = np.degrees(np.arccos(cosBC))
    
    
    
    return parameters

def print_parameters(parameters: dict):
    for itens in parameters:
        print(str(itens) + '\t=\t' + str(parameters[itens]))


def get_vectors(parameters: dict) -> list:
    print('a')
    
    
def translate_atoms(AtomsList: list, direction: np.array) -> list:
    newList = []
    for atoms in AtomsList:
        newList.append([atoms[0], atoms[1] + direction])
            
    return newList
    
def get_atoms(atoms_file: str) -> list:
    with open(atoms_file) as File:
        CFile = File.readlines()

    SplittedLines = []
    for lines in CFile:
        SplittedLines.append(lines.split())
    
    for i in range(len(SplittedLines)):
        for j in range(1,4):
            SplittedLines[i][j] = float(SplittedLines[i][j])
        
    Atoms = []
    for lines in SplittedLines:
        Atoms.append([lines[0], lines[1:]])
        
    for i in range(len(Atoms)):
        Atoms[i] = [Atoms[i][0], np.array(Atoms[i][1])]

    return Atoms
