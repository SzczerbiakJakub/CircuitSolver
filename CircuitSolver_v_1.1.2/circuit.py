import abc, calc

#   ----------------------  NOWE KLASY -------------------


class Element:

    elements = []
    
    def __init__(self) -> None:
        self.next = None
        self.prev = None
        Element.elements.append(self)

    def join_to(self, element) -> None:

        if len(Branch2.branches) == 0:
            Branch2.branches.append(Branch2(self, element))
            Circuit(Branch2.branches)

        elif isinstance(self, Wire2):
            Node2(self, element)

        elif isinstance(element, Wire2):
            Node2(element, self)

        else:
            for branch in Branch2.branches:
                if self in branch.elements:
                    branch.elements = branch.add_to_end(Wire2(self, element))
                    branch.elements = branch.add_to_end(element)


    def remove(self) -> None:
        try:
            self.prev.next = self.next
            self.next.prev = self.prev
        except ZeroDivisionError:       #tu wstaw errora z brakiem elementow
            ...




class Res(Element):

    def __init__(self, id, resistance: float = 10,) -> None:
        super().__init__()
        self.resistance = resistance

        self.id = id


    def set_resistance(self, resistance: float) -> float:
        return resistance



class PowerSuply(Element):

    def __init__(self, id, voltage: float = 10) -> None:
        super().__init__()
        self.voltage = voltage
        self.direction = None

        self.id = id


    def set_voltage(self, voltage: float) -> float:
        return voltage
    

    def set_direction(self, direction: Element) -> Element:
        return direction



class Wire2(Element):

    def __init__(self, element1: Element, element2: Element) -> None:

        self.prev = element1
        self.head = element1
        self.next = element2
        self.tail = element2

        self.links = [element1, element2]

        self.id = str(f"{element1.id}-{element2.id}")

        if isinstance(element1, Node2):
            element1.nexts.append(self)
            element2.prev = self

        elif isinstance(element2, Node2):
            element1.next = self
            element2.prevs.append(self)
        
        else:
            element1.next = self
            element2.prev = self


class Node2(Element):

    nodes = []

    def __init__(self, wire: Wire2, element: Element) -> None:

        self.nexts = []
        self.prevs = []
        
        self.links = [wire.head, element, wire.tail]

        self.id = str(f"{wire.head.id}x{element.id}x{wire.tail.id}")

        new_branch_2 = Branch2(self, element)

        element_in_branches = False

        print("NOWY KNOCIARZ")

        Node2.nodes.append(self)

        for branch in Branch2.branches:
            if wire in branch.elements:
    
                branch.elements.insert(branch.elements.index(wire), self)
                branch.elements.insert(branch.elements.index(self), Wire2(wire.head, self))
                branch.elements.insert(branch.elements.index(self) + 1, Wire2(self, wire.tail))

                branch.elements.remove(wire)

                new_branch = Branch2(self, wire.tail)

                if len(Node2.nodes) < 2:
                    print(len(branch.elements))
                    new_branch.elements = calc.change_list(branch.elements, self)
                    new_branch.tail = new_branch.elements[-1]
                    new_branch.head = new_branch.elements[0]
                    Branch2.branches.append(new_branch)
                    Branch2.branches.remove(branch)
                    print(len(branch.elements))

                else:
                    new_branch.elements = [x for x in branch.elements if branch.elements.index(x) >= branch.elements.index(self)]
                    new_branch.tail = new_branch.elements[-1]
                    Branch2.branches.append(new_branch)

                    """print(f"LISTA:   {branch.head.id} <->{branch.tail.id}")
                    for x in branch.elements:
                        print(x.id)"""

                    branch.elements = [x for x in branch.elements if branch.elements.index(x) <= branch.elements.index(self)]
                    branch.tail = branch.elements[-1]

            
            if element == branch.tail:
                branch.elements = branch.add_to_end(Wire2(element, self))
                branch.elements = branch.add_to_end(self)
                element_in_branches = True

            elif element == branch.head:
                branch.elements = branch.add_to_start(Wire2(self, element))
                branch.elements = branch.add_to_start(self)
                element_in_branches = True

        #new_branch.add_to_end(adding_element)

        if not element_in_branches:
            new_branch_2 = Branch2(self, element)
            Branch2.branches.append(new_branch_2)



        for branch in Branch2.branches:
            print(f"LISTA:   {branch.head.id} <->{branch.tail.id}")
            for x in branch.elements:
                print(x.id)



