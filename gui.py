from tkinter import *
from tkinter import ttk
from customtkinter import *
from PIL import Image, ImageTk

from calc import *
import circuit
import time
import threading



exitFlag = 0

class GUIThread (threading.Thread):
    def __init__(self, threadID, name, counter, delay, object, event, printing=False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay
        self.object = object
        self.event = event
        self.printing = printing
    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.counter, self.delay, self.printing, self.object, self.event, self.threadID)

        if not self.object.wait_for_properties:
            print("PRZERWANO THREADA")
            return
        
        print("Exiting " + self.name)
        self.finished(self.object, self.event)


    def finished(self, object, event) -> None:
        if object.wait_for_properties:
            Menu.open_properties_table(object, event.x, event.y)



def print_time(threadName, counter, delay, printing, object, event, id):

    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        if printing:
            print(threadName)
        
        """if Mouse.left_button_is_held and id == -1:
            object.wait_for_properties = False
            drag(event, object, object.root)"""

        counter -= 1



def change_position(event):
    super.place((event.x, event.y))


#   FUNKCJA ZMIENIAJACA SKINKA DO ELEMENTOW


def change_image(path) -> ImageTk.PhotoImage:
    img_name = Object.allign + "_resistor_selected.png"
    res_img = Image.open("img/" + img_name)

    resolution = (int(res_img.width / 5), int(res_img.height / 5))
    print(resolution)



class Mouse:

    x = None
    y = None


    left_button_is_held = False

    def mouse_motion(event):
        Mouse.x, Mouse.y = event.x, event.y
        #print('MOUSE: {}, {}'.format(Mouse.x, Mouse.y))


    def left_button_held(event):
        print("LPM CLICKED")
        Mouse.left_button_is_held = True

    def left_button_released(event):
        print("LPM RELEASED")
        Mouse.left_button_is_held = False


def pos_on_widget(event):
    Mouse.on_widget_x, Mouse.on_widget_y = event.x, event.y






class Object:

    resistor = None
    allign = None
    objects = []
    wires = []
    resistors = []
    nodes = []
    supplies = []

    joining = None
    joining_element = None
    joining_side = None
    joining_state = False

    def get_resistor_ammount():
        print(len(Object.objects))


    def join(self, master, element_2, side_1, side_2) -> None:
        new_wire = Wire(master, self, element_2, side_1, side_2)
        self.connections.append(element_2)
        element_2.connections.append(self)

    
    
    def joining_simul(event, element):
        if element.allign == 'horizontal':
            if event.x < element.coords['x']:
                Object.joining_side = "LEFT"
            else:
                Object.joining_side = "RIGHT"

        elif element.allign == 'vertical':
            if event.y < element.coords['y']:
                Object.joining_side = "UPPER"
            else:
                Object.joining_side = "LOWER"
    

    def check_joining(object):

        if Object.joining is not None and object is not Object.joining:
            print(f"JOINED: {Object.joining_state} and {object.state}")
            Object.joining.join(object, object.resistor.master)
            Object.joining = None
        

    def get_wire_origin(element, side):
        if side == 'LEFT':
            return (element.coords['x']-element.width/2, element.coords['y'])
        elif side == 'RIGHT':
            return (element.coords['x']+element.width/2, element.coords['y'])
        elif side == 'UPPER':
            return (element.coords['x'], element.coords['y']-element.height/2)
        elif side == 'LOWER':
            return (element.coords['x'], element.coords['y']+element.height/2, element)

        elif side == "NODE":
            return (element.coords['x'], element.coords['y'])



def cursor_over_widget(event, object):

    if object.properties_shown == False:
        object.properties_thread = GUIThread(len(circuit.Element.resistors), object.entity.id+" THREAD", 1, 2, object, event)
        object.properties_thread.start()

    object.wait_for_properties = True
    Menu.over_widget = True
    print("NAD WIDGETEM")


def cursor_left_widget(event, object):
    object.wait_for_properties = False
    Menu.over_widget = False
    print("OPUSZCZONO WIDGET")

def show_properties(event, object):
    object.properties_shown = True
    Menu.open_properties_table(object, event.x, event.y)

    




