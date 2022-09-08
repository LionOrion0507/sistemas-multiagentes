from enum import Enum
import random
import agentpy as ap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import IPython
import socket


f = open("initialPos.txt", "w")
f2 = open("positionsSimul.txt", "w")
class MODEL_TYPE(Enum):
  CAR = 0
  DEPORTIVE = 1
  BUS = 2

class Vehiculo(ap.Agent):
  
  def setup(self):
    #Creamos los datos del vehiculo
    self.velocity = 0
    self.type = MODEL_TYPE(random.randint(0, 2))
    self.dir = 'initial' # up, down, left, right
    self.state = 'straight' # 0 straight, 1 crossing, 2 stopped
    
    #Declaramos la posicion del vehiculo
    self.grid = self.model.grid
    self.pos = (0, 0)
    self.counter = 0
    
  def print_data(self):
    print("\nDatos del vehiculo: ")
    print("Mass: ", self.mass, " tipo: ", self.type, " direccion: ", self.dir)
        
  def setVelocity(self):
    if self.type == 0:
      self.velocity = 2
    elif self.type == 1:
      self.velocity = 4
    else:
      self.velocity = 1
    
  def starting_position(self):                           
    spot = random.choice(self.grid.empty)
    if self.dir == 'up':
      while spot[0] >= 9 or spot[1] != 29:
        spot = random.choice(self.grid.empty)
      print(f"Up {spot}\n")
      f.write(f"{spot[0]} {spot[1]}\n")
      self.grid.move_to(self, spot)

    elif self.dir == 'down':
      while spot[0] <= 28 and spot[0] >= 40 or spot[1] != 33:
        spot = random.choice(self.grid.empty)
      print(f"Down {spot}\n")
      f.write(f"{spot[0]} {spot[1]}\n")
      self.grid.move_to(self, spot)

    elif self.dir == 'left':
      while spot[0] != 15 or spot[1] <= 33:
        spot = random.choice(self.grid.empty)
      f.write(f"{spot[0]} {spot[1]}\n")
      print(f"left {spot}\n")
      self.grid.move_to(self, spot)

    elif self.dir == 'right':
      while spot[0] != 21 or spot[1] >= 17:
        spot = random.choice(self.grid.empty)
      f.write(f"{spot[0]} {spot[1]}\n")
      print(f"Right {spot}\n")
      self.grid.move_to(self, spot)

  def move(self, car_pos):                                                                                                                      
    if self.dir == 'up':                          
      next_pos = (car_pos[0] - 1, car_pos[1])
      y = next_pos[0]     
      x = next_pos[1]     
      pos_cag = (x, y)    
      if pos_cag in self.grid.empty:
        self.grid.move_to(self, next_pos)
        self.pos = next_pos

    elif self.dir == 'down':
      next_pos = (car_pos[0] + 1, car_pos[1])
      y = next_pos[0]
      x = next_pos[1]
      pos_cag = (x, y)
      if pos_cag in self.grid.empty:
        self.grid.move_to(self, next_pos)
        self.pos = next_pos

    elif self.dir == 'left':
      next_pos = (car_pos[0], car_pos[1] - 1)
      y = next_pos[0]
      x = next_pos[1]
      pos_cag = (x, y)
      if pos_cag in self.grid.empty:
        self.grid.move_to(self, next_pos)
        self.pos = next_pos

    elif self.dir == 'right':
      next_pos = (car_pos[0], car_pos[1] + 1)
      y = next_pos[0]
      x = next_pos[1]
      pos_cag = (x, y)
      if pos_cag in self.grid.empty:
        self.grid.move_to(self, next_pos)
        self.pos = next_pos

  def turn(self):

    if self.dir == 'up':
      self.dir = 'right'

    elif self.dir == 'down':
      self.dir = 'left'

    elif self.dir == 'left':
      self.dir = 'up'

    elif self.dir == 'right':
      self.dir = 'down'

class Semaforo(ap.Agent):
  def setup(self):

    self.grid = self.model.grid
    self.state = 'switch' #switch, stay
    self.color = 'green'
    self.loc = 'none'
    self.counter = 0 

  def place_light(self, cont):
    if cont == 0:
      self.grid.move_to(self, (18, 20))
      self.loc = 'north'

    elif cont == 1:
      self.grid.move_to(self, (21, 32))
      self.loc = 'east'

    elif cont == 2:
      self.grid.move_to(self, (32, 29))
      self.loc = 'south'

    elif cont == 3:
      self.grid.move_to(self, (30, 17)) 
      self.loc = 'west'

