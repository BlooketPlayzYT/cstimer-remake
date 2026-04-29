import random
import pygame
import csv
import pandas as pd
from pygame_gui import UIManager
from pygame_gui.elements import UIScrollingContainer, UILabel
import os
pygame.init()

def generate_csv():
    if not os.path.exists("solves.csv"):
        with open("solves.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["time"]) 
def append_data(arr):
   with open('solves.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    column_data = [row[0] for row in reader]
   for value in column_data:
      arr.append(value)
labels = []
def update_scrollbar():
    global labels

    for label in labels:
        label.kill()
    labels.clear()

    y = 0
    for time in data:
        label = UILabel(
            pygame.Rect((0,y),(200,30)),
            f"{time}",
            manager=manager,
            container=scroll_container
            )
        labels.append(label)
        y+=50
def record_solve():
    global data
    
    if not trigger_timer:
        with open("solves.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([f"{cube_time:.2f}"])
    data.clear()
    append_data(data)
    update_scrollbar()

clock = pygame.time.Clock()
Width = 1280
Height = 720
fps = 240
realscreen = pygame.display.set_mode((Width, Height))

white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
black = [0, 0, 0]

scramble_font = pygame.font.SysFont("comic sans", 30, bold=False)
timer_font = pygame.font.SysFont("comic sans", 80, bold=True)
timer_color = white
scramble_color = white
bg_color = black

scramble = ""
cube_time = 0.00
trigger_timer = False
trigger_wait = False
ready_to_start = False
hold_time = 0.00

data = []


#scroll bar
FILL_COLOR = (255,0,0) 
WINDOW_SIZE = (200,Height)
manager = UIManager(WINDOW_SIZE)
background = pygame.Surface(WINDOW_SIZE)
background.fill(FILL_COLOR)

scroll_container = UIScrollingContainer(
    pygame.Rect(0, 0, 200, Height),
    manager,
    should_grow_automatically=True
)
generate_csv()
append_data(data)
update_scrollbar()

def main(fakescreen):
    global scramble_font, timer_font, trigger_timer, trigger_wait, ready_to_start, cube_time, timer_color, hold_time, scramble
    clock = pygame.time.Clock()

    running = True    
    scramble = generate_scramble()

    
    while running:
        time_delta = clock.tick(fps)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if trigger_timer:
                    timer_color = red
                    trigger_timer = False
                    scramble = generate_scramble()
                    ready_to_start = False
                    record_solve()
                    ao5()
                else:
                    if event.key == pygame.K_SPACE:
                        trigger_wait = True
                        cube_time = 0.00
                        hold_time = 0.00

            if event.type == pygame.KEYUP:
                if not ready_to_start:
                    timer_color = white
                if event.key == pygame.K_SPACE:
                    trigger_wait = False
                    timer_color = white
                    hold_time = 0.00

                    if ready_to_start:
                        timer_color = white
                        trigger_timer = True
                        ready_to_start = False
            manager.process_events(event)
        
        timer_wait()
        timer()
        display(fakescreen,time_delta)
    pygame.quit()

def timer_wait():
    global trigger_wait, timer_start, timer_color, ready_to_start, hold_time
    if trigger_wait:
        hold_time += 1/fps
        timer_color = red
    if hold_time > 0.4:
        trigger_wait = False
        timer_color = green
        ready_to_start = True

def timer():
    global cube_time, trigger_timer
    if trigger_timer == True:
        cube_time += 1/fps

def ao5():
    last_5 = pd.read_csv("solves.csv").iloc[-5:, 0].astype(float).tolist()
    print(last_5)

        

def generate_scramble():
    faces = ["U", "D", "F", "B", "R", "L"]
    state = ["", "'", "2"]
    scramble = []
    for i in range(20):
        while True:
            choice = random.choice(faces)
            if i == 0:
                break
            if choice not in scramble[-1]:
                break
        scramble.append(choice + random.choice(state))
    return " ".join(scramble)

def display_time(fakescreen):
    displayed_time = timer_font.render(f"{cube_time:.2f}", True, timer_color)
    fakescreen.blit(displayed_time, (Width/2-80, Height/2-80))

def display_scramble(fakescreen):
    global trigger_timer
    if not trigger_timer:
        displayed_scramble = scramble_font.render(scramble, True, scramble_color)
        fakescreen.blit(displayed_scramble, (230, 0))

def display_scrollbar(fakescreen,manager,time_delta):
    manager.update(time_delta)
    fakescreen.blit(background, (0, 0))
    manager.draw_ui(fakescreen)

def display(fakescreen, time_delta):    
    fakescreen.fill(black)
    display_time(fakescreen)
    display_scramble(fakescreen)
    display_scrollbar(fakescreen,manager, time_delta)
    pygame.display.flip()
if __name__ == "__main__":
    main(realscreen)