class Resistor(Object):

    
    def __init__(self, root, x, y, allign: str = 'horizontal'):

        self.entity = circuit.Resistor()

        self.root = root

        self.first_electrode = None
        self.second_electrode = None
        self.selected_electrode = None
        self.wires = []
        self.connections = []
        self.coords = {'x': x, 'y': y}
        self.resistance = 10
        self.properties_shown = False

        self.generate_sprite(self.coords['x'], self.coords['y'], root, allign)

        Object.resistor = self
        self.allign = allign

        Object.objects.append(self)
        Object.resistors.append(self)

        self.state = "unselected"

        print(f"REZYSTOR: {self.coords['x']}, {self.coords['y']}, {self.width}, {self.height}")


    
    def __str__(self):
        return("SRACKA")
    


    def generate_sprite(self, x, y, root, allign: str ='horizontal', anchor=CENTER):

        try:
            root.delete(self.id)
        except AttributeError:
            ...

        path = f"img/{allign}_resistor.png"
        res_img = Image.open(path)
        resolution = (res_img.width, res_img.height)

        resolution = (int(resolution[0] / 5), int(resolution[1] / 5))
        print(resolution)

        self.res_img = ImageTk.PhotoImage(res_img.resize(resolution))

        self.coords['x'] = x
        self.coords['y'] = y

        self.width, self.height = resolution
        
        """try:
            root.destroy(self.name)
        except AttributeError:
            ..."""

        self.id = root.create_image(x, y, image = self.res_img, anchor=anchor)

        try:
            root.delete(self.name)
        except AttributeError:
            ...

        self.name = root.create_text(x, y, text = self.entity.id, fill="green", font=('Helvetica 10 bold'), anchor=anchor)

        root.tag_bind(self.id, '<Button-2>', lambda event: select(event, self, root))
        root.tag_bind(self.id, '<Button-1>', lambda event: drag(event, self, root))
        root.tag_bind(self.id, '<ButtonRelease-1>', lambda event: move(event, self, root))
        root.tag_bind(self.id, '<ButtonRelease-3>', lambda event: Menu.open_menu(event, self, root))
        
        #root.tag_bind(self.id, '<Enter><Motion>', lambda event: select_widget(event, self, root))
        root.tag_bind(self.id, '<Leave>', lambda event: unselect_widget(event, self))

        root.tag_bind(self.id, '<Enter>', lambda event: cursor_over_widget(event, self))
        root.tag_bind(self.id, '<Leave>', lambda event: cursor_left_widget(event, self), add = "+")


        root.tag_bind(self.name, '<Button-2>', lambda event: select(event, self, root))
        root.tag_bind(self.name, '<ButtonRelease-1>', lambda event: move(event, self, root))
        root.tag_bind(self.name, '<ButtonRelease-3>', lambda event: Menu.open_menu(event, self, root))
        
        #root.tag_bind(self.id, '<Enter><Motion>', lambda event: select_widget(event, self, root))
        root.tag_bind(self.name, '<Leave>', lambda event: unselect_widget(event, self))
        #root.tag_bind(self.name, '<Enter>', lambda event: show_properties(event, self), add="+")


    def set_resistance(self):
        ...


    def show_properties(self, event):
        
        self.properties_label = CTkLabel(self.root, width=self.width, height = 10, text=str(self.resistance)+" Ohm", text_color="black")
        self.properties_label.place(x=self.coords['x'], y = self.coords['y']-15)
        print("PROPERTIES")

    def hide_properties(self, event):
        self.properties_label.destroy()
        