class Branch2:

    branches = []
    
    def __init__(self, element1: Element, element2: Element) -> None:
        new_wire = Wire2(element1, element2)
        self.elements = [element1, new_wire, element2]
        self.head = element1
        self.tail = element2

    def add_to_end(self, element: Element) -> list:
        if element in self.elements:
            Loop2.loops.append(Loop2(self))
            print("powstalo oczko")
            return self.elements
        else:
            self.elements.append(element)
            self.tail = element
            return self.elements

    def add_to_start(self, element: Element) -> list:
        if element in self.elements:
            Loop2.loops.append(Loop2(self))
            print("powstalo oczko")
            return self.elements
        else:
            self.elements.insert(0, element)
            self.head = element
            return self.elements


class Loop2:

    loops = []

    def __init__(self, loopedBranch: Branch2) -> None:
        self.loopedBranch = loopedBranch

class Circuit:
    
    def __init__(self, branches: list[Branch2]) -> None:
        self.branches = branches


    def compute(self, method) -> list:
        method(self.branches)   #   STOSUJE TE FUNKCJE I SE LICZY
        return self.branches


















#   ---------------------   STARE KLASY POD SPODEM  -------------------------

class Node:

    nodes = []
    links = []

    def __init__(self, id: str = "") -> None:
        self.id = id
        self.links = []
        self.next: Node = None
        self.prev: Node = None
        self.nodes.append(self)

class Wire(Node):

    wires = []


    def __init__(self, element_1: Node, element_2: Node) -> None:
        
        super().__init__()
        
        if isinstance(element_2, Knot):
            self.id = element_2.id + ":" + element_1.id
            self.head = element_2
            self.tail = element_1
            self.head.nexts.update({self : self.tail})
            self.tail.prev = self.head
        elif isinstance(element_1, Knot):
            self.id = element_1.id + ":" + element_2.id
            self.head = element_1
            self.tail = element_2
            self.head.nexts.update({self : self.tail})
            self.tail.prev = self.head
        elif element_1.id > element_2.id:
            self.id = element_2.id + ":" + element_1.id
            self.head = element_2
            self.tail = element_1
        else:
            self.id = element_1.id + ":" + element_2.id
            self.head = element_1
            self.tail = element_2

        self.links = [self.head, self.tail]

        """if isinstance(element_1, Knot):
            element_1.nexts.update({self : element_2})
        else:
            element_1.next = element_2
            
        if isinstance(element_2, Knot):
            element_2.prevs.update({self : element_1})
        else:
            element_2.prev = element_1"""

        #self.id = self.change_id(element_1, element_2)

    
    def change_id(self, element_1: Node, element_2: Node) -> None:
        if element_1.id > element_2.id:
            self.id = element_2.id + ":" + element_1.id
        else:
            self.id = element_1.id + ":" + element_2.id



class Knot(Node):

    knots = []

    def __init__(self, element: Node, wire: Wire) -> None:

        elements_ids = wire.id.split(':')
        elements_ids.append(element.id)
        elements_ids.sort()
        self.id =  str(elements_ids[0])
        for x in elements_ids[1:]:
            self.id += 'x' + str(x)


        self.added_element = element

        
        self.cojoined_wires = []
        self.nexts = {}
        self.prevs = {}

        new_wire = Wire(self, wire.links[0])
        self.cojoined_wires.append(new_wire)
        Wire.wires.append(new_wire)

        new_wire = Wire(self, element)
        self.cojoined_wires.append(new_wire)
        Wire.wires.append(new_wire)

        new_wire = Wire(self, wire.links[1])
        self.cojoined_wires.append(new_wire)
        Wire.wires.append(new_wire)
        


        self.connected_branches = []

        
        self.links = [wire.links[0], wire.links[1], element]

        wire.links[0].links.remove(wire.links[1])
        wire.links[0].links.append(self)

        wire.links[1].links.remove(wire.links[0])
        wire.links[1].links.append(self)

        element.links.append(self)

        
        Knot.knots.append(self)

        


    def add_to_knot(self, element: Node) -> None:
        new_wire = Wire(self, element)
        self.cojoined_wires.append(new_wire)
        self.links.append(element)
        self.links.sort(key=id)
        self.id =  self.links[0].id
        for x in self.links[1:]:
            self.id += 'x' + x.id

        element.links.append(self)

        Wire.wires.append(new_wire)


    
