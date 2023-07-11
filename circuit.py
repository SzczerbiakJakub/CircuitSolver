import abc


class Element:

    elements = []
    resistors = []
    supplies = []
    
    def __init__(self) -> None:
        self.next = None
        self.prev = None
        Element.elements.append(self)
        self.links = []

    def join_to(self, element) -> None:

        if len(Branch.branches) == 0:
            self.links.append(element)
            element.links.append(self)
            Branch.branches.append(Branch(self, element))
            circuit = Circuit()
            circuit.branches = Branch.branches
            Circuit.circuits.append(circuit)

        elif isinstance(self, Wire):
            Node(self, element)

        elif isinstance(element, Wire):
            Node(element, self)

        else:
            self.links.append(element)
            element.links.append(self)
            both_exists = False
            for branch in Branch.branches:
                if self in branch.elements:
                    for another_branch in Branch.branches:
                        if element in another_branch.elements and another_branch is not branch:

                            branch.elements = branch.add_to_end(Wire(self, element))
                            branch.elements = branch.add_to_end(element)
                            both_exists = True

                            while len(another_branch.elements) != 1:
                                another_branch.elements.pop(-1)
                                branch.elements.append(another_branch.elements[-1])

                            Branch.branches.remove(another_branch)

                    if not both_exists:
                        branch.elements = branch.add_to_end(Wire(self, element))
                        branch.elements = branch.add_to_end(element)

                elif element in branch.elements:
                    for another_branch in Branch.branches:
                        if self in another_branch.elements and another_branch is not branch:

                            both_exists = True
                            branch.elements = branch.add_to_end(Wire(self, element))
                            branch.elements = branch.add_to_end(self)

                            while len(another_branch.elements) != 1:
                                another_branch.elements.pop(-1)
                                branch.elements.append(another_branch.elements[-1])

                            Branch.branches.remove(another_branch)

                    if not both_exists:
                        branch.elements = branch.add_to_end(Wire(self, element))
                        branch.elements = branch.add_to_end(self)

        print(f"Joined {self.id} and {element.id}")


    def remove(self) -> None:
        try:
            self.prev.next = self.next
            self.next.prev = self.prev
        except ZeroDivisionError:       #tu wstaw errora z brakiem elementow
            ...




class Resistor(Element):

    def __init__(self, resistance: float = 10) -> None:
        super().__init__()
        self.resistance = resistance

        Element.resistors.append(self)

        self.id = f"R{len(Element.resistors)}"

        print(f"REZYSTOR {self.id}")


    def set_resistance(self, resistance: float) -> None:
        self.resistance = resistance



class PowerSupply(Element):

    def __init__(self, voltage: float = 10) -> None:
        super().__init__()
        self.voltage = voltage
        self.direction = None

        Element.supplies.append(self)

        self.id = f"E{len(Element.supplies)}"


    def set_voltage(self, voltage: float) -> None:
        self.voltage = voltage
    

    def set_direction(self, direction: Element) -> None:
        self.direction = direction



class Wire(Element):

    def __init__(self, element1: Element, element2: Element) -> None:

        self.prev = element1
        self.head = element1
        self.next = element2
        self.tail = element2

        self.links = [element1, element2]

        self.id = str(f"{element1.id}-{element2.id}")

        if isinstance(element1, Node):
            element1.nexts.append(self)
            element2.prev = self

        elif isinstance(element2, Node):
            element1.next = self
            element2.prevs.append(self)
        
        else:
            element1.next = self
            element2.prev = self


class Node(Element):

    nodes = []

    def __init__(self, wire: Wire, element: Element) -> None:

        self.nexts = []
        self.prevs = []
        
        self.links = [wire.head, element, wire.tail]

        wire.head.links.remove(wire.tail)
        wire.head.links.append(self)
        
        wire.tail.links.remove(wire.head)
        wire.tail.links.append(self)

        element.links.append(self)

        self.id = str(f"{wire.head.id}x{element.id}x{wire.tail.id}")

        for branch in Branch.branches:
            if wire.head in branch.elements and wire.tail in branch.elements:
                print("MAMY W GALEZI")

                new_branch = Branch(self, wire.head)
                new_branch.elements.extend(branch.elements[:branch.elements.index(wire.head)])
                new_branch.tail = new_branch.elements[-1]
                Branch.branches.append(new_branch)

                new_branch = Branch(self, wire.tail)
                new_branch.elements.extend(branch.elements[branch.elements.index(wire.tail)+1:])
                new_branch.tail = new_branch.elements[-1]
                Branch.branches.append(new_branch)

                Branch.branches.remove(branch)

        new_branch = Branch(self, element)
        Branch.branches.append(new_branch)

        element_in_branches = False

        print("NOWY KNOCIARZ")

        Node.nodes.append(self)

        



