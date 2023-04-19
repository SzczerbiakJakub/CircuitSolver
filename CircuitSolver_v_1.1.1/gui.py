# importing pygame and we can call it by using py
import tkinter as tk
 
# this is a simple App class in pygame
 
 
class App_Class:
 
    def __init__(self):
 
        # initializing the function for app
        # class to declare the changeable content
        tk.init()
        App_Class.screen = tk.display.set_mode(
            # size of window will be 540x340
            (540, 340))
        App_Class.running = True
 
    def play(self):
        pass
 
if __name__ == '__main__':
    App_Class().play()