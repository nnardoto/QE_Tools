from errno import EMLINK
import pandas as pd
import os
import TerminalTools as ptt
import pBandsQuestions as pbq


def read_states(setup: dict) -> pd.DataFrame:
    """
    Converte a parte relevante do arquivo pdos.out
    em um formato adquado para uso com PANDAS
    """
    toRemove = ['state #', ':', 'atom', '(', ')', ',', 'wfc', 'm_j=', 'j=', 'm=', 'l=']
    with open(setup['pdos_file']) as File:
        StatesLines = []
        for line in File:
            # append to DataFrame
            if line.find("state #") > 0:
                StatesLines.append(clear_str(line, toRemove, ' ').split())

            # exit condiction
            elif line.find("k =") > 0:
                break


    # convert to DataFrame
    DataFrame = pd.DataFrame(StatesLines)

    # correctly to nome columns
    if len(DataFrame.columns) == 7:
        DataFrame.columns = ['state', 'atom_n', 'atom_s', 'wfc', 'l', 'j', 'm_j']

    elif len(DataFrame.columns) == 6:
        DataFrame.columns = ['state', 'atom_n', 'atom_s', 'wfc', 'l', 'm']

    # rename orbitals
    DataFrame['l'] = DataFrame['l'].apply(OrbitalName)

    return DataFrame


def clear_str(rawString: str, toRemove: list, toReplace: str)  -> str:
    """
    remove da string inserida um lista de itens
    """

    # fisrt remove list
    for itens in toRemove:
       rawString = rawString.replace(itens, toReplace)

    return rawString


def OrbitalName(l):
    orbitals = ['s', 'p', 'd', 'f']
    return orbitals[int(l)]


def loadSetup(SetupFile: str) -> dict:
    """
    Carrega informações do arquivo setup
    """
    with open(SetupFile) as File:
        SetupFileText = File.readlines()

    # path of current work
    SetupDict = {}
    #SetupDict['local_path'] = os.path.abspath(SetupFile)[:-len(SetupFile)]

    for Element in SetupFileText:
        # split lines
        try:
            if Element[0] not in ['#', ' ', '\n']:
                Element = Element.replace('=', ' ').split()
                SetupDict[Element[0].lower()] = Element[1]

        except IndexError:
            print ("--> There are variable not seted")
            exit()


    # create a work_path variable from SETUP or default
    try:
        if not SetupDict['work_path'].endswith('/'):
            SetupDict['work_path'] += '/'

    except:
        SetupDict['work_path'] = 'work/'


    # create a input_path variable from SETUP or default
    try:
        if not SetupDict['input_path'].endswith('/'):
            SetupDict['input_path'] += '/'

    except:
        SetupDict['input_path'] = 'inputs/'


    # estabelece os nomes dos arquivos de forma correta no setup
    for name_list in SetupDict:
        if name_list.find('file') > 0:
            SetupDict[name_list] = SetupDict['input_path'] + SetupDict[name_list]


    # create WORK File
    WORK = open('WORK', 'w')
    WORK.write(SetupDict['work_path'])
    WORK.close()

    return SetupDict


def AtomFilter(states: pd.DataFrame, filter_list: list, mode = 'all') -> dict:
    """
    filter raw states using filter_list and mode
    """

    # store return value
    Filtered = {}
    if filter_list[0] == 'all':
        Filtered['all'] = states
        return Filtered

    for selection in states:
        # in case of all merge all results
        if mode == 'all':
            name = ''
            for elements in filter_list:
                name += elements + '_'

            Filtered[name[:-1]] = states[selection][states[selection].atom_n.isin(filter_list) | states[selection].atom_s.isin(filter_list)]
            return Filtered


        # Convert input in atom_n
        for item in filter_list:
            if item.isnumeric():
                Filtered[item] = states[selection][states[selection].atom_n == item]
            else:
                Filtered[item] = states[selection][states[selection].atom_s == item]

        # return dict of results
        return Filtered


