from pico2d import *
import game_framework
import math
import random
mx, my = 0, 0
ui, hero = None, None
camX = 0
isClicked = False
isRightClicked = False
current_time = 0






def enter():
    global ui, hero, current_time
    ui = UI()
    hero = Hero()
    current_time = get_time()
    pass

def exit():
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    global mx, my, isClicked, isRightClicked
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, 599 - event.y
            print(mx, my)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == 1:
                isClicked = True
            elif event.button == 3:
                isRightClicked = True
        elif event.type == SDL_MOUSEBUTTONUP:
            print(event.button)
            if event.button == 3:
                isRightClicked = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                isClicked = True
            elif event.key == SDLK_RETURN:
                isRightClicked = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RETURN:
                isRightClicked = False

def update():
    global hero, current_time

    frame_time = get_time() - current_time
    current_time += frame_time

    hero.update(frame_time)

def draw():
    global ui, hero
    clear_canvas()
    ui.draw()
    hero.draw()
    update_canvas()
