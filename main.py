import pygame
import sys, math

# variables
SCREEN_WIDTH = 860
SCREEN_HEIGHT = 600
ATOM_SIZE = 9
ATOM_OUTLINE_SIZE = 13
BOND_LENGTH = 64
BUTTON_SIZE = 24
COLOR_BLUE = "#004df2"
COLOR_RED = "#f20000"
COLOR_YELLOW = "#4287f5"
COLOR_WHITE = "#ffffff"
COLOR_BLACK = "#000000"
COLOR_LIGHT_GRAY = "#8c8c8c"
COLOR_DARK_GRAY = "#6b6b6b"

atoms = []
positions = []
bonds = []
menu = False

# initialization
pygame.init()
pygame.font.init()
font_menu = pygame.font.SysFont(pygame.font.get_default_font(), 36)
font_molecule = pygame.font.SysFont(pygame.font.get_default_font(), 32)
font_chiral = pygame.font.SysFont(pygame.font.get_default_font(), 26)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Molecule Builder")
screen.fill(COLOR_WHITE)
pygame.display.update()

# images
draw_icon = pygame.image.load('draw-icon.png')
select_icon = pygame.image.load('select-icon.png')
erasor_icon = pygame.image.load('erasor-icon.png')
single_icon = pygame.image.load('single-icon.png')
double_icon = pygame.image.load('double-icon.png')
wedge_icon = pygame.image.load('wedge-icon.png')
dash_icon = pygame.image.load('dash-icon.png')
refresh_icon = pygame.image.load('refresh-icon.png')

# objects
class Atom:
  def __init__(self, element, x, y):
      self.element = element
      self.x = x
      self.y = y
      self.size = ATOM_SIZE
      self.osize = ATOM_OUTLINE_SIZE
      self.highlighted = False
      self.chiral = False
  def draw(self, draw_circle):
      if self.highlighted:
        pygame.draw.circle(screen, COLOR_YELLOW, (self.x, self.y), self.size)
      elif self.element == "n":
        pygame.draw.circle(screen, COLOR_WHITE, (self.x, self.y), self.osize)
        text_surface = font_molecule.render('N', True, COLOR_BLUE)
        screen.blit(text_surface, dest=(self.x-self.size, self.y-self.size))
      elif self.element == "o":
        pygame.draw.circle(screen, COLOR_WHITE, (self.x, self.y), self.osize)
        text_surface = font_molecule.render('O', True, COLOR_RED)
        screen.blit(text_surface, dest=(self.x-self.size, self.y-self.size))
      elif self.element == "h":
        pygame.draw.circle(screen, COLOR_WHITE, (self.x, self.y), self.osize)
        text_surface = font_molecule.render('H', True, COLOR_DARK_GRAY)
        screen.blit(text_surface, dest=(self.x-self.size, self.y-self.size))
      elif self.element == "r":
        pygame.draw.circle(screen, COLOR_WHITE, (self.x, self.y), self.osize)
        text_surface = font_molecule.render('R', True, COLOR_BLACK)
        screen.blit(text_surface, dest=(self.x-self.size, self.y-self.size))
      elif draw_circle:
        pygame.draw.circle(screen, COLOR_BLACK, (self.x, self.y), self.size)
  def drawChiral(self, configuration):
    if self.chiral and configuration:
        text_surface = font_chiral.render(configuration, True, COLOR_RED)
        screen.blit(text_surface, dest=(self.x-self.size, self.y-self.size - (ATOM_SIZE*2)))
  def clicked(self, pos):
      if pos[0] > (self.x - (self.size)) and pos[0] < (self.x + (self.size)):
              if pos[1] > (self.y - (self.size)) and pos[1] < (self.y + (self.size)):
                  return True
              else:
                  return False
      else:
          return False

class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.size = ATOM_SIZE
    self.color = COLOR_LIGHT_GRAY
    self.highlighted = False
  def draw(self):
    if self.highlighted:
      pygame.draw.circle(screen, COLOR_YELLOW, (self.x, self.y), self.size)
    else:
      pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
  def clicked(self, pos):
      if pos[0] > (self.x - (self.size)) and pos[0] < (self.x + (self.size)):
              if pos[1] > (self.y - (self.size)) and pos[1] < (self.y + (self.size)):
                  return True
              else:
                  return False
      else:
          return False

