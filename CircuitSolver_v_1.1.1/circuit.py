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
        elif isinstance(element_1, Knot):
            self.id = element_1.id + ":" + element_2.id
            self.head = element_1
            self.tail = element_2
        elif element_1.id > element_2.id:
            self.id = element_2.id + ":" + element_1.id
            self.head = element_2
            self.tail = element_1
        else:
            self.id = element_1.id + ":" + element_2.id
            self.head = element_1
            self.tail = element_2

        self.links = [self.head, self.tail]

        element_1.next = element_2
        element_2.prev = element_1

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

        if isinstance(element, Knot):
            self.knots.append(element)
        
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
        self.dir = 1
    
    def set_voltage(self, voltage = float) -> None:
        self.voltage = voltage     


    def set_direction(self, element: Node) -> None:

        self.dir = element