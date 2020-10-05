# -*- coding: utf-8 -*-
"""
Created on Fri May  1 19:26:37 2020

@author: Viviana Osorio Nieto A01374461
@author: Oscar Zuniga Lara A01654827
        
"""
from itertools import combinations


def readTXT(nombreArchivo):
    data = []
    file = open(nombreArchivo, 'r')
    lines = file.readlines()
    for line in lines:
        # quitar { }
        x = line.strip('{}')
        # Separar por()
        y = x.split('(')
        z = ''.join(y)
        m = z.split(')')
        blanc = '|'.join(m)
        node = blanc.split('|')
        for i in node:
            j = i.split(',')
            element = '|'.join(j)
            space = element.strip('|')
            array = space.split('|')
            data.append(array)
    data.pop(-1)
    return data


# Regresa todas las combinaciones de estados posibles.
def generateStates(data):
    states = []
    newStates = []
    # añade los estados.
    for node in data:
        states.append(node[1])
    # elimina los repetidos
    uniqueStates = set(states)
    # Todas las combinaciones de estados.
    for i in range(1, len(uniqueStates) + 1):
        comb = combinations(uniqueStates, i)
        for i in list(comb):
            newStates.append(i)
    return newStates


def newTansitionsStates(data):
    inp, state = '', ''
    newState = []
    for node in data:
        inp, state = node[0], node[1]
        for i in data:
            if str(i[0]) == inp and str(i[1]) == state:  # Si la entrada es la misma y el estado es el mismo
                estado1 = i[2]
                estado2 = node[2]
                if i[2] != node[2]:
                    transtate = [estado1, estado2]
                    newNode = [inp, state, transtate]
                    newState.append(newNode)
                    data.remove(i)
    # elimina estados repetidos
    for j in range(len(newState)):
        for node in newState:
            inp, state = node[0], node[1]
            for i in data:
                if str(i[0]) == inp and str(i[1]) == state:
                    data.remove(i)

    # juntar todo. Ay prof si ve esto perdoon. No es mucho pero es trabajo honesto
    for i in data:
        newState.append(i)
    return newState


def newTransition(states, transitionStates):
    DFA = []
    issue = []
    for state in states:
        for transition in transitionStates:
            if ''.join(transition[1]) == ''.join(state):
                # print(transition , state)
                DFA.append(transition)

    # Hacer diccionario de transisciones 0 y 1
    dic0 = {}
    dic1 = {}
    for state in DFA:
        stat = state[1]
        new = state[2]
        if state[0] == '0':
            dic0.update({stat: new})
        else:
            dic1.update({stat: new})

    # estados para nueva transicion
    for state in states:
        # print(state, len(state))
        if len(state) <= 1:
            continue
        else:
            issue.append(state)

    # generate 0

    for states in issue:
        Allstates = []
        for state in states:
            if state in dic1:
                # print(dic1.get(state))
                Allstates.append(dic0.get(state))

        together = ''.join(str(Allstates))
        l = together.strip('[]')
        clean = []
        for m in l:
            x = m.strip('[]')
            y = ','.join(x)
            p = y.strip('\'')
            b = ''.join(p).strip(' ')
            w = ''.join(b).strip(',')
            # print(w)
            if w != '':
                clean.append(w)
                # break
        uniqueClean = set(clean)
        tr = ['', '', '']
        tr[0] = '0'
        tr[1] = states
        tr[2] = uniqueClean
        DFA.append(tr)

    # generate 1
    for states in issue:
        Allstates = []
        for state in states:
            if state in dic1:
                Allstates.append(dic1.get(state))

        together = ''.join(str(Allstates))
        l = together.strip('[]')
        clean = []
        for m in l:
            x = m.strip('[]')
            y = ','.join(x)
            p = y.strip('\'')
            b = ''.join(p).strip(' ')
            w = ''.join(b).strip(',')
            if w != '':
                clean.append(w)
                # break
        uniqueClean = set(clean)

        tr = ['', '', '']
        tr[0] = '1'
        tr[1] = states
        tr[2] = uniqueClean
        DFA.append(tr)

    return DFA

def exportarTxt(DFA,file):
    file = file + "DFA.txt"
    f = open(file, "w+")
    toFile = ("{")

    for n in DFA:
        toFile = toFile + "("
        for x in n:
            for h in x:
                toFile = toFile + str(h)
            toFile = toFile + ','
        toFile = toFile[:-1]
        toFile = toFile + ")"


    toFile = toFile + "}"
    # print(toFile)
    f.write(toFile)
    return 0

def main():
    file = input("INSERTE NOMBRE DEL ARCHIVO:   ")
    data = readTXT(file)
    newStates = generateStates(data)
    newTranStates = newTansitionsStates(data)
    DFA = newTransition(newStates, newTranStates)
    exportarTxt(DFA, file)


main()

