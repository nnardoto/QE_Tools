import os
from pyfiglet import Figlet

# Global variables to use here
ColumnSize = os.get_terminal_size(0)[0]

def ProgramTitle(text: str, author: str, mail: str, font = 'big'):
    f = Figlet(font=font)
    toPrint = f.renderText(text)
    
    box(toPrint, bottom = False)
    print(draw_row(['by']))
    print(draw_row([author]))
    print(draw_row([mail]))
    draw_line()
    

def box(text: str, width = ColumnSize, align = 'centered', top = True, bottom = True):
    """
    print text inside a box
    """
    
    # remove two characters of borders
    nwidth = width - 2
       
    # print top line
    if top: 
        draw_line(width)
        
    # split input text
    ListedText = text.split('\n')
    
    toPrintLines = []
    for lines in ListedText:
        nBlanckL = int((nwidth - len(lines))/2)
        nBlanckR = nBlanckL
        
        if((nwidth - len(lines))%2) > 0:
            nBlanckR += 1
        
        if align == 'centered':
            toPrintLines.append('|' + ' ' * nBlanckL + lines + ' ' * nBlanckR + '|')
        elif align == 'left':
            toPrintLines.append('|' + lines + ' ' * (nBlanckL + nBlanckR) + '|')
    
    for lines in toPrintLines:
        print(lines)
        
    # print bottom line
    if bottom:
        draw_line(width)
        
        
def draw_row(line: list, width = ColumnSize):
    sizes = calcdiv(width, len(line))
    
    for i in range (len(line)):
        line[i] = line[i].center(sizes[i])

    LineOut = '|'
    for columns in line:
        LineOut += columns + '|'
        
    return LineOut

    
def calcdiv(width: int, div: int) -> list:
    width -= div + 1

    real_size = []
    for column in range(div):
        real_size.append(int(width / div))

    for i in range(width % div):
        real_size[i] += 1
        
    return real_size
    
    
def draw_line(width = ColumnSize, div = 1):
    sizes = calcdiv(width, div)
   
    Line = '+'
    for i in range (div):
        Line += '-' * sizes[i] + '+'
    
    print(Line)