class PowerSupply(Object):

    def __init__(self, root, x, y, allign: str = 'horizontal', dir: str = "left"):

        self.entity = circuit.PowerSupply()

        self.first_electrode = None
        self.second_electrode = None
        self.selected_electrode = None
        self.wires = []
        self.connections = []
        self.coords = {'x': x, 'y': y}

        self.dir = dir

        self.generate_sprite(self.coords['x'], self.coords['y'], root, allign)

        self.allign = allign

        Object.objects.append(self)
        Object.supplies.append(self)

        self.state = "unselected"

        print(f"ZASILACZ: {self.coords[0]}, {self.coords[1]}, {self.width}, {self.height}")


    
    def __str__(self):
        return("ZASILACZOR")
    


    def generate_sprite(self, x, y, root, allign: str, anchor=NW):

        try:
            root.delete(self.id)
        except AttributeError:
            ...

        path = f"img/{allign}_{self.dir}_supply.png"

        vs_img = Image.open(path)
        resolution = (vs_img.width, vs_img.height)

        resolution = (int(resolution[0] / 3), int(resolution[1] / 3))
        print(resolution)

        self.vs_img = ImageTk.PhotoImage(vs_img.resize(resolution))

        self.coords['x'] = x
        self.coords['y'] = y

        self.width, self.height = resolution

        self.id = root.create_image(x, y, image = self.vs_img, anchor=anchor)

        try:
            root.delete(self.name)
        except AttributeError:
            ...

        self.name = root.create_text(x+self.width/2, y+self.height/2, text = self.entity.id, fill="green", font=('Helvetica 10 bold'))
        

        root.tag_bind(self.id, '<ButtonRelease-2>', lambda event: select(event, self, root))
        root.tag_bind(self.id, '<ButtonRelease-1>', lambda event: move(event, self, root))
        root.tag_bind(self.id, '<ButtonRelease-3>', lambda event: Menu.open_menu(event, self, root))
        
        #root.tag_bind(self.id, '<Enter><Motion>', lambda event: select_widget(event, self, root))
        root.tag_bind(self.id, '<Leave>', lambda event: unselect_widget(event, self))

        root.tag_bind(self.id, '<Enter>', lambda event: cursor_over_widget(event, self))
        root.tag_bind(self.id, '<Leave>', cursor_left_widget, add = "+")



        root.tag_bind(self.name, '<ButtonRelease-2>', lambda event: select(event, self, root))
        root.tag_bind(self.name, '<ButtonRelease-1>', lambda event: move(event, self, root))
        root.tag_bind(self.name, '<ButtonRelease-3>', lambda event: Menu.open_menu(event, self, root))
        
        #root.tag_bind(self.id, '<Enter><Motion>', lambda event: select_widget(event, self, root))
        root.tag_bind(self.name, '<Leave>', lambda event: unselect_widget(event, self))


    def set_voltage(self):
        ...




class Wire(Object):

    texture_img = Image.open("img/wire_txt.png")
    

    
    def __init__(self, root, element_1, element_2, side_1, side_2):

        self.entity = circuit.Wire(element_1.entity, element_2.entity)
        
        self.params = None
        self.state = None

        self.elements_linked = {element_1 : side_1, element_2 : side_2}

        self.node = None

        if isinstance(element_1, Node):
            self.node = element_1
        elif isinstance(element_2, Node):
            self.node = element_2

        element_1.wires.append(self)
        element_2.wires.append(self)


        self.draw(root, element_1, element_2, side_1, side_2)

        Object.wires.append(self)
        #self.wire_widget.place(x = element_1.resistor.winfo_x()+100, y = element_1.resistor.winfo_y()+20)


        
    

    def draw(self, root, element_1, element_2, side_1, side_2):
        
        self.origin_1 = Object.get_wire_origin(element_1, side_1)
        self.origin_2 = Object.get_wire_origin(element_2, side_2)

        self.horizontal_wire = root.create_line(self.origin_1[0], self.origin_1[1], self.origin_2[0], self.origin_1[1], fill="grey", width=6)
        self.vertical_wire = root.create_line(self.origin_2[0], self.origin_1[1], self.origin_2[0], self.origin_2[1], fill="grey", width=6)

        self.id = (self.horizontal_wire, self.vertical_wire)

        root.tag_bind(self.horizontal_wire, '<Button-2>', lambda event: select_wire(event, self, root))
        root.tag_bind(self.vertical_wire, '<Button-2>', lambda event: select_wire(event, self, root))


    def delete(self, root) -> None:
        for element in list(self.elements_linked.keys()):
            element.wires.remove(self)

        self.remove_img(root)

    def remove_img(self, root) -> None:
        root.delete(self.horizontal_wire)
        root.delete(self.vertical_wire)
        root.delete(self.id)


        




