import calc

from gui import *

from circuit import Node, Wire, Knot, Branch, Resistor, VoltageGenerator




def main() -> None:

    resistor_1 = Resistor('R1')
    resistor_2 = Resistor('R2')
    resistor_3 = Resistor('R3')
    resistor_4 = Resistor('R4')
    resistor_5 = Resistor('R5')
    resistor_6 = Resistor('R6')
    """resistor_7 = Resistor('R7')
    resistor_8 = Resistor('R8')"""
    voltage_gen_1 = VoltageGenerator('V1')
    voltage_gen_2 = VoltageGenerator('V2', 10)



    resistor_1.join(resistor_2)
    resistor_2.join(resistor_3)


    resistor_3.join(voltage_gen_2)
    voltage_gen_2.join(resistor_4)
    voltage_gen_2.set_direction(resistor_3)
    resistor_4.join(voltage_gen_1)
    voltage_gen_1.join(resistor_1)
    voltage_gen_1.set_direction(resistor_1)


    print("przewody: ")
    for x in Wire.wires:
        print(x.id)

    print("tworzenie knotów: ")
    for current_branch in Wire.wires:
        if resistor_1 in current_branch.links and resistor_2 in current_branch.links:
            print(current_branch.links)
            resistor_5.tie_to_wire(current_branch)
        if resistor_2 in current_branch.links and resistor_3 in current_branch.links:
            print(current_branch.links)
            resistor_6.tie_to_wire(current_branch)
        if resistor_4 in current_branch.links and voltage_gen_1 in current_branch.links:
            print(current_branch.links)
            resistor_5.tie_to_wire(current_branch)
        if resistor_4 in current_branch.links and voltage_gen_2 in current_branch.links:
            print(current_branch.links)
            resistor_6.tie_to_wire(current_branch)

            

    print("Utworzone node'y:")
    for node in Node.nodes:
        print(node.id)

    print("Linki kolejnych rezystorow:")
    print(resistor_1.links)
    print(resistor_2.links)
    print(resistor_3.links)
    print(resistor_4.links)
    print(resistor_5.links)


    print("Wezly:")
    for knot in Knot.knots:
        print(knot.id)
        print("Ten wezel wiaze ze soba: ")
        for x in knot.cojoined_wires:
            print(x.id)

    print("rezystory:")
    for x in Resistor.resistors:
        print(x.id + ",  " + str(x.resistance) + " Ohm")

    print("Zrodla:")
    for x in VoltageGenerator.generators:
        print(x.id + ",  " + str(x.voltage) + " V")


    print(f"\nLINKI ELEMENTU {voltage_gen_2.id}:        {voltage_gen_2.links}\n")

    calc.nodal_analysis(Knot.knots, Wire.wires)
    
    #App_Class().play()



if __name__ == "__main__":
    main()