class Bond:
  def __init__(self, origin, destination, bondtype):
    self.origin = origin
    self.destination = destination
    self.bondtype = bondtype
    self.color = COLOR_BLACK
    self.thickness = 3
  def draw(self):
    if self.bondtype == "double":
      if self.origin[0] == self.destination[0]:
        origin1 = (self.origin[0] - self.thickness, self.origin[1])
        destination1 = (self.destination[0] - self.thickness, self.destination[1])
        origin2 = (self.origin[0] + self.thickness, self.origin[1])
        destination2 = (self.destination[0] + self.thickness, self.destination[1])
      else:
        origin1 = (self.origin[0], self.origin[1] - self.thickness)
        destination1 = (self.destination[0], self.destination[1] - self.thickness)
        origin2 = (self.origin[0], self.origin[1] + self.thickness)
        destination2 = (self.destination[0], self.destination[1] + self.thickness)
      pygame.draw.line(screen, self.color, origin1, destination1, self.thickness)
      pygame.draw.line(screen, self.color, origin2, destination2, self.thickness)
    elif self.bondtype == "wedge":
      if self.origin[0] == self.destination[0]:
        destination1 = (self.destination[0] - ATOM_SIZE, self.destination[1])
        destination2 = (self.destination[0] + ATOM_SIZE, self.destination[1])
      else:
        destination1 = (self.destination[0], self.destination[1] - ATOM_SIZE)
        destination2 = (self.destination[0], self.destination[1] + ATOM_SIZE)
      pygame.draw.polygon(screen, COLOR_BLACK, (self.origin, destination1, destination2))
    elif self.bondtype == "dash":
      if self.origin[0] == self.destination[0]:
        destination1 = (self.destination[0] - ATOM_SIZE, self.destination[1])
        destination2 = (self.destination[0] + ATOM_SIZE, self.destination[1])
      else:
        destination1 = (self.destination[0], self.destination[1] - ATOM_SIZE)
        destination2 = (self.destination[0], self.destination[1] + ATOM_SIZE)
      pygame.draw.line(screen, self.color, self.origin, destination1, self.thickness)
      pygame.draw.line(screen, self.color, self.origin, destination2, self.thickness)
      pygame.draw.line(screen, self.color, destination1, destination2, self.thickness)
    else:
      pygame.draw.line(screen, self.color, self.origin, self.destination, self.thickness)