class Node(Object):


    def __init__(self, root, event, element, wire):

        self.entity = circuit.Node(wire.entity, element.entity)
        
        self.params = None
        self.state = None

        self.elements_linked = {}
        self.wires = []
        self.connections = []

        self.coords = {'x': 100, 'y': 100}

        self.draw(root, event, element, wire)

        Object.nodes.append(self)
        #self.wire_widget.place(x = element_1.resistor.winfo_x()+100, y = element_1.resistor.winfo_y()+20)

    def generate_node_img(self, root, x, y) -> None:
        self.id = root.create_oval(x - 8, y - 8, x + 8, y + 8, fill="black")

        root.tag_bind(self.id, '<ButtonRelease-2>', lambda event: select(event, self, root))
        root.tag_bind(self.id, '<ButtonRelease-1>', lambda event: move(event, self, root))
        root.tag_bind(self.id, '<ButtonRelease-3>', lambda event: Menu.open_menu(event, self, root))
        
        root.tag_bind(self.id, '<Leave>', lambda event: unselect_widget(event, self))


    def regenerate_node_img(self, root) -> None:
        root.delete(self.id)
        self.generate_node_img(root, self.coords['x'], self.coords['y'])


    def draw(self, root, event, element, wire):

        self.coords['x'] = event.x
        self.coords['y'] = event.y

        self.join(root, element, "NODE", Object.joining_side)
        self.elements_linked.update({element : Object.joining_side})

        elements = list(wire.elements_linked.keys())

        self.join(root, elements[0], "NODE", wire.elements_linked[elements[0]])
        self.elements_linked.update({elements[0] : wire.elements_linked[elements[0]]})

        self.join(root, elements[1], "NODE", wire.elements_linked[elements[1]])
        self.elements_linked.update({elements[1] : wire.elements_linked[elements[1]]})

        delete_object(root, wire)

        #Wire(root, element, self, Object.joining_side, "NODE")

        self.generate_node_img(root, self.coords['x'], self.coords['y'])

        print(f"NARYSOWANO NODEA, ile wireow: {len(self.wires)}, {len(self.elements_linked)}")




    def redraw(self, x, y, root):

        self.coords['x'] = x
        self.coords['y'] = y

        wire_ammount = len(self.wires)

        for x in range(0, wire_ammount):
           self.wires[0].delete(root)
           print(len(self.wires))

        print(self.coords)

        for element in list(self.elements_linked.keys()):
            self.join(root, element, "NODE", self.elements_linked[element])

        self.regenerate_node_img(root)







def delete_object(master, object):

    if isinstance(object, Wire):
        for element in list(object.elements_linked.keys()):
            element.wires.remove(object)
        master.delete(object.horizontal_wire)
        master.delete(object.vertical_wire)

    if isinstance(object, Resistor):
        #circuit.Element.resistors.remove(object.entity)
        for wire in object.wires:

            for element in list(wire.elements_linked.keys()):
                if element is not object:
                    element.wires.remove(wire)

            master.delete(wire.horizontal_wire)
            master.delete(wire.vertical_wire)

        Object.resistors.remove(object)
        Application.current_root.resistors_info.configure(text = f"Resistors: {len(Object.resistors)}")
    elif isinstance(object, PowerSupply):
        #circuit.Element.supplies.remove(object.entity)

        for wire in object.wires:

            for element in list(wire.elements_linked.keys()):
                if element is not object:
                    element.wires.remove(wire)

            master.delete(wire.horizontal_wire)
            master.delete(wire.vertical_wire)

        Object.supplies.remove(object)
        Application.current_root.supplies_info.configure(text = f"Supplies: {len(Object.supplies)}")


    object.coords = None
    master.delete(object.id)
    
    if not isinstance(object, Wire):
        master.delete(object.name)

    object.coords = None
    object.width = None
    object.height = None




