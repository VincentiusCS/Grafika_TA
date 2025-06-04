import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objek2d import UShape2D, Leaf2D, FanShape2D
from objek3d import Talenan3D, BotolBir3D, Guci3D
import copy
import threading
import tkinter as tk

# Helper untuk objek default
def default_object(obj_type):
    base_colors = {
        "ushape":  {"fill": (0.66, 0.66, 0.66), "border": (0, 0, 0)},
        "leaf":    {"fill": (0.0, 0.8, 0.0), "border": (0, 0.4, 0)},
        "fan":     {"fill": (1.0, 0.0, 0.0), "border": (0.0, 0.0, 0.0)},
        "talenan": {"fill": (0.85, 0.7, 0.4), "border": (0.3, 0.23, 0.11)},
        "botol":   {"fill": (0.6, 0.3, 0.1), "border": (0.5, 0.25, 0.1)},
        "guci":    {
            "fill": (0.53, 0.42, 0.22),
            "border": (0.35, 0.25, 0.13),
            "top": (0.48, 0.37, 0.17),
            "bottom": (0.35, 0.22, 0.11)
        }
    }
    return {
        "type": obj_type,
        "pos": [0.0, 0.0, 0.0],
        "scale": 1.0,
        "rotation": [0.0, 0.0],
        "colors": copy.deepcopy(base_colors[obj_type])
    }