class Interseccion(ap.Model):
  def setup(self):

    self.grid = ap.Grid(self, (50, 50), track_empty=True)                             #
    cars = self.cars = ap.AgentList(self, self.p.car_pop, Vehiculo)
    lights = self.lights = ap.AgentList(self, self.p.light_pop, Semaforo)
    self.counter = 0
    self.crossings = [] # 0 north, 1 east, 2 south, 3 west

    cont = 0

    self.grid.add_agents(lights)
    for l in lights:
      l.place_light(cont)
      self.crossings.append(l)
      cont += 1

    dirs = ['up', 'down', 'left', 'right'] 

    self.grid.add_agents(cars)
    for c in cars:
      c.dir = random.choice(dirs)
      c.starting_position()
      
    

    
  def step(self):
    turn_or_not = ['turn', 'not_turn']

    street = self.grid.positions

    n_stop = street[self.crossings[0]]
    s_stop = street[self.crossings[2]]
    e_stop = street[self.crossings[1]]
    w_stop = street[self.crossings[3]]

    n_s_empty = True
    e_w_empty = True

    for c in self.cars:
      car_pos = street[c]
      f2.write(f"{str(c)} {str(car_pos)}\n")
      #print(f"Carro No. {c} esta en pos: {car_pos}")
      if car_pos == n_stop or car_pos == s_stop:
        n_s_empty = False
      elif car_pos == e_stop or car_pos == w_stop :
        e_w_empty = False
      
      if c.state == 'straight':
        if c.dir == 'up':
          if car_pos[0] == 17:
            if self.crossings[2].color == 'green':
              choice = random.choice(turn_or_not)
              if choice == 'turn':
                c.move(car_pos)
                c.turn()
              elif choice == 'not_turn':
                c.state = 'crossing'
            elif self.crossings[2].color == 'yellow' or self.crossings[2].color == 'red':
              c.state = 'stopped'
          elif car_pos[0] > 0:
            c.move(car_pos)

        elif c.dir == 'down':
          if car_pos[0] == 14:
            if self.crossings[0].color == 'green':
              choice = random.choice(turn_or_not)
              if choice == 'turn':
                c.move(car_pos)
                c.turn()
              elif choice == 'not_turn':
                c.state = 'crossing'
            elif self.crossings[0].color == 'yellow' or self.crossings[0].color == 'red':
              c.state = 'stopped'
          if car_pos[0] <= 31:
            c.move(car_pos)

        elif c.dir == 'left':
          if car_pos[1] == 17:
            if self.crossings[1].color == 'green':
              choice = random.choice(turn_or_not)
              if choice == 'turn':
                c.move(car_pos)
                c.turn()
              elif choice == 'not_turn':
                c.state = 'crossing'
            elif self.crossings[1].color == 'yellow' or self.crossings[1].color == 'red':
              c.state = 'stopped'
          elif car_pos[1] > 0:
            c.move(car_pos)

        elif c.dir == 'right':
          if car_pos[1] == 14:
            if self.crossings[1].color == 'green':
              choice = random.choice(turn_or_not)
              if choice == 'turn':
                c.move(car_pos)
                c.turn()
              elif choice == 'not_turn':
                c.state = 'crossing'
            elif self.crossings[1].color == 'yellow' or self.crossings[1].color == 'red':
              c.state = 'stopped'
          elif car_pos[1] <= 31:
            c.move(car_pos)
          
        
        elif c.state == 'crossing':
          c.move()
        

        elif c.state == 'stopped':

          if c.dir == 'up':
            if self.crossings[2].color == 'green':
              c.state = 'straight'
          elif c.dir == 'down':
            if self.crossings[0].color == 'green':
              c.state = 'straight'
          elif c.dir == 'left':
            if self.crossings[1].color == 'green':
              c.sate = 'straight'
          elif c.dir == 'right':
            if self.crossings[3].color == 'green':
              c.state = 'straight'

      # 0 north, 1 east, 2 south, 3 west
      

      if n_s_empty == True and e_w_empty == False:
        for l in self.crossings:
          l.state = 'stay'
        self.crossings[0].color = self.crossings[2].color = 'red'
        self.crossings[1].color = self.crossings[3].color = 'green'
      elif e_w_empty == True and n_s_empty == False:
        for l in self.crossings:
          l.state = 'stay'
        self.crossings[0].color = self.crossings[2].color = 'green'
        self.crossings[1].color = self.crossings[3].color = 'red'
      else:
        for l in self.crossings:
          l.state = 'switch'
  
  
      if self.crossings[0].state == 'switch':
        if self.crossings[0].color == 'green':
          if self.counter >= 3:
            self.crossings[0].color = self.crossings[2].color = 'yellow'
          self.counter += 1
        elif self.crossings[0].color == 'yellow':
          self.crossings[0].color = self.crossings[2].color = 'red'
          self.crossings[1].color = self.crossings[3].color = 'green'
          self.counter = 0
        elif self.crossings[1].color == 'yellow':
          self.crossings[1].color = self.crossings[3].color = 'red'
          self.crossings[0].color = self.crossings[2].color = 'green'
          self.counter = 0
        elif self.crossings[0].color == 'red':
          if self.counter >= 3:
            self.crossings[1].color = self.crossings[3].color = 'yellow'
          self.counter += 1

      #print(self.crossings[0].color)

parameters = {
  'car_pop': 5,
  'light_pop': 4,
  'steps': 10,
  'size': 10
}
pd.set_option("display.max_rows", 255, "display.max_columns", 5)
model = Interseccion(parameters)

results = model.run()
f.close()
f2.close()
