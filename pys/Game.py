from pico2d import *

def enter(self):
    print("State [%s] Entered" % self.name)

def exit(self):
    print("State [%s] Exited" % self.name)

def pause(self):
    print("State [%s] Paused" % self.name)

def resume(self):
    print("State [%s] Resumed" % self.name)

def handle_events(self):
    print("State [%s] handle_events" % self.name)

def update(self):
    print("State [%s] update" % self.name)

def draw(self):
    print("State [%s] draw" % self.name)