class Menu:

    over_widget = False

    def open_properties_table(object, event_x, event_y):
        object.properties_table = Label(object.root, text=f"{object.resistance} Ohm", bg="white", borderwidth=1, relief="solid")
        object.properties_table.place(x=event_x, y=event_y, anchor=CENTER)

        object.properties_table.bind("<Leave>", lambda event: Menu.close_object_properties(object.properties_table, object))

    def close_object_properties(label, object):
        object.properties_shown = False
        label.destroy()

    def close_menu(menu):
        menu.destroy()

    def optionmenu_callback(choice, event, master, menu, object):
        print("optionmenu dropdown clicked:", choice)
        if choice == "Exit":
            Menu.close_menu(menu)
        elif choice == "Links":
            Menu.close_menu(menu)
            for x in object.entity.links:
                print(x.id)

        elif choice == "Rotate":
            Menu.close_menu(menu)
            rotate(object, master)
        elif choice == "Set resistance":
            input = Menu.open_resistance_input(master, menu, object)
        elif choice == "Set voltage":
            input = Menu.open_voltage_input(master, menu, object)
        elif choice == "Join":
            Menu.close_menu(menu)
            Object.joining = object
            Object.joining_state = True
            Object.joining_simul(event, object)
            print("JOINING...")
        elif choice == "Delete":
            Menu.close_menu(menu)
            delete_object(master, object)


    def open_menu(event, object, master):

        print(object)

        #print(object.state)
        if isinstance(object, Resistor):
            menu = CTkSegmentedButton(master, values=["Links", "Rotate", "Join", "Exit", "Delete"], command=lambda choice: Menu.optionmenu_callback(choice, event, master, menu, object))
        #menu.bind("<ButtonRelease-3>", lambda event: Menu.close_menu(event, menu))
        elif isinstance(object, PowerSupply):
            menu = CTkSegmentedButton(master, values=["Set voltage", "Rotate", "Join", "Exit", "Delete"], command=lambda choice: Menu.optionmenu_callback(choice, event, master, menu, object))
        #menu.bind("<ButtonRelease-3>", lambda event: Menu.close_menu(event, menu))
        elif isinstance(object, Wire):
            menu = CTkSegmentedButton(master, values=["Set wire heh", "Rotate", "Join", "Exit", "Delete"], command=lambda choice: Menu.optionmenu_callback(choice, event, master, menu, object))
        elif isinstance(object, Node):
            menu = CTkSegmentedButton(master, values=["Links", "Exit"], command=lambda choice: Menu.optionmenu_callback(choice, event, master, menu, object))
        else:
            Object.joining_state = object.state
            menu = CTkSegmentedButton(master, values=["Join", "Delete", "Exit"], command=lambda choice: Menu.optionmenu_callback(choice, event, master, menu, object))
        
        menu.width = 230

        if event.x + menu.width > int(master.cget('width')):
            pos_x = int(master.cget('width')) - menu.width
        else:
            pos_x = event.x

        if event.y + int(menu.cget('height')) > int(master.cget('height')):
            pos_y = int(master.cget('height')) - int(menu.cget('height'))
        else:
            pos_y = event.y

        menu.place(x=pos_x, y=pos_y)
        menu.bind("<Leave><Button-3>", menu.destroy)

    
    def map_option_menu_callback(choice, event, master, menu):
        if choice == "Resistor":
            Menu.close_menu(menu)
            Application.create_resistor(master, event.x, event.y)
        elif choice == "Power Supply":
            Menu.close_menu(menu)
            Application.create_vs(master, event.x, event.y)
        elif choice == "Exit":
            Menu.close_menu(menu)


    def open_map_menu(event, master):
        if Menu.over_widget is not True:
            menu = CTkSegmentedButton(master, width = 185, values=["Resistor", "Power Supply", "Exit"], command=lambda choice: Menu.map_option_menu_callback(choice, event, master, menu))
            
            menu.width = 185

            if event.x + menu.width > int(master.cget('width')):
                pos_x = int(master.cget('width')) - menu.width
            else:
                pos_x = event.x

            if event.y + int(menu.cget('height')) > int(master.cget('height')):
                pos_y = int(master.cget('height')) - int(menu.cget('height'))
            else:
                pos_y = event.y

            menu.place(x=pos_x, y=pos_y)
            


    def open_resistance_input(master, menu, object):
        input = CTkEntry(master, placeholder_text="Enter resistance value, press enter...:")
        input.bind("<Return>", lambda event: Menu.set_resistance_value(input, object))

        input.place(x = menu.winfo_x(), y = menu.winfo_y())
        Menu.close_menu(menu)

        return input

    def open_voltage_input(master, menu, object):
        input = CTkEntry(master, placeholder_text="Enter voltage value, press enter...:")
        input.bind("<Return>", lambda event: Menu.set_voltage_value(input, object))

        input.place(x = menu.winfo_x(), y = menu.winfo_y())
        Menu.close_menu(menu)

        return input
    
    def set_voltage_value(input, object):
        value = float(input.get())

        if value >= 0:
            object.voltage = value
            Menu.close_menu(input)

    def set_resistance_value(input, object):
        value = float(input.get())

        if value >= 0:
            object.resistance = value
            Menu.close_menu(input)






