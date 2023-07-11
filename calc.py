import numpy as np

from circuit import *
from copy import deepcopy

    
def add_sth(element: int, element2: int) -> int:
    return element + element2


def change_list(list: list, item) -> list:
    return list[list.index(item):] + list[ : list.index(item)]




#   -----   ponizej stara funkcja, zamienic na nowa wykorzystujaca klase Circuit ^

def nodal_analysis_2(Nodes: list[Node] = Node.nodes, branches: list[Branch] = Branch.branches) -> None:

    branches = Branch.branches

    ground = Nodes[1] #max(Nodes, key=lambda Node: len(Node.links))

    print(Nodes.index(ground))


    equations = []

    currents = []

    potentials_data = {}
    for Node in Nodes:

        if Node != ground:
            potentials_data.update({Node : {}})     #   DO ZAPISU WYNIKU KONCOWEGO   

        print(f"DLA NODE'A {Node.id}: ")
        for wire in Node.cojoined_wires:
            new_branch = Branch(wire)

            print(new_branch.head.id)
            print(new_branch.tail.prev.id)
            print((new_branch.tail.links[0].id, new_branch.tail.links[1].id))
            print(new_branch.tail.next)

            while new_branch.tail not in Nodes:
                for x in new_branch.tail.links:
                    if isinstance(new_branch.tail, Node):
                        if x not in new_branch.tail.prevs.items():
                            
                            print(new_branch.tail.id + f"    {new_branch.tail.next}")
                            x.prevs.update({new_branch : new_branch.tail})
                            new_branch.tail.next = x

                    else:
                        if isinstance(x, Node):
                            if x is not new_branch.tail.prev:
                                x.prev = new_branch.tail
                                new_branch.tail.next = x

                    new_branch.add_to_tail(x)
                        #print(f"NOWY TAIL:       {new_branch.tail.prev.id}")
            
            print(new_branch.tail.id)

            print(new_branch.id + ",        poczatek w:     " + new_branch.head.id + ",        koniec w:     " + new_branch.tail.id)

            new_branch.links.sort(key=id)

            already_exists = False

            for branch in branches:
                if new_branch.links == branch.links:
                    already_exists = True
            
            if not already_exists:
                branches.append(new_branch)


                #
                #   TEST NASTEPUJACYCH PO SOBIE ELEMENTOW W GALEZI
                #   
                print("                 KOLEJNA NOWA GALAZ")

                for a in new_branch.links:
                    print(a.id)

                print("\n\n")

                node = new_branch.head

                while node != new_branch.tail:
                    if isinstance(node, Node):
                        for x in node.nexts.items():
                            if x[1] in new_branch.links:
                                print(node.id, x[1].id)
                                node = x[1]
                    else:
                        print(node.id, node.next.id)
                        node = node.next




                print("                 KONIEC NOWEJ GALEZI")

            

    print(f"\n\nILE GALEZI?: {len(branches)}")
    for branch in branches:
        elements = ""
        for x in branch.links:
            elements += x.id + "    "

        print(branch.id + f", która łączy elementy: {elements}")

    print("METODA WEZLOWA - OBLICZANIE")

    
    print(ground.id + "   ma potencjal rowny   0 V \n\n")


    for Node in Nodes:

        if Node != ground:

            values = {}
            
            potential_dict = {Node.id : {"res": 0, "current" : 0, "potential" : 0}}

            for potential in potentials_data.keys():

                if potential != Node:
                    potential_dict[Node.id].update({potential.id + "_resistance" : 0})
                    print(potential_dict)

            for branch in branches:

                if Node in branch.Nodes:

                    potential_dict[Node.id].update({branch.id : {"volts" : 0, "res" : 0, "current" : 0}})

                    print (f"Node: {Node.id},  BRANCH: {branch.id}")

                    for element in branch.links:

                        if isinstance(element, Resistor):
                            
                            potential_dict[Node.id]["res"] += 1/element.resistance
                            potential_dict[Node.id][branch.id]["res"] += element.resistance

                            for potential in potentials_data.keys():

                                if potential in branch.links and potential != Node:
                                    potential_dict[Node.id][potential.id + "_resistance"] += 1/element.resistance

                        if isinstance(element, PowerSupply):

                            direction_check = element.dir


                            if branch.links.index(direction_check) > branch.links.index(element):
                                direction_check = branch.tail
                                if Node != direction_check:
                                    potential_dict[Node.id][branch.id]["volts"] += element.voltage
                            
                                else:
                                    potential_dict[Node.id][branch.id]["volts"] -= element.voltage
                            
                            else:
                                direction_check = branch.head
                                if Node == direction_check:
                                    potential_dict[Node.id][branch.id]["volts"] += element.voltage
                            
                                else:
                                    potential_dict[Node.id][branch.id]["volts"] -= element.voltage

                try:
                    potential_dict[Node.id][branch.id]["current"] += potential_dict[Node.id][branch.id]["volts"] / potential_dict[Node.id][branch.id]["res"]
                    potential_dict[Node.id]["current"] += potential_dict[Node.id][branch.id]["current"]
                except ZeroDivisionError:
                    pass
                except KeyError:
                    pass

                


            potential_dict[Node.id]["res"] = float("{:.3f}".format(potential_dict[Node.id]["res"]))



            sorted_potential_dict = sorted(potential_dict.items())

            potentials_data[Node] = sorted_potential_dict


            for potential in potentials_data.keys():

                if potential in Nodes:
                    if potential != Node:
                        values.update({potential.id : potential_dict[Node.id][potential.id + "_resistance"]*-1})
                    else:
                        values.update({potential.id : potential_dict[Node.id]["res"]})

            equation = []

            for x in values.keys():
                equation.append(values[x])

            equations.append(equation)
            currents.append(potential_dict[Node.id]["current"])

            print(f"DLA NodeA {Node.id}:        {potentials_data[Node]} R \n")
        


    print(equations)

    main_matrix = np.array(equations)
    currents_matrix = np.array(currents).reshape(len(potentials_data.keys()), 1)

    print("\n\n")
    print(currents_matrix)

    print("\n\n")
    print(main_matrix)

    print("\n\n")
    print(main_matrix)


    main_determinant = float("{:.3f}".format(np.linalg.det(main_matrix)))
    print(main_determinant)



    branches_currents = {}

    for Node in Nodes:

        if Node != ground:


            potential_index = list(potentials_data.keys()).index(Node)


            for x in range(0, 3):
                main_matrix[x][potential_index] = currents_matrix[x]
        
            """print(f"PO ZAMIANIE NR {potential_index}")
            print(main_matrix)"""


            potentials_data[Node][0][1]["potential"] = float("{:.3f}".format(np.linalg.det(main_matrix) / main_determinant))
            
            print(potentials_data[Node][0][1]["potential"])
            print("iok")



            for x in range(0, 3):
                main_matrix[x][potential_index] = equations[x][potential_index]




            for branch in branches:
                if branch not in branches_currents.keys():
                    try:
                        branches_currents.update({branch : potentials_data[Node][0][1][branch.id]})
                    except KeyError:
                        pass
            
    for branch in branches_currents.keys():

        print(branch.id)
        #potentials_data[Node][0][1]["potential"]
        if branch.tail == ground:
            voltage_b = 0
        else:
            voltage_b = potentials_data[branch.tail][0][1]["potential"]

        if branch.head == ground:
            voltage_a = 0
        else:
            voltage_a = potentials_data[branch.head][0][1]["potential"]
        
        
        #   OKRESLENIE KIERUNKU ZASILANIA WZGLEDEM GALAZKI, TO TEZ WAZNE!!

        """print(element.id)

        for a in range(0, len(branch.links)):
            if isinstance(element, Node):
                for x in element.nexts.items():
                    if x[1] in branch.links:
                        print(x[1].id)
                        element = x[1]
                
            else:
                element = element.next
                print(element.id)"""

        #   BUUG MOZE BYC TUTAJ
        a = 0
        element = branch.links[a]

        while not isinstance(element, PowerSupply) and a < len(branch.links)-1:

            a += 1
            element = branch.links[a]

            """if isinstance(element, Node):
                for x in element.nexts:
                    if x in branch.links and x.next == element:
                        print(element.id, x.id, x.next.id)
                        element = x
            else:
                print(element.id, element.next.id)
                element = element.next"""

        if isinstance(element, PowerSupply):
            print(element.links[0].id, element.links[1].id)
            print(element.next.id)
            print(element.dir.id)

        try:
            if element.dir == element.next:
                charging_voltage = branches_currents[branch]["volts"]
            else:
                charging_voltage = branches_currents[branch]["volts"] * -1
        except AttributeError:
            charging_voltage = branches_currents[branch]["volts"]

        branch_resistance = branches_currents[branch]["res"]

        branches_currents[branch]["current"] = float("{:.4f}".format((voltage_a - voltage_b + charging_voltage)/branch_resistance))
        
        print(branch.id + "   -  " + str(branches_currents[branch]["current"]) + " A")

        