def OrbitalFilter(states: dict, filter_list: list, mode = 'all') -> dict:
    """
    filter states by orbital name using filter_list and mode
    """
    # store return value
    Filtered = {}

    # in case of all merge all results
    if mode == 'all':
        for selection in states:
            orbitals = []
            for l in states[selection].l.unique():
                if l in filter_list:
                    orbitals.append(l)

            name = '_'
            for elements in orbitals:
                name += elements

            Filtered[selection + name] = states[selection][states[selection].l.isin(filter_list)]

        return Filtered


    # Convert input in atom_n
    for selection in states:
        orbitals = []
        for l in states[selection].l.unique():
            if l in filter_list:
                orbitals.append(l)

        for item in orbitals:
            Filtered[selection + '_' + item] = states[selection][states[selection].l == item]

    # return dict of results
    return Filtered


def JFilter(states: dict, filter_list: list, mode = 'all') -> dict:
    """
    filter states by j value using filter_list and mode
    """
    # store return value
    Filtered = {}

    # in case of all merge all results
    if mode == 'all':
        for selection in states:
            J_list = []
            for j in states[selection].j.unique():
                if j in filter_list:
                    J_list.append(j)

            name = '_'
            for elements in J_list:
                name += elements + '_'

            Filtered[selection + name[:-1]] = states[selection][states[selection].j.isin(filter_list)]

        return Filtered


    # Convert input in atom_n
    for selection in states:
        J_list = []
        for j in states[selection].j.unique():
            if j in filter_list:
                J_list.append(j)

        for item in J_list:
            Filtered[selection + '_' + item] = states[selection][states[selection].j == item]

    # return dict of results
    return Filtered


def FilterStep(states: dict, name: str, list_f, get_f, filter_f) -> dict:
    ptt.box("{} Selection".format(name))
    filter_list = list_f(get_f(states))

    step_mode = 'all'
    if len(filter_list) > 1:
        step_mode = pbq.EachAll(name)

    return filter_f(states, filter_list, mode = step_mode)

def panorama(states: pd.DataFrame):
    """
    show panorama of states table
    """

    species = states.atom_s.unique()
    orbitals = {}
    for atom in species:
        orbitals[atom] = states[states.atom_s == atom].l.unique()

    ptt.draw_line()
    print(ptt.draw_row(['Orbitals for each atom specie']))
    ptt.draw_line(div = 2)
    print(ptt.draw_row(['Atoms Species', 'Orbitals']))
    ptt.draw_line(div = 2)


    for itens in orbitals:
        print(ptt.draw_row([itens, ' '.join(orbitals[itens])]))


    ptt.draw_line(div = 2)

def getOrbitals(states: dict):
    raw_orbital_list = {}
    for itens in states:
        raw_orbital_list[itens] = states[itens].l.unique()

    sizes = []
    for itens in raw_orbital_list:
        sizes.append(len(raw_orbital_list[itens]))

    orbitals = ['s', 'p', 'd', 'f']

    return orbitals[:max(sizes)]


def getJ(states: dict):
    J_list = {}
    for itens in states:
        for J in states[itens].j.unique():
            J_list[J] = True

    out = []
    for itens in J_list:
        out.append(itens)

    return out


def getAtoms(states: dict):
    Atoms_list = {}

    for itens in states:
        for Atoms in states[itens].atom_s.unique():
            Atoms_list[Atoms] = True

    out = []
    for itens in Atoms_list:
        out.append(itens)

    return out

def getInput(text: str, filter_list: list, default = []):
    """
    return only if all inputs are in filter list
    """
    raw = []
    if len(default) == 0:
        raw = input(text).split()

    else:
        raw = input(text + ' [' + default + '] ').split()

    if len(raw) == 0 and len(default) == 0:
        return getInput(text, filter_list)

    elif len(raw) == 0:
        raw = [default]

    for elements in raw:
        if elements in filter_list:
            pass

        else:
            return getInput(text, filter_list)

    return raw