def select(event, element, root):

    element.wait_for_properties = False

    print(f"{Object.joining_state}")
    
    if Object.joining_state:

        if isinstance(element, Wire):
            if element.node is None:
                Node(root, event, Object.joining, element)
            else:
                element.node.join(root, Object.joining, "NODE", Object.joining_side)
                element.node.elements_linked.update({Object.joining : Object.joining_side})
                Object.joining.entity.join_to(element.node.entity)

        elif isinstance(Object.joining, Wire):
            if Object.joining.node is None:
                Node(root, event, element, Object.joining)
            else:
                Object.joining.node.join(root, element, "NODE", Object.joining_side)
                Object.joining.node.entity.join_to(element.entity)
            

        else:
            Object.joining.entity.join_to(element.entity)

            if element.allign == 'horizontal':
                if event.x < element.coords['x'] + element.width/2:
                    Object.joining.join(root, element, Object.joining_side, 'LEFT')
                    print(f"{Object.joining_side} + LEFT")
                else:
                    Object.joining.join(root, element, Object.joining_side, 'RIGHT')
                    print(f"{Object.joining_side} + RIGHT")

            elif element.allign == 'vertical':
                if event.y < element.coords['y'] + element.height/2:
                    Object.joining.join(root, element, Object.joining_side, 'UPPER')
                    print(f"{Object.joining_side} + UPPER")
                else:
                    Object.joining.join(root, element, Object.joining_side, 'LOWER')
                    print(f"{Object.joining_side} + LOWER")


        Object.joining_state = False
        Object.joining_side = None
                


def select_wire(event, wire, root):

    wire.wait_for_properties = False

    print(f"{Object.joining_state}")
    
    if Object.joining_state:

        if isinstance(wire, Wire):
            if wire.node is None:
                Node(root, event, Object.joining, wire)
            else:
                wire.node.join(root, Object.joining, "NODE", Object.joining_side)
                wire.node.elements_linked.update({Object.joining : Object.joining_side})
                Object.joining.entity.join_to(wire.node.entity)

        elif isinstance(Object.joining, Wire):
            if Object.joining.node is None:
                Node(root, event, wire, Object.joining)
            else:
                Object.joining.node.join(root, wire, "NODE", Object.joining_side)
                Object.joining.node.entity.join_to(wire.entity)
            

        else:
            Object.joining.entity.join_to(wire.entity)

            if wire.allign == 'horizontal':
                if event.x < wire.coords['x'] + wire.width/2:
                    Object.joining.join(root, wire, Object.joining_side, 'LEFT')
                    print(f"{Object.joining_side} + LEFT")
                else:
                    Object.joining.join(root, wire, Object.joining_side, 'RIGHT')
                    print(f"{Object.joining_side} + RIGHT")

            elif wire.allign == 'vertical':
                if event.y < wire.coords['y'] + wire.height/2:
                    Object.joining.join(root, wire, Object.joining_side, 'UPPER')
                    print(f"{Object.joining_side} + UPPER")
                else:
                    Object.joining.join(root, wire, Object.joining_side, 'LOWER')
                    print(f"{Object.joining_side} + LOWER")


        Object.joining_state = False
        Object.joining_side = None


def drag(event, element, root):

    """element.movement_thread = GUIThread(-1, element.entity.id+" MOVING...", 1, 1, element, event, True)
    element.movement_thread.start()"""

    print("MOVING")
    """move(event, element, root)"""

    '''while Mouse.left_button_is_held:
        element.movement_thread = GUIThread(-1, object.entity.id+" MOVING...", 1, object, event, True)
        element.movement_thread.start()'''
        #move(event, element, root)

def move(event, element, root):
    movement = (Mouse.x, Mouse.y)

    if isinstance(element, Node):
        element.redraw(movement[0], movement[1], root)

    else:
        element.generate_sprite(movement[0], movement[1], root, element.allign)
        

        for wire in element.wires:
            #wire.generate_sprite_2(wire.elements_linked[0], wire.elements_linked[1])
            element_list = list(wire.elements_linked.keys())
            
            wire.remove_img(root)
            
            wire.draw(root, element_list[0], element_list[1],  wire.elements_linked[element_list[0]], wire.elements_linked[element_list[1]])
            

            print("KABEL DO PRZESUNIECIA")
        
    for element in element.connections:
        if isinstance(element, Node):
            element.regenerate_node_img(root)
        
    print(f'MOVED TO: {movement[0]}, {movement[1]}, id: {element.id}')