def nodal_analysis(branches: list[Branch], Nodes: list[Node] = Node.nodes)  -> dict:     #   zwroci dicta z pradem dla kazdej galezi

    ground = Nodes[1] #max(Nodes, key=lambda Node: len(Node.links))

    nodes_without_ground = []

    for node in Nodes:
        if node is not ground:
            nodes_without_ground.append(node)

    print(Nodes.index(ground))

    branches_info = {}

    for branch in branches:
        branches_info.update({branch : {"voltage" : 0.0, "resistance" : 0.0, "current" : 0.0,
                                        "end_potential" : 0, "start_potential" : 0}})


    equations = []

    currents = []

    potentials_data = {}

    #   WSTEPNY DICT DO OBSLUGI WEZLOW

    for node in Nodes:
        potentials_data.update({node : {"conductance" : 0.0, "voltage" : 0.0, "current" : 0.0}})     #   DO ZAPISU WYNIKU KONCOWEGO 
        for other_node in Nodes:
            if other_node is not node:
                potentials_data[node].update({other_node : 0.0})


    print(f"{len(branches)}")

    for branch in branches:

        resistance = 0.0

        branch_with_supply = False

        print(f"{branch.elements}")
        print(f"{branch.head},   {branch.tail}")
        print(f"{branch.head.id},   {branch.tail.id}")

        for element in branch.elements:
            if isinstance(element, Resistor):
                resistance += element.resistance
            if isinstance(element, PowerSupply):
                potentials_data[branch.head]["voltage"] += element.voltage
                potentials_data[branch.tail]["voltage"] -= element.voltage
                branches_info[branch]["voltage"] += element.voltage
                branch_with_supply = True

        if branch_with_supply:
            try:
                potentials_data[branch.head]["current"] += potentials_data[branch.head]["voltage"]/resistance
                potentials_data[branch.tail]["current"] += potentials_data[branch.tail]["voltage"]/resistance
            except ZeroDivisionError:
                potentials_data[branch.head]["current"] += potentials_data[branch.head]["voltage"]
                potentials_data[branch.tail]["current"] += potentials_data[branch.tail]["voltage"]

        branches_info[branch]["resistance"] += resistance
        potentials_data[branch.head]["conductance"] += 1/resistance
        potentials_data[branch.head][branch.tail] += 1/resistance

        potentials_data[branch.tail]["conductance"] += 1/resistance
        potentials_data[branch.tail][branch.head] += 1/resistance

    for x in list(potentials_data.keys()):
        print(f"{x.id} --------> {potentials_data[x]['conductance']} Ohm,   {potentials_data[x]['voltage']} V,   {potentials_data[x]['current']} A")
        if x is not ground:
            equation = []
            for y in list(potentials_data[x].keys()):
                if isinstance(y, Node) and y is not ground:
                    print(f"-----------> {y.id} --------> {potentials_data[x][y]}")

                    try:
                        equation.append(-potentials_data[x][y])
                    except ZeroDivisionError:
                        equation.append(0)

            equation.insert(nodes_without_ground.index(x), potentials_data[x]['conductance'])

            equations.append(equation)

            currents.append(potentials_data[x]['current'])


    print(equations)
    print(currents)

    main_matrix = np.array(equations)
    main_determinant = np.linalg.det(main_matrix)

    minor_matrixes = []
    minor_determinants = []

    potentials = {}

    for node in Nodes:
        if node is not ground:
            potentials.update({node : None})

    for x in range (0, len(currents)):
        minor_matrix = deepcopy(equations)
        print(minor_matrix)
        for y in range (0, len(currents)):
            minor_matrix[y][x] = currents[y]

            print(f"{y},      {len(currents)},         {minor_matrix}")

        minor_matrix = np.array(minor_matrix)
        minor_matrixes.append(minor_matrix)
        minor_determinants.append(np.linalg.det(minor_matrix))

    print(f"WYZNACZNIK GLOWNY: {main_determinant}")

    print("MACIERZE POSZCZEGOLNE:")
    for x in list(potentials.keys()):
        print(minor_matrixes[list(potentials.keys()).index(x)])
        print(f"WYZNACZNIK MACIERZY WYZEJ: {minor_determinants[list(potentials.keys()).index(x)]}")

        potentials[x] = minor_determinants[list(potentials.keys()).index(x)]/main_determinant

    print("POTENCJALY:")
    for x in list(potentials.keys()):
        print(f"{x.id} --------> {potentials[x]}")


    for branch in branches:
        for x in list(potentials.keys()):
            if branch.head == x:
                branches_info[branch]["start_potential"] = potentials[x]
            if branch.tail == x:
                branches_info[branch]["end_potential"] = potentials[x]

        branch_voltage = branches_info[branch]["start_potential"] - branches_info[branch]["end_potential"]

        branches_info[branch]["current"] = float("{:.3f}".format((-branches_info[branch]["voltage"] + branch_voltage)/branches_info[branch]["resistance"]))
        
        branch_id = ""

        for x in branch.elements:
            branch_id += x.id
            branch_id += "-"

        print(f"{branch_id} -----> {branches_info[branch]['current']} A,      {branch_voltage} V")



        
def Kirchhoffs_laws_method() -> None:
    # n wezlow, b galezi, -> n-1 rownan pradowych + b-n+1 rownan napieciowych
    ...