# OpenGL rendering window, menerima state dengan banyak objek
def run_opengl_window(current_state):
    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL Viewer")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800/600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -10)

    objek_class_map = {
        "ushape": UShape2D,
        "leaf": Leaf2D,
        "fan": FanShape2D,
        "talenan": Talenan3D,
        "botol": BotolBir3D,
        "guci": Guci3D
    }

    if "objects" not in current_state:
        current_state["objects"] = [default_object("talenan")]
    if "selected_index" not in current_state:
        current_state["selected_index"] = 0

    dragging = False
    last_mouse = (0, 0)
    clock = pygame.time.Clock()

    while current_state["running"]:
        for event in pygame.event.get():
            if event.type == QUIT:
                current_state["running"] = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                last_mouse = event.pos
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == MOUSEMOTION and dragging:
                idx = current_state["selected_index"]
                if idx < 0 or idx >= len(current_state["objects"]):
                    continue
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                last_mouse = event.pos
                obj_data = current_state["objects"][idx]
                if obj_data["type"] in ["ushape", "leaf", "fan"]:
                    obj_data["rotation"][1] += dx
                else:
                    obj_data["rotation"][0] += dy
                    obj_data["rotation"][1] += dx
            elif event.type == KEYDOWN:
                idx = current_state["selected_index"]
                # Navigasi objek aktif (opsional, misal Tab)
                if event.key == pygame.K_TAB:
                    if current_state["objects"]:
                        idx = (idx + 1) % len(current_state["objects"])
                        current_state["selected_index"] = idx
                # Tambah objek baru (gunakan tombol di GUI, ini untuk opsional saja)
                elif event.key == pygame.K_1:
                    current_state["objects"].append(default_object("ushape"))
                    current_state["selected_index"] = len(current_state["objects"]) - 1
                elif event.key == pygame.K_2:
                    current_state["objects"].append(default_object("leaf"))
                    current_state["selected_index"] = len(current_state["objects"]) - 1
                elif event.key == pygame.K_3:
                    current_state["objects"].append(default_object("fan"))
                    current_state["selected_index"] = len(current_state["objects"]) - 1
                elif event.key == pygame.K_4:
                    current_state["objects"].append(default_object("talenan"))
                    current_state["selected_index"] = len(current_state["objects"]) - 1
                elif event.key == pygame.K_5:
                    current_state["objects"].append(default_object("botol"))
                    current_state["selected_index"] = len(current_state["objects"]) - 1
                elif event.key == pygame.K_6:
                    current_state["objects"].append(default_object("guci"))
                    current_state["selected_index"] = len(current_state["objects"]) - 1
                # Transformasi objek aktif
                elif 0 <= idx < len(current_state["objects"]):
                    obj_data = current_state["objects"][idx]
                    if event.key == pygame.K_LEFT:
                        obj_data["pos"][0] -= 0.1
                    elif event.key == pygame.K_RIGHT:
                        obj_data["pos"][0] += 0.1
                    elif event.key == pygame.K_UP:
                        obj_data["pos"][1] += 0.1
                    elif event.key == pygame.K_DOWN:
                        obj_data["pos"][1] -= 0.1
                    elif event.key == pygame.K_PAGEUP:
                        obj_data["pos"][2] += 0.1
                    elif event.key == pygame.K_PAGEDOWN:
                        obj_data["pos"][2] -= 0.1
                    elif event.key == pygame.K_a:
                        obj_data["rotation"][0] += 5
                    elif event.key == pygame.K_z:
                        obj_data["rotation"][0] -= 5
                    elif event.key == pygame.K_s:
                        obj_data["rotation"][1] += 5
                    elif event.key == pygame.K_x:
                        obj_data["rotation"][1] -= 5
                    elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        obj_data["scale"] *= 1.1
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                        obj_data["scale"] *= 0.9
                    elif event.key == pygame.K_r:
                        obj_data["pos"] = [0.0, 0.0, 0.0]
                        obj_data["rotation"] = [0.0, 0.0]
                        obj_data["scale"] = 1.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -10)

        for i, obj_data in enumerate(current_state["objects"]):
            obj_type = obj_data["type"]
            obj = objek_class_map[obj_type]()
            pos = obj_data.get("pos", [0.0, 0.0, 0.0])
            scale = obj_data.get("scale", 1.0)
            rotation = obj_data.get("rotation", [0.0, 0.0])
            colors = obj_data.get("colors", {})
            fill_color = colors.get("fill", (1.0, 1.0, 1.0))
            border_color = colors.get("border", (0.0, 0.0, 0.0))

            if hasattr(obj, "fill_color"):
                obj.fill_color = fill_color
                if obj_type == "talenan":
                    obj.side_color = fill_color
            if hasattr(obj, "border_color"):
                obj.border_color = border_color
            if obj_type == "guci":
                if hasattr(obj, "top_color"):
                    obj.top_color = colors.get("top", (0.48, 0.37, 0.17))
                if hasattr(obj, "bottom_color"):
                    obj.bottom_color = colors.get("bottom", (0.35, 0.22, 0.11))

            if obj_type in ["ushape", "leaf", "fan"]:
                obj.set_position(pos[:2])
                obj.set_scale(scale)
                obj.set_rotation(rotation[1])
            else:
                obj.set_position(pos)
                obj.set_scale(scale)
                obj.set_rotation(rotation[0], rotation[1])

            obj.draw()
            # Highlight objek terpilih
           

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# GUI Tkinter untuk duplikat/hapus/memilih objek
def start_gui(current_state):
    root = tk.Tk()
    root.title("Kontrol Objek")

    def update_listbox():
        listbox.delete(0, tk.END)
        for i, obj in enumerate(current_state["objects"]):
            label = f"{i+1}. {obj['type']}"
            listbox.insert(tk.END, label)
        if current_state["selected_index"] >= 0 and current_state["objects"]:
            listbox.select_clear(0, tk.END)
            listbox.select_set(current_state["selected_index"])
            listbox.see(current_state["selected_index"])

    def on_select_obj(evt):
        sel = listbox.curselection()
        if sel:
            current_state["selected_index"] = sel[0]

    def on_duplicate():
        idx = current_state["selected_index"]
        if 0 <= idx < len(current_state["objects"]):
            obj = copy.deepcopy(current_state["objects"][idx])
            obj["pos"] = [obj["pos"][0] + 0.5, obj["pos"][1], obj["pos"][2]]
            current_state["objects"].append(obj)
            current_state["selected_index"] = len(current_state["objects"]) - 1
            update_listbox()

    def on_delete():
        idx = current_state["selected_index"]
        if 0 <= idx < len(current_state["objects"]):
            del current_state["objects"][idx]
            if current_state["objects"]:
                current_state["selected_index"] = max(0, idx-1)
            else:
                current_state["selected_index"] = -1
            update_listbox()

    def on_add(obj_type):
        current_state["objects"].append(default_object(obj_type))
        current_state["selected_index"] = len(current_state["objects"]) - 1
        update_listbox()

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    tk.Label(frame, text="Daftar Objek:").grid(row=0, column=0, columnspan=3)
    listbox = tk.Listbox(frame, width=20)
    listbox.grid(row=1, column=0, columnspan=3)
    listbox.bind('<<ListboxSelect>>', on_select_obj)

    btn_duplicate = tk.Button(frame, text="Duplikat", command=on_duplicate)
    btn_duplicate.grid(row=2, column=0, sticky="ew", pady=3)
    btn_delete = tk.Button(frame, text="Hapus", command=on_delete)
    btn_delete.grid(row=2, column=1, sticky="ew", pady=3)

    frame_add = tk.Frame(root)
    frame_add.pack(padx=10, pady=5)
    tk.Label(frame_add, text="Tambah Bentuk:").grid(row=0, column=0, columnspan=6)
    btn_ushape = tk.Button(frame_add, text="UShape", command=lambda: on_add("ushape"))
    btn_ushape.grid(row=1, column=0, padx=2)
    btn_leaf = tk.Button(frame_add, text="Leaf", command=lambda: on_add("leaf"))
    btn_leaf.grid(row=1, column=1, padx=2)
    btn_fan = tk.Button(frame_add, text="Fan", command=lambda: on_add("fan"))
    btn_fan.grid(row=1, column=2, padx=2)
    btn_talenan = tk.Button(frame_add, text="Talenan", command=lambda: on_add("talenan"))
    btn_talenan.grid(row=1, column=3, padx=2)
    btn_botol = tk.Button(frame_add, text="Botol", command=lambda: on_add("botol"))
    btn_botol.grid(row=1, column=4, padx=2)
    btn_guci = tk.Button(frame_add, text="Guci", command=lambda: on_add("guci"))
    btn_guci.grid(row=1, column=5, padx=2)

    def periodic_update():
        update_listbox()
        root.after(500, periodic_update)
    periodic_update()

    root.mainloop()

if __name__ == "__main__":
    current_state = {
        "running": True,
    }
    t = threading.Thread(target=run_opengl_window, args=(current_state,))
    t.daemon = True
    t.start()
    start_gui(current_state)
    current_state["running"] = False