def rotate(element, root):

    size = (element.width, element.height)

    if element.allign == "horizontal":

        element.allign = "vertical"

        if isinstance(element, PowerSupply):
        

            if element.dir == "left":
                element.dir = "up"
            else:
                element.dir = "down"

        element.generate_sprite(element.coords['x'], element.coords['y'], root, "vertical")

    elif element.allign == "vertical":

        element.allign = "horizontal"

        if isinstance(element, PowerSupply):
            if element.dir == "up":
                element.dir = "right"
            else:
                element.dir = "left"
            
            print("iok")

        element.generate_sprite(element.coords['x'], element.coords['y'], root, "horizontal")

    element.width, element.height = size[1], size[0]

    for wire in element.wires:
        #wire.generate_sprite_2(wire.elements_linked[0], wire.elements_linked[1])
        element_list = list(wire.elements_linked.keys())

        
        if wire.elements_linked[element] == "LEFT":
            wire.elements_linked[element] = "UPPER"
        elif wire.elements_linked[element] == "RIGHT":
            wire.elements_linked[element] = "LOWER"
        elif wire.elements_linked[element] == "UPPER":
            wire.elements_linked[element] = "LEFT"
        elif wire.elements_linked[element] == "LOWER":
            wire.elements_linked[element] = "RIGHT"

        former_wire_id = wire.id
        wire.draw(root, element_list[0], element_list[1],  wire.elements_linked[element_list[0]], wire.elements_linked[element_list[1]])
        
        for x in former_wire_id:
            root.delete(x)

        print("KABEL DO PRZESUNIECIA")


    print(f"OBJECT ROTATED: {element.width}, {element.height}, coords: {element.coords}")



def set_skin(widget, name, root):
    res_img = Image.open("img/" + name)

    resolution = (int(res_img.width / 5), int(res_img.height / 5))
    print(resolution)

    res_img = ImageTk.PhotoImage(res_img.resize(resolution))

    #widget.resistor.configure(image=res_img)
    #root.delete(widget.resistor_image)



def select_widget(event, widget, root):

    if widget.allign == "horizontal":

        img_name = widget.allign + "_resistor_selected.png"
        widget.state = "selected"
        
        '''
        if event.x < 23:
            img_name = widget.allign + "_resistor_LWS.png"
            widget.state = "h_lws"
            Object.check_joining(widget)

        elif event.x > 77:
            img_name = widget.allign + "_resistor_RWS.png"
            widget.state = "h_rws"
            Object.check_joining(widget)
        
        else:
            img_name = widget.allign + "_resistor_selected.png"
            widget.state = "selected"
        '''
        
        set_skin(widget, img_name, root)


    elif widget.allign == "vertical":

        img_name = widget.allign + "_resistor_selected.png"
        widget.state = "selected"
        
        '''
        if event.y < 23:
            img_name = widget.allign + "_resistor_UWS.png"
            widget.state = "v_uws"
            Object.check_joining(widget)
        
        elif event.y > 77:
            img_name = widget.allign + "_resistor_LWS.png"
            widget.state = "v_lws"
            Object.check_joining(widget)

        else:
            img_name = widget.allign + "_resistor_selected.png"
            widget.state = "selected"
        '''

        set_skin(widget, img_name, root)

    """res_img = Image.open("img/" + img_name)

    resolution = (int(res_img.width / 5), int(res_img.height / 5))
    print(resolution)

    res_img = ImageTk.PhotoImage(res_img.resize(resolution))

    resistor.configure(image=res_img)"""



def unselect_widget(event, widget):

    '''
    img_name = widget.allign + "_resistor.png"
    res_img = Image.open("img/" + img_name)

    resolution = (int(res_img.width / 5), int(res_img.height / 5))

    res_img = ImageTk.PhotoImage(res_img.resize(resolution))

    widget.resistor.configure(image=res_img)
    '''

    widget.state = "unselected"


class InputDialog:

    def __init__(self, apk) -> None:
        self.window = CTkLabel(apk.root, width=100, height=100).place(x=100, y=100)


class ToplevelWindow(CTkToplevel):

    def __init__(self, apk):
        super().__init__()
        self.title("New Project")
        self.geometry("300x120")

        self.input = CTkEntry(self, width = 250, placeholder_text="Enter new project's name...")
        self.ok_button = CTkButton(self, width=80, height=30, text="OK", command=lambda: self.after_ok(apk)).place(x=40, y = 70)
        self.bind("<FocusIn><Return>", lambda event: self.after_ok(apk))
        self.bind("<FocusIn><Escape>", lambda event: self.after_cancel(), add='+')
        self.cancel_button = CTkButton(self, width=80, height=30, text="Cancel", command=self.after_cancel).place(x=180, y = 70)

        self.input.pack(padx=20, pady=20)
        
    
    def after_ok(self, apk) -> str:
        project_name = self.input.get()
        if project_name == "":
            return
    
        Project.new_project(apk, project_name)
        self.destroy()
    

    def after_cancel(self):
        self.destroy()




