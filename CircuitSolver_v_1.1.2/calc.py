import numpy as np

from circuit import Wire, Knot, Branch, Resistor, VoltageGenerator, Circuit

    
def add_sth(element: int, element2: int) -> int:
    return element + element2


def change_list(list: list, item) -> list:
    return list[list.index(item):] + list[ : list.index(item)]



#   --------    NOWA FUNKCJA


def nodal_analysis_2(cirucit: Circuit) -> dict:     #   zwroci dicta z pradem dla kazdej galezi
    ...


#   -----   ponizej stara funkcja, zamienic na nowa wykorzystujaca klase Circuit ^

def nodal_analysis(knots: list[Knot], wires: list[Wire]) -> None:

    branches = Branch.branches

    ground = knots[1] #max(knots, key=lambda knot: len(knot.links))

    print(knots.index(ground))


    equations = []

    currents = []

    potentials_data = {}
    for knot in knots:

        if knot != ground:
            potentials_data.update({knot : {}})     #   DO ZAPISU WYNIKU KONCOWEGO   

        print(f"DLA KNOTA {knot.id}: ")
        for wire in knot.cojoined_wires:
            new_branch = Branch(wire)

            print(new_branch.head.id)
            print(new_branch.tail.prev.id)
            print((new_branch.tail.links[0].id, new_branch.tail.links[1].id))
            print(new_branch.tail.next)

            while new_branch.tail not in knots:
                for x in new_branch.tail.links:
                    if isinstance(new_branch.tail, Knot):
                        if x not in new_branch.tail.prevs.items():
                            
                            print(new_branch.tail.id + f"    {new_branch.tail.next}")
                            x.prevs.update({new_branch : new_branch.tail})
                            new_branch.tail.next = x

                    else:
                        if isinstance(x, Knot):
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
                    if isinstance(node, Knot):
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


    for knot in knots:

        if knot != ground:

            values = {}
            
            potential_dict = {knot.id : {"res": 0, "current" : 0, "potential" : 0}}

            for potential in potentials_data.keys():

                if potential != knot:
                    potential_dict[knot.id].update({potential.id + "_resistance" : 0})
                    print(potential_dict)

            for branch in branches:

                if knot in branch.knots:

                    potential_dict[knot.id].update({branch.id : {"volts" : 0, "res" : 0, "current" : 0}})

                    print (f"KNOT: {knot.id},  BRANCH: {branch.id}")

                    for element in branch.links:

                        if isinstance(element, Resistor):
                            
                            potential_dict[knot.id]["res"] += 1/element.resistance
                            potential_dict[knot.id][branch.id]["res"] += element.resistance

                            for potential in potentials_data.keys():

                                if potential in branch.links and potential != knot:
                                    potential_dict[knot.id][potential.id + "_resistance"] += 1/element.resistance

                        if isinstance(element, VoltageGenerator):

                            direction_check = element.dir


                            if branch.links.index(direction_check) > branch.links.index(element):
                                direction_check = branch.tail
                                if knot != direction_check:
                                    potential_dict[knot.id][branch.id]["volts"] += element.voltage
                            
                                else:
                                    potential_dict[knot.id][branch.id]["volts"] -= element.voltage
                            
                            else:
                                direction_check = branch.head
                                if knot == direction_check:
                                    potential_dict[knot.id][branch.id]["volts"] += element.voltage
                            
                                else:
                                    potential_dict[knot.id][branch.id]["volts"] -= element.voltage

                try:
                    potential_dict[knot.id][branch.id]["current"] += potential_dict[knot.id][branch.id]["volts"] / potential_dict[knot.id][branch.id]["res"]
                    potential_dict[knot.id]["current"] += potential_dict[knot.id][branch.id]["current"]
                except ZeroDivisionError:
                    pass
                except KeyError:
                    pass

                


            potential_dict[knot.id]["res"] = float("{:.3f}".format(potential_dict[knot.id]["res"]))



            sorted_potential_dict = sorted(potential_dict.items())

            potentials_data[knot] = sorted_potential_dict


            for potential in potentials_data.keys():

                if potential in knots:
                    if potential != knot:
                        values.update({potential.id : potential_dict[knot.id][potential.id + "_resistance"]*-1})
                    else:
                        values.update({potential.id : potential_dict[knot.id]["res"]})

            equation = []

            for x in values.keys():
                equation.append(values[x])

            equations.append(equation)
            currents.append(potential_dict[knot.id]["current"])

            print(f"DLA KNOTA {knot.id}:        {potentials_data[knot]} R \n")
        


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

    for knot in knots:

        if knot != ground:


            potential_index = list(potentials_data.keys()).index(knot)


            for x in range(0, 3):
                main_matrix[x][potential_index] = currents_matrix[x]
        
            """print(f"PO ZAMIANIE NR {potential_index}")
            print(main_matrix)"""


            potentials_data[knot][0][1]["potential"] = float("{:.3f}".format(np.linalg.det(main_matrix) / main_determinant))
            
            print(potentials_data[knot][0][1]["potential"])
            print("iok")



            for x in range(0, 3):
                main_matrix[x][potential_index] = equations[x][potential_index]




            for branch in branches:
                if branch not in branches_currents.keys():
                    try:
                        branches_currents.update({branch : potentials_data[knot][0][1][branch.id]})
                    except KeyError:
                        pass
            
    for branch in branches_currents.keys():

        print(branch.id)
        #potentials_data[knot][0][1]["potential"]
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
            if isinstance(element, Knot):
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

        while not isinstance(element, VoltageGenerator) and a < len(branch.links)-1:

            a += 1
            element = branch.links[a]

            """if isinstance(element, Knot):
                for x in element.nexts:
                    if x in branch.links and x.next == element:
                        print(element.id, x.id, x.next.id)
                        element = x
            else:
                print(element.id, element.next.id)
                element = element.next"""

        if isinstance(element, VoltageGenerator):
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

        