class Menu:
  def __init__(self):
    self.width = 650
    self.height = 50
    self.x = (SCREEN_WIDTH/2) - (self.width/2)
    self.y = SCREEN_HEIGHT - self.height - 50
    self.border = 2
    self.buttons = []
    self.BUTTON_DRAW = True
    self.BUTTON_SELECT = False
    self.BUTTON_ERASE = False
    self.BUTTON_SINGLE = True
    self.BUTTON_DOUBLE = False
    self.BUTTON_WEDGE = False
    self.BUTTON_DASH = False
    self.BUTTON_CARBON = True
    self.BUTTON_NITROGEN = False
    self.BUTTON_OXYGEN = False
    self.BUTTON_HYDROGEN = False
    self.BUTTON_RADICAL = False
    # add buttons
    self.buttons.append(MenuButton("draw", True, self.x + (BUTTON_SIZE*2), self.y + (self.height/2)))
    self.buttons.append(MenuButton("select", False, self.x + (BUTTON_SIZE*4), self.y + (self.height/2)))
    self.buttons.append(MenuButton("erase", False, self.x + (BUTTON_SIZE*6), self.y + (self.height/2)))
    self.buttons.append(MenuButton("single", True, self.x + (BUTTON_SIZE*9), self.y + (self.height/2)))
    self.buttons.append(MenuButton("double", False, self.x + (BUTTON_SIZE*11), self.y + (self.height/2)))
    self.buttons.append(MenuButton("wedge", False, self.x + (BUTTON_SIZE*13), self.y + (self.height/2)))
    self.buttons.append(MenuButton("dash", False, self.x + (BUTTON_SIZE*15), self.y + (self.height/2)))
    self.buttons.append(MenuButton("carbon", True, self.x + (BUTTON_SIZE*18), self.y + (self.height/2)))
    self.buttons.append(MenuButton("nitrogen", False, self.x + (BUTTON_SIZE*20), self.y + (self.height/2)))
    self.buttons.append(MenuButton("oxygen", False, self.x + (BUTTON_SIZE*22), self.y + (self.height/2)))
    self.buttons.append(MenuButton("hydrogen", False, self.x + (BUTTON_SIZE*24), self.y + (self.height/2)))
    self.buttons.append(MenuButton("radical", False, self.x + (BUTTON_SIZE*26), self.y + (self.height/2)))
  def draw(self):
    pygame.draw.rect(screen, COLOR_BLACK, (self.x - (self.border), self.y - (self.border), self.width + (self.border*2), self.height + (self.border*2)))
    pygame.draw.rect(screen, COLOR_WHITE, (self.x, self.y, self.width, self.height))
    for i in range(len(self.buttons)):
      self.buttons[i].draw()
  def clicked(self, pos):
    if pos[0] > self.x and pos[0] < (self.x + (self.width)):
      if pos[1] > self.y and pos[1] < (self.y + (self.height)):
        return True
      else:
        return False
    else:
      return False
  def click(self, pos):
    for i in range(len(self.buttons)):
      if self.buttons[i].clicked(pos):
        if self.buttons[i].function == "draw":
          self.BUTTON_DRAW = True
          self.BUTTON_SELECT = False
          self.BUTTON_ERASE = False
          self.buttons[0].highlighted = True
          self.buttons[1].highlighted = False
          self.buttons[2].highlighted = False
        elif self.buttons[i].function == "select":
          self.BUTTON_DRAW = False
          self.BUTTON_SELECT = True
          self.BUTTON_ERASE = False
          self.buttons[0].highlighted = False
          self.buttons[1].highlighted = True
          self.buttons[2].highlighted = False
        elif self.buttons[i].function == "erase":
          self.BUTTON_DRAW = False
          self.BUTTON_SELECT = False
          self.BUTTON_ERASE = True
          self.buttons[0].highlighted = False
          self.buttons[1].highlighted = False
          self.buttons[2].highlighted = True
        elif self.buttons[i].function == "single":
          self.BUTTON_SINGLE = True
          self.BUTTON_DOUBLE = False
          self.BUTTON_WEDGE = False
          self.BUTTON_DASH = False
          self.buttons[3].highlighted = True
          self.buttons[4].highlighted = False
          self.buttons[5].highlighted = False
          self.buttons[6].highlighted = False
        elif self.buttons[i].function == "double":
          self.BUTTON_SINGLE = False
          self.BUTTON_DOUBLE = True
          self.BUTTON_WEDGE = False
          self.BUTTON_DASH = False
          self.buttons[3].highlighted = False
          self.buttons[4].highlighted = True
          self.buttons[5].highlighted = False
          self.buttons[6].highlighted = False
        elif self.buttons[i].function == "wedge":
          self.BUTTON_SINGLE = False
          self.BUTTON_DOUBLE = False
          self.BUTTON_WEDGE = True
          self.BUTTON_DASH = False
          self.buttons[3].highlighted = False
          self.buttons[4].highlighted = False
          self.buttons[5].highlighted = True
          self.buttons[6].highlighted = False
        elif self.buttons[i].function == "dash":
          self.BUTTON_SINGLE = False
          self.BUTTON_DOUBLE = False
          self.BUTTON_WEDGE = False
          self.BUTTON_DASH = True
          self.buttons[3].highlighted = False
          self.buttons[4].highlighted = False
          self.buttons[5].highlighted = False
          self.buttons[6].highlighted = True
        elif self.buttons[i].function == "carbon":
          self.BUTTON_CARBON = True
          self.BUTTON_NITROGEN = False
          self.BUTTON_OXYGEN = False
          self.BUTTON_HYDROGEN = False
          self.BUTTON_RADICAL = False
          self.buttons[7].highlighted = True
          self.buttons[8].highlighted = False
          self.buttons[9].highlighted = False
          self.buttons[10].highlighted = False
          self.buttons[11].highlighted = False
        elif self.buttons[i].function == "nitrogen":
          self.BUTTON_CARBON = False
          self.BUTTON_NITROGEN = True
          self.BUTTON_OXYGEN = False
          self.BUTTON_HYDROGEN = False
          self.BUTTON_RADICAL = False
          self.buttons[7].highlighted = False
          self.buttons[8].highlighted = True
          self.buttons[9].highlighted = False
          self.buttons[10].highlighted = False
          self.buttons[11].highlighted = False
        elif self.buttons[i].function == "oxygen":
          self.BUTTON_CARBON = False
          self.BUTTON_NITROGEN = False
          self.BUTTON_OXYGEN = True
          self.BUTTON_HYDROGEN = False
          self.BUTTON_RADICAL = False
          self.buttons[7].highlighted = False
          self.buttons[8].highlighted = False
          self.buttons[9].highlighted = True
          self.buttons[10].highlighted = False
          self.buttons[11].highlighted = False
        elif self.buttons[i].function == "hydrogen":
          self.BUTTON_CARBON = False
          self.BUTTON_NITROGEN = False
          self.BUTTON_OXYGEN = False
          self.BUTTON_HYDROGEN = True
          self.BUTTON_RADICAL = False
          self.buttons[7].highlighted = False
          self.buttons[8].highlighted = False
          self.buttons[9].highlighted = False
          self.buttons[10].highlighted = True
          self.buttons[11].highlighted = False
        elif self.buttons[i].function == "radical":
          self.BUTTON_CARBON = False
          self.BUTTON_NITROGEN = False
          self.BUTTON_OXYGEN = False
          self.BUTTON_HYDROGEN = False
          self.BUTTON_RADICAL = True
          self.buttons[7].highlighted = False
          self.buttons[8].highlighted = False
          self.buttons[9].highlighted = False
          self.buttons[10].highlighted = False
          self.buttons[11].highlighted = True

