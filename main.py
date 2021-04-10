import tkinter as tk
import math
import random

canvas = None
SQUARE_LENGTH = 100
RADIUS = SQUARE_LENGTH / 2 - 5
POSITION = {"x": 8, "y": 8}
BORDER_WIDTH = 8
NUMBER = 4
LENGTH = SQUARE_LENGTH * NUMBER + BORDER_WIDTH * NUMBER
CELL_COLORS = {0:'#cbbeb5', 2:'rosybrown', 4:'indianred', 8:'brown', 16:'firebrick', 32:'maroon', 64:'darkred', 128:'red', 256:'gold', 512:'orange', 1024:'darkorange', 2048:'purple'}
BORDER_COLOR = '#b2a698'
field = [[0] * NUMBER for i in range(4)]

def set_field():
  canvas.create_rectangle(POSITION["x"], POSITION["y"], LENGTH + POSITION["x"], LENGTH + POSITION["y"], fill='#cbbeb5', width=BORDER_WIDTH, outline=BORDER_COLOR)
  for i in range(NUMBER - 1):
    x = POSITION["x"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    y = POSITION["y"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    canvas.create_line(x, POSITION["y"], x, LENGTH + POSITION["y"], width=BORDER_WIDTH, fill=BORDER_COLOR)
    canvas.create_line(POSITION["x"], y, LENGTH + POSITION["x"], y, width=BORDER_WIDTH, fill=BORDER_COLOR)

def create_canvas():
  root = tk.Tk()
  root.geometry(f"""{LENGTH + POSITION["x"] * 2}x{LENGTH + POSITION["y"] * 2}""")
  root.title("2048")
  canvas = tk.Canvas(root, width=(LENGTH + POSITION["x"]), height=(LENGTH + POSITION["y"]))
  canvas.place(x=0, y=0)
  return root, canvas

def set_number(field):
  x = 0
  y = 0
  while x < NUMBER:
    while y < NUMBER:
      num = field[x][y]
      center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
      center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2
      canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill=CELL_COLORS[num], width=0)
      if field[x][y] == 0:
        canvas.create_text(center_x, center_y, justify="center", font=("", 70), tag="count_text")
      else:
        canvas.create_text(center_x, center_y, text=str(num), justify="center", font=("", 70), tag="count_text")
      y += 1
    x += 1
    y = 0
  
def operate(event):
  global field
  new_field = slide_number(field, event.keysym)
  field = new_field
  appear_number(field)
  
def gameover():
  label1 = tk.Label(text= 'Game over', fg = 'red')
  label1.place(x = LENGTH * 0.5, y= LENGTH *0.5)

def select_number(field): #NONEの座標調べ
  counter = 0
  for i in field:
    counter += i.count(0)
  if counter == 0:
    gameover()
    return
  x = random.randint(0,NUMBER - 1)
  y = random.randint(0,NUMBER - 1)
  while field[x][y]:
    x = random.randint(0,NUMBER - 1)
    y = random.randint(0,NUMBER - 1)
  return x,y

def appear_number(field):#空のますに出現させる
  x, y = select_number(field)
  numbertype = random.randint(0,10)
  number = 2 if numbertype >= 0 and numbertype <= 8 else 4
  field[x][y] = number
  set_number(field)

def delet_zero(field):
  for i in range(4):
    counter = 0 #0のマスの数count
    new_list = []
    for j in field[i]:
      if j == 0:
        counter += 1
      else:
        new_list.append(j)
    for k in range(counter):
      new_list.append(0)
    field[i] = new_list
  new_field = calculate(field) 
  return new_field

def calculate(field): #足し算
  for i in range(4):
    new_list = field[i]
    if new_list[0] == new_list[1] and new_list[2] == new_list[3]:
      new_list = [new_list[0] * 2, new_list[2] * 2, 0, 0]
    elif new_list[0] == new_list[1]:
      new_list = [new_list[0] * 2, new_list[2], new_list[3], 0]
    elif new_list[1] == new_list[2]:
      new_list = [new_list[0], new_list[1] * 2, new_list[3], 0]
    elif new_list[2] == new_list[3]:
      new_list = [new_list[0], new_list[1], new_list[2] * 2 , 0]
    field[i] = new_list
  return field 

def reverse(field):
  for i in range(NUMBER):
      field[i].reverse()

def rotate(array, is_right=True):##ぱくり
    _array = [[None for i in range(4)] for j in range(4)]
    for i in range(len(array)):
      for j in range(len(array[0])):
        if is_right:
          _array[i][len(array) - 1 - j] = array[j][i]
        else:
          _array[len(array) - 1 - i][j] = array[j][i]
    return _array

def slide_number(field,command):#0のます移動
  if command == 'Up':
    new_field = delet_zero(field)
    set_number(new_field)
    return new_field
  elif command == 'Down':
    reverse(field)
    new_field = delet_zero(field)
    reverse(new_field)
    set_number(new_field)
    return new_field
  elif command == 'Right':
    rolled = rotate(field, is_right=True)
    rolled_field = delet_zero(rolled)
    new_field = rotate(rolled_field, is_right=False)
    set_number(new_field)
    return new_field
  else:
    rolled = rotate(field, is_right=False)
    rolled_field = delet_zero(rolled)
    new_field = rotate(rolled_field, is_right=True)
    set_number(new_field)
    return new_field

def play():
  global canvas
  root, canvas = create_canvas()
  set_field()
  appear_number(field)
  root.bind("<Key>", lambda event: operate(event))
  root.mainloop()

play()
