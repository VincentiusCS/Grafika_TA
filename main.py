import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from objek2d import UShape2D, Leaf2D, FanShape2D
from objek3d import Talenan3D, BotolBir3D, Guci3D
from ui_handler import process_input

def main():
    pygame.init()
    screen_size = (800, 600)
    pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Grafika Komputer")

    # Setup projection & view
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, screen_size[0]/screen_size[1], 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -10)

    ushape = UShape2D()
    leaf = Leaf2D()
    fan = FanShape2D()
    talenan = Talenan3D()
    botol = BotolBir3D()
    guci = Guci3D()

    current_object = "ushape"  # Default object to draw
    clock = pygame.time.Clock()
    running = True

    mouse_down = False
    last_mouse_pos = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_object = "ushape"
                elif event.key == pygame.K_2:
                    current_object = "leaf"
                elif event.key == pygame.K_3:
                    current_object = "fan"
                elif event.key == pygame.K_4:
                    current_object = "talenan"
                elif event.key == pygame.K_5:
                    current_object = "botol"
                elif event.key == pygame.K_6:
                    current_object = "guci"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_down = True
                    last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
                    last_mouse_pos = None
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                x, y = pygame.mouse.get_pos()
                if last_mouse_pos is not None:
                    dx = x - last_mouse_pos[0]
                    dy = y - last_mouse_pos[1]
                    if current_object == "talenan":
                        talenan.rotate(dy, dx)
                    elif current_object == "botol":
                        botol.rotate(dy, dx)
                    elif current_object == "guci":
                        guci.rotate(dy, dx)
                    elif current_object == "ushape":
                        ushape.rotate(dx)
                    elif current_object == "leaf":
                        leaf.rotate(dx)
                    elif current_object == "fan":
                        fan.rotate(dx)
                last_mouse_pos = (x, y)

            # Panggil process_input untuk objek yang aktif
            if current_object == "ushape":
                process_input(event, ushape, None)
            elif current_object == "leaf":
                process_input(event, leaf, None)
            elif current_object == "fan":
                process_input(event, fan, None)
            elif current_object == "talenan":
                process_input(event, None, talenan)
            elif current_object == "botol":
                process_input(event, None, botol)
            elif current_object == "guci":
                process_input(event, None, guci)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Gambar objek berdasarkan pilihan
        if current_object == "ushape":
            ushape.draw()
        elif current_object == "leaf":
            leaf.draw()
        elif current_object == "fan":
            fan.draw()
        elif current_object == "talenan":
            talenan.draw()
        elif current_object == "botol":
            botol.draw()
        elif current_object == "guci":
            guci.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