class MenuButton:
  def __init__(self, function, active, x, y):
    self.function = function
    self.x = x - (BUTTON_SIZE/2)
    self.y = y - (BUTTON_SIZE/2)
    self.width = BUTTON_SIZE
    self.height = BUTTON_SIZE
    self.color = COLOR_BLACK
    self.highlighted = active
  def draw(self):
    # draw yellow box if highlighted
    if self.highlighted:
        pygame.draw.rect(screen, COLOR_YELLOW, (self.x, self.y, self.width, self.height))
    # draw atomic symbol if element button
    if self.function == "carbon":
      text_surface = font_menu.render('C', True, COLOR_BLACK)
      screen.blit(text_surface, dest=(self.x+1, self.y+1))
    elif self.function == "nitrogen":
      text_surface = font_menu.render('N', True, COLOR_BLUE)
      screen.blit(text_surface, dest=(self.x+1, self.y+1))
    elif self.function == "oxygen":
      text_surface = font_menu.render('O', True, COLOR_RED)
      screen.blit(text_surface, dest=(self.x+1, self.y+1))
    elif self.function == "hydrogen":
      text_surface = font_menu.render('H', True, COLOR_DARK_GRAY)
      screen.blit(text_surface, dest=(self.x+1, self.y+1))
    elif self.function == "radical":
      text_surface = font_menu.render('R', True, COLOR_BLACK)
      screen.blit(text_surface, dest=(self.x+1, self.y+1))
    # draw icon
    elif self.function == "draw":
      screen.blit(draw_icon, (self.x, self.y))
    elif self.function == "select":
      screen.blit(select_icon, (self.x, self.y))
    elif self.function == "erase":
      screen.blit(erasor_icon, (self.x, self.y))
    elif self.function == "single":
      screen.blit(single_icon, (self.x, self.y))
    elif self.function == "double":
      screen.blit(double_icon, (self.x, self.y))
    elif self.function == "wedge":
      screen.blit(wedge_icon, (self.x, self.y))
    elif self.function == "dash":
      screen.blit(dash_icon, (self.x, self.y))
    # black box for anything else
    elif not self.highlighted:
      pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
  def clicked(self, pos):
    if pos[0] > self.x and pos[0] < (self.x + (self.width)):
      if pos[1] > self.y and pos[1] < (self.y + (self.height)):
        return True
      else:
        return False
    else:
      return False

class RefreshButton:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.width = BUTTON_SIZE
    self.height = BUTTON_SIZE
  def draw(self):
    screen.blit(refresh_icon, (self.x, self.y))
    pygame.display.update()
  def clicked(self, pos):
    if pos[0] > self.x and pos[0] < (self.x + (self.width)):
      if pos[1] > self.y and pos[1] < (self.y + (self.height)):
        return True
      else:
        return False
    else:
      return False

# functions
def getAdjoiningAtom(atom, bond):
  # adjoining atom is at destination
  if atom.x == bond.origin[0] and atom.y == bond.origin[1]:
    targetx = bond.destination[0]
    targety = bond.destination[1]
  # adjoining atom is at origin
  elif atom.x == bond.destination[0] and atom.y == bond.destination[1]:
    targetx = bond.origin[0]
    targety = bond.origin[1]
  else:
    return False
  for i in range(len(atoms)):
    if targetx == atoms[i].x and targety == atoms[i].y:
      return atoms[i]

