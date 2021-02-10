"""
Created on Thu Oct  1 19:49:55 2020

@author: Emilio Popovits Blake
@author: Roberto Gervacio 
@author: Carla Perez Gavilan
"""

from itertools import combinations
from os import listdir, path


def printTable(table, alphabet, states):
    alphabetString = 'State\t' + '\t'.join(alphabet)
    print(alphabetString)
    for line in enumerate(table):
        lineString = '\t'.join(line[1])
        print(states[line[0]] + '\t' + lineString)


def main():
    # Prompt user to select file with NFA and read it
    print('Files in ./NFAs/ directory:')
    fileArray = []
    count = 1
    for file in listdir('./NFAs'):
            if file.endswith('.txt'):
                    print(path.join(str(count) + '. ', file))
                    fileArray.append(file)
                    count += 1
    
    prompt = input('\nWhich file number which contains an NFA do you want converted into a DFA?: ')
    selectedFile = fileArray[int(prompt)-1]

    file = open('./NFAs/' + selectedFile)
    nfa = file.read()
    nfa = ''.join(nfa.split())

    print('\nRecieved NFA string:')
    print(nfa)

    # Trim nfa input string onto format: ["0,p,p", "0,p,q",...,"1,s,s"]
    nfa = nfa.replace('{', '').replace('}', '')
    nfa = nfa[1:len(nfa)-1]
    nfa = nfa.split('),(')
    print('Initial String as Array:')
    print(nfa)

    alphabet = set()
    states = set()
    
    # Get complete alphabet and states from nfa string
    for tupple in nfa:
        tupple = tupple.split(',')
        alphabet.add(tupple[0])
        states.add(tupple[1])
        states.add(tupple[2])
    
    alphabet = list(alphabet)
    states = list(states)

    alphabet.sort()
    states.sort()

    print('\nAlphabet:')
    print(alphabet)
    print('States:')
    print(states)

    # Make NFA delta table
    nfaTable = [ ['0' for i in range(0, len(alphabet)) ] for j in range(0, len(states)) ]
    for tupple in nfa:
        tupple = tupple.split(',')
        col = states.index(tupple[1])
        row = alphabet.index(tupple[0])
        
        nfaTable[col][row] = tupple[2] if nfaTable[col][row] == '0' else nfaTable[col][row] + "" + tupple[2]
    print('\nNFA Table')
    print('-----------')
    printTable(nfaTable, alphabet, states)
    # print(nfaTable)

    # Saves all possible combinations of states into array
    stateCombinations = []
    for i in range(1,len(states)+1):
      comb = combinations(states, i)
      stateCombinations += [''.join(i) for i in comb]
    stateCombinations.insert(0,'0')
    print('State Combinations:')
    print(stateCombinations)

    # Saves stateCombinations as indexes for usage in dfaTable
    stateCombinationsIndexes = []
    tmpStates = states.copy()
    tmpStates.insert(0,'0')
    for entry in stateCombinations:
        if len(entry) == 1:
            stateCombinationsIndexes.append([tmpStates.index(entry)])
        else:
            tmpArray = []
            i = 0
            while i < len(entry):
                tmpArray.append(tmpStates.index(entry[i]))
                i += 1
            stateCombinationsIndexes.append(tmpArray)
    print('State Combinations Indexes:')
    print(stateCombinationsIndexes)
            
    # Make DFA delta table
    dfaTable = []
    stringOutput = "{"
    for index, entry in enumerate(stateCombinationsIndexes):
        if len(entry) == 1:
            if entry[0] == 0:
                dfaTable.append(['0','0'])
            else:
                tmpArray = []
                for alIdx in enumerate(alphabet):
                    tmpArray.append(nfaTable[index-1][alIdx[0]])
                    stringOutput += "("
                    stringOutput += str(alIdx[0]) + "," + stateCombinations[index] + "," + nfaTable[index-1][alIdx[0]]
                    stringOutput += "),"
                dfaTable.append(tmpArray)
        else:
            tmpArray = []
            for alIdx in enumerate(alphabet):
                stringOutput += "("
                tmpSet = set()
                for enIndex in entry:
                    tmpSet.add(str(dfaTable[enIndex][alIdx[0]]))
                if len(tmpSet) > 1 and '0' in tmpSet:
                    tmpSet.remove('0')
                setStringList = [str(s) for s in tmpSet]
                setStringList.sort()
                setString = ''.join(setStringList)
                tmpArray.append(setString)
                stringOutput += str(alIdx[0]) + "," + stateCombinations[index] + "," + setString
                stringOutput += "),"
            dfaTable.append(tmpArray)

    stringOutput = stringOutput[:-1]
    stringOutput += "}"
    print('\nDFA Table')
    print('-----------')
    printTable(dfaTable, alphabet, stateCombinations)

    #Create dfa format
    finalFilePath = './DFAs/' + selectedFile.replace('.txt', '') + '-DFA.txt'
    finalFile = open(finalFilePath, "w+")
    finalFile.write(stringOutput)
    finalFile.close()

    print('\nOutput file was saved to ' + finalFilePath)

if __name__ == "__main__":
    main()