class Branch:

    branches = []
    created_branches = []
    
    def __init__(self, element1: Element, element2: Element) -> None:
        new_wire = Wire(element1, element2)
        self.elements = [element1, element2]
        self.head = element1
        self.tail = element2
        self.is_loop = False

    def add_to_end(self, element: Element) -> list:
        if element in self.elements:
            Loop.loops.append(Loop(self))
            print("powstalo oczko")
            self.is_loop = True
            return self.elements
        else:
            self.elements.append(element)
            self.tail = element
            return self.elements

    def add_to_start(self, element: Element) -> list:
        if element in self.elements:
            Loop.loops.append(Loop(self))
            print("powstalo oczko")
            self.is_loop = True
            return self.elements
        else:
            self.elements.insert(0, element)
            self.head = element
            return self.elements
        
    def add_element(self, element: Element) -> None:
        ...

    def show() -> None:
        for x in Branch.branches:
            text = ""
            for y in x.elements:
                text = text + " " + y.id
            print(text)

    def create_branches(nodes = Node.nodes) -> list:

        branches = []

        for node in nodes:
            for element in node.links:

                exists = False
                for x in branches:
                    if element in x.elements:
                        exists = True

                if not exists:
                    new_branch = Branch(node, element)
                    while not isinstance(new_branch.tail, Node):
                        if new_branch.tail.links[0] in new_branch.elements:
                            new_branch.add_to_end(new_branch.tail.links[1])
                        else:
                            new_branch.add_to_end(new_branch.tail.links[0])

                    branches.append(new_branch)

        for x in branches:
            x.head = x.elements[0]
            x.tail = x.elements[-1]
            text = ""
            for y in x.elements:
                text = text + " " + y.id
            print(text)

        return branches



class Loop:

    loops = []

    def __init__(self, loopedBranch: Branch) -> None:
        self.loopedBranch = loopedBranch



class Circuit:      #   ON MA OBSLUGIWAC LOGIKE

    circuits = []
    
    resistors = []

    
    def __init__(self) -> None:
        self.elements = []
        self.branches = []
        self.nodes = []
        self.currents = {}
        for branch in self.branches:
            self.currents.update({branch.head.id + "-" + branch.tail.id : 0})
        
        self.loops = []
        Circuit.circuits.append(self)


    def add_branch(self, branch: Branch) -> None:
        self.branches.append(branch)

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def add_element(self, element: Element) -> None:
        self.elements.append(element)
        

    def add_loop(self, loop: Loop) -> None:
        self.loops.append(loop)



    #   OGARNIAJ LOGIKE


    def compute(self, method) -> list:
        method(self.branches)   #   STOSUJE TE FUNKCJE I SE LICZY
        return self.branches
    

    def print_nodes(nodes: list[Node] = Node.nodes) -> None:
        print("NODE'Y:")
        for x in nodes:
            print(x.id)

        


def join(element_1: Element, element_2: Element):

    if type(element_1) != Wire and type(element_2) != Wire:
        element_1.links.append(Wire(element_1, element_2))
        element_2.links.append(Wire(element_1, element_2))

    elif type(element_1) == Wire:
        node = Node(element_1, element_2)
        element_2.links.append(node)


    elif type(element_2) == Wire:
        node = Node(element_2, element_1)
        element_1.links.append(node)


if __name__ == "__main__":

    this_circuit =  Circuit()


    resistor_1 = Resistor()
    this_circuit.add_element(resistor_1)

    resistor_2 = Resistor()
    this_circuit.add_element(resistor_2)

    print("TYPE REZYSTORA R2")
    print(type(resistor_2))
    if type(resistor_2) is Resistor:
        print("Jest rezystorem")

    resistor_3 = Resistor()
    this_circuit.add_element(resistor_3)
    
    resistor_4 = Resistor()
    this_circuit.add_element(resistor_4)
    
    resistor_5 = Resistor()
    this_circuit.add_element(resistor_5)

    resistor_6 = Resistor()
    this_circuit.add_element(resistor_6)

    voltage_gen_1 = PowerSupply()
    this_circuit.add_element(voltage_gen_1)

    voltage_gen_2 = PowerSupply(10)
    this_circuit.add_element(voltage_gen_2)



    resistor_1.join_to(resistor_2)
    join(resistor_1, resistor_2)

    resistor_2.join_to(resistor_3)
    join(resistor_2, resistor_3)

    resistor_3.join_to(voltage_gen_2)
    join(resistor_3, voltage_gen_2)

    voltage_gen_2.join_to(resistor_4)
    join(voltage_gen_2, resistor_4)
    
    voltage_gen_2.direction = voltage_gen_2.set_direction(resistor_3)

    resistor_4.join_to(voltage_gen_1)
    join(voltage_gen_1, resistor_4)

    voltage_gen_1.join_to(resistor_1)
    join(voltage_gen_1, resistor_1)

    voltage_gen_1.direction = voltage_gen_1.set_direction(resistor_1)


    for branch in Branch.branches:
        for element in branch.elements:
            if isinstance(element, Wire):

                if resistor_1 in element.links and resistor_2 in element.links:
                    resistor_5.join_to(element)

                if resistor_2 in element.links and resistor_3 in element.links:
                    resistor_6.join_to(element)

                if voltage_gen_2 in element.links and resistor_4 in element.links:
                    resistor_6.join_to(element)

                if voltage_gen_1 in element.links and resistor_4 in element.links:
                    resistor_5.join_to(element)

    circuit = Circuit.circuits[0]

    for branch in circuit.branches:
        print(f"GALAZ {circuit.branches.index(branch) + 1}")
        for element in branch.elements:
            print(element.id)
        print(f"HEAD:    {branch.head.id},  TAIL:   {branch.tail.id}")


    print(len(circuit.branches))

    print(Node.nodes)

    print(circuit.currents)

    for element in this_circuit.elements:
        print(element.id)
        for link in element.links:
            print(f"POLACZENIE: {link.id}")

    #calc.nodal_analysis(circuit, Node.nodes)