def getRank(element):
  # 0 will mean there is nothing there, ignore it
  if element == "h":
    return 1
  elif element == "c":
    return 2
  elif element == "n":
    return 3
  elif element == "o":
    return 4
  else:
    return 0

def getAtomByPosition(pos):
  for i in range(len(atoms)):
    condition1 = pos[0] > atoms[i].x - ATOM_SIZE and pos[0] < atoms[i].x + ATOM_SIZE
    condition2 = pos[1] > atoms[i].y - ATOM_SIZE and pos[1] < atoms[i].y + ATOM_SIZE
    if condition1 and condition2:
      return atoms[i]
  return False

def getBondBetween(atom1, atom2):
  for i in range(len(bonds)):
    # condition 1 - atom1 has to be at origin or destination
    if atom1.x == bonds[i].origin[0] and atom1.y == bonds[i].origin[1]:
      # condition 2 - atom2 has to be at opposite end
      if atom2.x == bonds[i].destination[0] and atom2.y == bonds[i].destination[1]:
        return bonds[i]
    if atom1.x == bonds[i].destination[0] and atom1.y == bonds[i].destination[1]:
      # condition 2 - atom2 has to be at opposite end
      if atom2.x == bonds[i].origin[0] and atom2.y == bonds[i].origin[1]:
        return bonds[i]
  return False

def getChiralConfiguration(atom):
  # make sure chiral
  if not atom.chiral:
    return False
  # get connected atoms clockwise from top position
  # check to make sure each one is connected
  p_top = (atom.x, atom.y - BOND_LENGTH)
  p_tright = (atom.x + BOND_LENGTH, atom.y - (BOND_LENGTH/2))
  p_bright = (atom.x + BOND_LENGTH, atom.y + (BOND_LENGTH/2))
  p_bottom = (atom.x, atom.y + BOND_LENGTH)
  p_bleft = (atom.x - BOND_LENGTH, atom.y + (BOND_LENGTH/2))
  p_tleft = (atom.x - BOND_LENGTH, atom.y - (BOND_LENGTH/2))
  # array will hold atoms
  # indexes: 0 = top, 1 = top-right, 2 = bottom-right, 4 = bottom
  #           5 = bottom-left, 6 = top-left (clockwise direction)
  r_groups = []
  r_groups.append(getAtomByPosition(p_top))
  r_groups.append(getAtomByPosition(p_tright))
  r_groups.append(getAtomByPosition(p_bright))
  r_groups.append(getAtomByPosition(p_bottom))
  r_groups.append(getAtomByPosition(p_bleft))
  r_groups.append(getAtomByPosition(p_tleft))
  # in a parallel array, get the bond types for each group
  r_bonds = []
  for i in range(len(r_groups)):
    if r_groups[i]:
      r_bonds.append(getBondBetween(atom, r_groups[i]))
    else:
      r_bonds.append(False)
  # trim the onoccupied positions
  for i in reversed(range(len(r_groups))):
    if not r_groups[i]:
      r_groups.pop(i)
  for i in reversed(range(len(r_bonds))):
    if not r_bonds[i]:
      r_bonds.pop(i)
  # get the ranks for each group
  for i in range(len(r_groups)):
    r_groups[i] = getRank(r_groups[i].element)
  # swap the lowest ranking group to the dash
  # (this will invert the R/S configuration)
  # (so when the R/S configuration is determined later, the real
  # (configuration will be the opposite)
  lowest_value = 100
  lowest_index = 0
  for i in range(len(r_groups)):
    if r_groups[i] < lowest_value:
      lowest_value = r_groups[i]
      lowest_index = i
  dash_index = 0
  for i in range(len(r_bonds)):
    if r_bonds[i].bondtype == "dash":
      dash_index = i
  swap = False
  if lowest_index != dash_index:
    swap = True
    # swap lowest value with whatever is at the dash index
    temp = r_groups[lowest_index]
    r_groups[lowest_index] = r_groups[dash_index]
    r_groups[dash_index] = temp
  # remove lowest index from array
  r_groups.pop(dash_index)
  r_bonds.pop(dash_index)
  # figure out direction of increase in array
  # if increase is from left to right - clockwise (R configuration)
  #   - this means that the original is S configuration
  # if increase is from right to left - counterclockwise (S configuration)
  #   - this means that the original is R configuration
  increases = 0
  decreases = 0
  if r_groups[1] > r_groups[0]:
    increases += 1
  else:
    decreases += 1
  if r_groups[2] > r_groups[1]:
    increases += 1
  else:
    decreases += 1
  if r_groups[0] > r_groups[2]:
    increases += 1
  else:
    decreases += 1
  # if there are more increases than decreases, the configuration is R (S originally)
  if increases > decreases:
    if swap:
      return "R"
    else:
      return "S"
  else:
    if swap:
      return "S"
    else:
      return "R"