def FilterRoutines(states: pd.DataFrame) -> dict:
    ## Terminal Interface
    ptt.box("pre-selection mode")

    # pre selection question for atoms list   
    first_atom_list = pbq.ProgramMode(states.atom_n.unique())

    # make first filter 
    groups = AtomFilter(states, first_atom_list)

    # filter by atom
    groups = FilterStep(groups, 'Atoms', pbq.AtomListQ, getAtoms, AtomFilter)

    ### Filter For Orbitals
    groups = FilterStep(groups, 'Orbitals', pbq.OrbitalListQ, getOrbitals, OrbitalFilter)


    ### ONLY FOR SPIN ORBIT CASE ###
    key = list(groups.keys())[0]
    if len(groups[key].columns) == 7:
       groups = FilterStep(groups, 'J', pbq.JListQ, getJ, JFilter)

    return groups

def MakeProjBandInput(prefix: str, setup: dict, states: dict, fermi_energy: float):
    """
    create plotbands.x input file using a list of states and setup informations
    for each element in states dictionary
    """

    # cria o diretorio WORK
    try:
        os.makedirs(setup['work_path'], exist_ok=True)
    
    except:    
        print("Erro ao Criar o Diretório: " + setup['work_path'])
        exit()

    for itens in states:
        try:
            os.makedirs(setup['work_path'] + prefix + '/' + itens, exist_ok=True)
    
        except:    
            print("Erro ao Criar o Diretório: " + prefix + '/' + itens)
            exit()

        newFile = "{}{}/{}/{}.in".format(setup['work_path'], prefix, itens, itens)
        with open(newFile, 'w') as inFile:
            inFile.write('../../../' + setup['bands_file'] + '\n')
            inFile.write(' '.join(states[itens]["state"].to_list()) + '\n')
            inFile.write(setup['min_energy'] + ' ' + setup['max_energy'] + '\n')
            inFile.write(itens + '.dat\n')
            inFile.write(itens + '.ps\n')
            inFile.write(str(fermi_energy) + '\n')
            inFile.write(str(setup['de']) + ' ' + str(fermi_energy) + '\n')


def RunPlotBandsX(prefix: str, setup: dict, states: dict):
    """
    Roda cada arquivo gerado pela função MakeProjBandInput
    """
    
    # salva local atual
    local_path = os.getcwd()

    # define local completo do plotband.x
    plotbands = setup['path'] + '/plotband.x'
    os.chdir(setup['work_path'] + prefix + '/')

    # tenta rodar o plotband.x para cada aquivo gerado e listado no dicionario states
    for itens in states:
        os.chdir(itens)
              
        try:
            os.system("mpirun -n 1 {} < {} > log.out".format(plotbands, itens + '.in'))
            print("plotband.x: {}".format(itens))
        
        except:
            print("plotband.x erro: {}".format(itens))
        
        # Apaga Arquivos Extras (não sei o que significam)
        os.system("rm *.1* *.ps")
        os.chdir('..')
    
    # retorna para o diretorio inicial
    os.chdir(local_path)

    
def MakeGraphics_gnuplot(prefix: str, setup: dict, states: dict, fermi_energy: float):
    """
    Produz gráficos a partide de um modelo de script editavel
    """
    # salva local atual
    local_path = os.getcwd()

    # define local completo do plotband.x
    script_path = os.path.dirname(__file__)
    print(script_path)
    os.chdir(setup['work_path'] + prefix + '/')

    # tenta rodar o plotband.x para cada aquivo gerado e listado no dicionario states
    for itens in states:
        os.chdir(itens)
              
        try:
            emin = setup['min_energy']
            emax = setup['max_energy']
            filename = itens
            fermi = fermi_energy
            os.system("gnuplot -e \"emin={}; emax={}; filename='{}.dat'; fermi={}; outfile='{}.png'\" {}/MakePicture.gp".format(emin, emax, filename, fermi, filename, script_path))
            print("gnuplot: {}".format(itens))
        
        except:
            print("gnuplot erro: {}".format(itens))
        
        # Apaga Arquivos Extras (não sei o que significam)
        os.chdir('..')
    
    # retorna para o diretorio inicial
    os.chdir(local_path)