def return_knot_with_max_links(knots: list) -> Knot:

    knots_links_list = []

    for knot in knots:
        knots_links_list.append(len(knot.links))

    return knots[knots_links_list.index(max(knots_links_list))]
        



class Branch: 

    branches = []
    
    wires = []
    links = []
    
    def __init__(self, wire: Wire) -> None:
        
        self.head = wire.links[0]
        self.tail = wire.links[1]
        self.id = str(self.head.id) + '-' + str(self.tail.id)
        
        self.links = [self.head, self.tail]
        self.wires.append(wire)

        self.knots = []

        if isinstance(self.head, Knot):
            self.knots.append(self.head)
        if isinstance(self.tail, Knot):
            self.knots.append(self.tail)
       
        

    def add_to_tail(self, element: Node) -> None:

        self.links.append(element)

        self.tail = element

        self.id += ("-" + element.id)
        
        if self.tail == self.head:
            print("oczko")
            new_loop = Loop(self)


    
    def add_element(self, element: Node) -> None:
        new_knot = Knot(element, self)
    



class Loop: 
    loops = []

    def __init__(self, branch = Branch) -> None:
        self.its_branch = branch
        self.containment = branch.links
        Loop.loops.append(self)



class CircuitElement(Node):

    def join(self, element = Node) -> None:
        self.links.append(element)
        element.links.append(self)
        new_wire = Wire(self, element)
        Wire.wires.append(new_wire)

        case = (len(self.links) > 1, len(element.links) > 1)


        if case[0] == True:
            print("Element tworzacy jest juz czescia jakiegos obwodu")

        if case[1] == True:
            print("Element dodawany tworzy juz jakis obwod")
        
        

    
    def tie_to_wire(self, wire = Wire) -> None:

        if isinstance(wire.links[0], Knot):
            wire.links[0].add_to_knot(self)
        elif isinstance(wire.links[1], Knot):
            wire.links[1].add_to_knot(self)

        else:
            new_knot = Knot(self, wire)
            
            print("id knota: " + new_knot.id)

    

class Resistor(CircuitElement):

    resistors = []

    def __init__(self, id=str, res = 10) -> None:
        super().__init__(id)
        self.set_resistance(res)
        Resistor.resistors.append(self)

    def set_resistance(self, resistance = float) -> None:
        self.resistance = resistance


class VoltageGenerator(CircuitElement):

    generators = []

    def __init__(self, id: str, voltage: int = 10) -> None:
        super().__init__(id)
        self.set_voltage(voltage)
        VoltageGenerator.generators.append(self)
        self.dir = None
    
    def set_voltage(self, voltage = float) -> None:
        self.voltage = voltage     


    def set_direction(self, element: Node) -> None:

        self.dir = element


#   ----------------------- KONIEC STARYCH KLAS ---------------------------------







if __name__ == "__main__":
    resistor_1 = Res('R1')
    resistor_2 = Res('R2')
    resistor_3 = Res('R3')
    resistor_4 = Res('R4')
    resistor_5 = Res('R5')
    resistor_6 = Res('R6')
    voltage_gen_1 = PowerSuply('V1')
    voltage_gen_2 = PowerSuply('V2', 10)



    resistor_1.join_to(resistor_2)
    resistor_2.join_to(resistor_3)

    resistor_3.join_to(voltage_gen_2)
    voltage_gen_2.join_to(resistor_4)
    
    voltage_gen_2.direction = voltage_gen_2.set_direction(resistor_3)

    resistor_4.join_to(voltage_gen_1)
    voltage_gen_1.join_to(resistor_1)

    voltage_gen_1.direction = voltage_gen_1.set_direction(resistor_1)


    for branch in Branch2.branches:
        for element in branch.elements:
            if isinstance(element, Wire2):

                if resistor_1 in element.links and resistor_2 in element.links:
                    resistor_5.join_to(element)

                if resistor_2 in element.links and resistor_3 in element.links:
                    resistor_6.join_to(element)

                if voltage_gen_2 in element.links and resistor_4 in element.links:
                    resistor_6.join_to(element)

                if voltage_gen_1 in element.links and resistor_4 in element.links:
                    resistor_5.join_to(element)


    circuit = Circuit(Branch2.branches)

    for branch in Branch2.branches:
        print(f"GALAZ {Branch2.branches.index(branch) + 1}")
        for element in branch.elements:
            print(element.id)


    print(len(circuit.branches))