def checkChirality():
  for i in range(len(atoms)):
    if isChiral(atoms[i]):
      atoms[i].chiral = True
      atoms[i].drawChiral(getChiralConfiguration(atoms[i]))
    else:
      atoms[i].chiral = False

def isChiral(atom):
  # element must be carbon (for now)
  if atom.element != "c":
    return False
  # element must have 4 bonds
  bond_types = []
  for i in range(len(bonds)):
      condition1 = bonds[i].origin[0] == atom.x and bonds[i].origin[1] == atom.y
      condition2 = bonds[i].destination[0] == atom.x and bonds[i].destination[1] == atom.y
      if condition1 or condition2:
        bond_types.append(bonds[i].bondtype)
  if len(bond_types) != 4:
    return False
  # check that no bonds are double bonds
  for i in range(len(bond_types)):
    if bond_types[i] == "double":
      return False
  # check that there is only 1 wedge and 1 dash
  wedges = 0
  dashes = 0
  for i in range(len(bond_types)):
    if bond_types[i] == "wedge":
      wedges += 1
    elif bond_types[i] == "dash":
      dashes += 1
  if wedges != 1 or dashes != 1:
    return False
  # get the 4 atoms joining
  adj_atoms = []
  for i in range(len(bonds)):
      condition1 = bonds[i].origin[0] == atom.x and bonds[i].origin[1] == atom.y
      condition2 = bonds[i].destination[0] == atom.x and bonds[i].destination[1] == atom.y
      if condition1 or condition2:
        adj_atoms.append(getAdjoiningAtom(atom, bonds[i]))
  # none of the 4 bonded groups can be an R
  for i in range(len(adj_atoms)):
    if adj_atoms[i].element == 'r':
      return False
  # 4 bonded groups must be different
  for i in range(len(adj_atoms)):
    for j in range(len(adj_atoms)):
      if i != j:
        if adj_atoms[i].element == adj_atoms[j].element:
          return False
  return True

def redraw(draw_button):
  screen.fill(COLOR_WHITE)
  for i in range(len(bonds)):
    bonds[i].draw()
  for i in range(len(positions)):
    positions[i].draw()
  for i in range(len(atoms)):
    atoms[i].draw(draw_button)
  if menu:
    menu.draw()
  checkChirality()
  refresh.draw()
  pygame.display.update()

def addPositions(atom):
  p_top = Position(atom.x, atom.y - BOND_LENGTH)
  p_bottom = Position(atom.x, atom.y + BOND_LENGTH)
  p_tleft = Position(atom.x - BOND_LENGTH, atom.y - (BOND_LENGTH/2))
  p_bleft = Position(atom.x - BOND_LENGTH, atom.y + (BOND_LENGTH/2))
  p_tright = Position(atom.x + BOND_LENGTH, atom.y - (BOND_LENGTH/2))
  p_bright = Position(atom.x + BOND_LENGTH, atom.y + (BOND_LENGTH/2))
  positions.append(p_top)
  positions.append(p_bottom)
  positions.append(p_tleft)
  positions.append(p_bleft)
  positions.append(p_tright)
  positions.append(p_bright)

def removePositions():
  positions.clear()

def refreshPage():
  positions.clear()
  atoms.clear()
  bonds.clear()
  atom = Atom("c", (SCREEN_WIDTH/2) - (ATOM_SIZE/2), (SCREEN_HEIGHT/2) - (ATOM_SIZE/2) - 50)
  atoms.append(atom)
  atom.draw(True)

def removeAtom(atom):
  for i in reversed(range(len(atoms))):
    if atoms[i].x == atom.x and atoms[i].y == atom.y:
      atoms.pop(i)
  for i in reversed(range(len(bonds))):
    condition1 = atom.x == bonds[i].origin[0] and atom.y == bonds[i].origin[1]
    condition2 = atom.x == bonds[i].destination[0] and atom.y == bonds[i].destination[1]
    if condition1 or condition2:
      bonds.pop(i)