class ProjectStream:
    
    def save_project():
        ...

    def load_project():
        ...


class Project:
    
    def __init__(self, name: str, apk) -> None:
        print(f"NOWY PROJEKT - {name}")
        self.name = name
        self.objects = []
        self.wires = []
        self.resistors = []
        self.nodes = []
        self.supplies = []

        self.create_sheet(apk)

        Application.current_info = self.info


    def create_sheet(self, apk):
        self.map = CTkCanvas(apk.root, width=800, height = 600, bg='white')
        self.info = CTkFrame(apk.root, width=100, height = 500, fg_color="white")
        self.sheet_name = CTkLabel(self.info, text=self.name, text_color="black").pack()
        self.branches_info = CTkButton(self.info, width = 90, height = 50, text_color="white", text= "Check branches", command=apk.create_branches)
        self.branches_info.pack()
        self.nodes_info = CTkButton(self.info, width = 90, height = 50, text_color="white", text= "Check nodes", command=circuit.Circuit.print_nodes)
        self.nodes_info.pack()
        self.resistors_info = CTkLabel(self.info, width = 90, height = 50, bg_color="black", text_color="white", text= "")
        self.resistors_info.pack()
        self.supplies_info = CTkLabel(self.info, width = 90, height = 50, bg_color="black", text_color="white", text = "")
        self.supplies_info.pack()
        self.map.bind("<ButtonRelease-3>", lambda event: Menu.open_map_menu(event, self.map))
        self.map.place(x = 10, y = 30)
        self.info.place(x = 820, y = 30)



    def new_project(apk, name: str) -> None:

        apk.map = Project(name, apk)



class Application:

    current_root = None
    current_frm = None
    current_map = None
    curent_info = None

    on_widget = False
 
    def __init__(self):

        deactivate_automatic_dpi_awareness()
        set_appearance_mode("dark")

        self.root = CTk()
        self.tk = self.root
        self.root.title("CircuitSolver v. 1.1.2")
        self.root.geometry("1000x500")
        self.toplevel_window = None

        self.root.bind('<Motion>', Mouse.mouse_motion)
        self.root.bind('<Button-1>', Mouse.left_button_held)
        self.root.bind('<ButtonRelease-1>', Mouse.left_button_released)
        #self.root.wm_attributes('-transparentcolor', '#ab23ff')
        #self.frm = CTkFrame(master=self.root)

        CTkButton(self.root, width=80, height=20, text="New project", command=self.create_new_project).place(x = 10, y = 5)
        CTkButton(self.root, width=80, height=20, text="Load project", command=self.load_project, ).place(x = 100, y = 5)
        CTkButton(self.root, width=80, height=20, text="Save project", command=self.save_project, ).place(x = 190, y = 5)
        CTkButton(self.root, width=80, height=20, text="Compute", command=self.compute, ).place(x = 280, y = 5)

        Application.current_root = self

        
 
    def play(self):
        self.root.mainloop()

    def create_new_project(self):
        print("NOWY PROJEKT")
        
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()  # if window exists focus it
            #name_input = Entry(self.root, textvariable="Enter the name...").place(x=10, y=10)

        #while()

        """name_input = CTkInputDialog(title="New Project", text="Enter new project's name...")

        try:
            name = name_input.get_input()
        except TclError:
            name = None

        if name is None:
            return
        else:
            Project.new_project(self, name_input.get_input())"""


    def load_project(self):
        ...

    def save_project(self):
        ...


    def create_resistor(map, x, y):
        Resistor(map, x, y)
        Application.current_root.resistors_info.configure(text = f"Resistors: {len(Object.resistors)}")


    def create_vs(map, x, y):
        PowerSupply(map, x, y)
        Application.current_root.supplies_info.configure(text = f"Supplies: {len(Object.supplies)}")

    
    def create_branches(self):
        circuit.Branch.branches = circuit.Branch.create_branches()
        

    def compute(self):
        branches = circuit.Branch.create_branches()
        nodal_analysis(branches)

    
    def cursor_over_widget():
        Application.on_widget = True

    def cursor_not_over_widget():
        Application.on_widget = False

    

#   Custom images

        #   Reisitor
    
 
if __name__ == '__main__':
    app = Application()
    app.play()