def addBond(origin, destination, bondtype, newatom, element):
  if newatom:
    # check if there is already an atom
    for i in reversed(range(len(atoms))):
      if atoms[i].x == destination[0] and atoms[i].y == destination[1]:
        atoms.pop(i)
    atoms.append(Atom(element, destination[0], destination[1]))
  # check if there is another bond
  for i in reversed(range(len(bonds))):
    condition1 = destination[0] == bonds[i].destination[0] and destination[1] == bonds[i].destination[1]
    condition2 = origin[0] == bonds[i].origin[0] and origin[1] == bonds[i].origin[1]
    condition3 = destination[0] == bonds[i].origin[0] and destination[1] == bonds[i].origin[1]
    condition4 = origin[0] == bonds[i].destination[0] and origin[1] == bonds[i].destination[1]
    if (condition1 and condition2) or (condition3 and condition4):
      bonds.pop(i)
  bonds.append(Bond(origin, destination, bondtype))

# game loop
atom = Atom("c", (SCREEN_WIDTH/2) - (ATOM_SIZE/2), (SCREEN_HEIGHT/2) - (ATOM_SIZE/2) - 50)
atoms.append(atom)
atom.draw(True)
menu = Menu()
menu.draw()
refresh = RefreshButton(0, 0)
refresh.draw()

drawline = False
lineorigin = (0,0)

run = True
while run:
    pygame.time.delay(25)

    if drawline:
      pygame.draw.line(screen, COLOR_BLACK, lineorigin, pygame.mouse.get_pos(), 3)
      # highlight positions if mouse hovers over
      pos = pygame.mouse.get_pos()
      for i in range(len(positions)):
        if positions[i].clicked(pos):
          positions[i].highlighted = True
        else:
          positions[i].highlighted = False
      # DRAW
      redraw(menu.BUTTON_DRAW or menu.BUTTON_ERASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # check if click was in menu first
            if menu.clicked(pos):
              menu.click(pos)
            elif refresh.clicked(pos):
              refreshPage()
            elif menu.BUTTON_DRAW:
              for i in range(len(atoms)):
                  if atoms[i].clicked(pos):
                    if atoms[i].element != "h":
                      atoms[i].highlighted = True
                      atoms[i].draw(True)
                      drawline = True
                      lineorigin = (atoms[i].x, atoms[i].y)
                      addPositions(atoms[i])
            elif menu.BUTTON_ERASE:
              for i in range(len(atoms)):
                  if atoms[i].clicked(pos):
                    atoms[i].highlighted = True
                    atoms[i].draw(True)

            # DRAW
            redraw(menu.BUTTON_DRAW or menu.BUTTON_ERASE)
        if event.type == pygame.MOUSEBUTTONUP:
          if menu.BUTTON_ERASE:
            if len(atoms) > 1:
              pos = pygame.mouse.get_pos()
              for i in range(len(atoms)):
                if atoms[i].clicked(pos):
                  removeAtom(atoms[i])
                  break
              for i in range(len(atoms)):
                atoms[i].highlighted = False
            else:
              atoms[0].highlighted = False
          elif menu.BUTTON_DRAW and drawline:
            drawline = False
            # check if a new bond and atom needs to be created
            pos = pygame.mouse.get_pos()
            for i in range(len(positions)):
              if positions[i].clicked(pos):
                # determine atom element
                element = "c"
                if menu.BUTTON_NITROGEN:
                  element = "n"
                elif menu.BUTTON_OXYGEN:
                  element = "o"
                elif menu.BUTTON_HYDROGEN:
                  element = "h"
                elif menu.BUTTON_RADICAL:
                  element = "r"
                # determine bond type
                bondtype = "single"
                if menu.BUTTON_DOUBLE:
                  bondtype = "double"
                elif menu.BUTTON_WEDGE:
                  bondtype = "wedge"
                elif menu.BUTTON_DASH:
                  bondtype = "dash"
                addBond(lineorigin, (positions[i].x, positions[i].y), bondtype, True, element) 
            # make sure no atoms are highlighted
            for i in range(len(atoms)):
              atoms[i].highlighted = False
            removePositions()
            
          # DRAW
          redraw(menu.BUTTON_DRAW or menu.BUTTON_ERASE)

pygame.quit()















