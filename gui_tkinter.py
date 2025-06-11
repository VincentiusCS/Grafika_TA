import tkinter as tk
from tkinter import ttk, colorchooser
import threading
import copy
from main_opengl import run_opengl_window

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
        "colors": copy.deepcopy(base_colors[obj_type]),
        "auto_rotate": False,  # ✨ Flag untuk auto-rotate
        "auto_rotate_speed": [30.0, 50.0],  # ✨ Kecepatan rotasi [x, y] derajat/detik
        "auto_rotate_axes": [True, True]    # ✨ Axis mana yang berputar [x, y]
    }

class ObjectController:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Object Controller")
        self.root.geometry("400x850")  # Tinggi ditambah untuk kontrol animasi
        self.state = {
            "running": True,
            "objects": [default_object("ushape")],
            "selected_index": 0
        }
        self.start_opengl_thread()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_opengl_thread(self):
        self.opengl_thread = threading.Thread(
            target=run_opengl_window,
            args=(self.state,),
            daemon=True
        )
        self.opengl_thread.start()

    def create_widgets(self):
        # Gunakan Canvas + Scrollbar untuk panel utama agar bisa discroll
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        # Daftar objek & tombol duplikat/hapus
        obj_frame = ttk.LabelFrame(main_frame, text="Objek", padding="10")
        obj_frame.pack(fill=tk.X, pady=5)
        self.listbox = tk.Listbox(obj_frame, width=25, height=5)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.bind('<<ListboxSelect>>', self.on_select_obj)

        btn_frame = ttk.Frame(obj_frame)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(btn_frame, text="Duplikat", command=self.on_duplicate).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Hapus", command=self.on_delete).pack(fill=tk.X, pady=2)

        # Tombol tambah objek
        add_frame = ttk.LabelFrame(main_frame, text="Tambah Bentuk", padding="10")
        add_frame.pack(fill=tk.X, pady=5)
        objects = [
            ("U Shape", "ushape"),
            ("Daun", "leaf"),
            ("Kipas", "fan"),
            ("Talenan", "talenan"),
            ("Botol", "botol"),
            ("Guci", "guci")
        ]
        for name, obj_key in objects:
            btn = ttk.Button(
                add_frame,
                text=name,
                command=lambda k=obj_key: self.on_add(k)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X, expand=True)

        # Kontrol properti objek terpilih
        ctrl_frame = ttk.LabelFrame(main_frame, text="Kontrol Properti", padding="10")
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        # Posisi
        pos_frame = ttk.LabelFrame(ctrl_frame, text="Posisi", padding="5")
        pos_frame.pack(fill=tk.X, pady=2)
        for i, axis in enumerate("XYZ"):
            frame = ttk.Frame(pos_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{axis}:").pack(side=tk.LEFT)
            ttk.Button(frame, text="+", width=3,
                       command=lambda idx=i: self.update_pos(idx, 0.1)).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame, text="-", width=3,
                       command=lambda idx=i: self.update_pos(idx, -0.1)).pack(side=tk.LEFT)
        
        # Rotasi
        rot_frame = ttk.LabelFrame(ctrl_frame, text="Rotasi", padding="5")
        rot_frame.pack(fill=tk.X, pady=2)
        for i, axis in enumerate(["X Rot", "Y Rot"]):
            frame = ttk.Frame(rot_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{axis}:").pack(side=tk.LEFT)
            ttk.Button(frame, text="+", width=3,
                       command=lambda idx=i: self.update_rotation(idx, 5)).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame, text="-", width=3,
                       command=lambda idx=i: self.update_rotation(idx, -5)).pack(side=tk.LEFT)
        
        # Skala
        scale_frame = ttk.LabelFrame(ctrl_frame, text="Skala", padding="5")
        scale_frame.pack(fill=tk.X, pady=2)
        scale_btn_frame = ttk.Frame(scale_frame)
        scale_btn_frame.pack()
        ttk.Button(scale_btn_frame, text="Perbesar (+10%)",
                   command=lambda: self.update_scale(1.1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(scale_btn_frame, text="Perkecil (-10%)",
                   command=lambda: self.update_scale(0.9)).pack(side=tk.LEFT)

        # ✨ Kontrol Animasi 3D (BARU)
        animation_frame = ttk.LabelFrame(ctrl_frame, text="Animasi 3D", padding="5")
        animation_frame.pack(fill=tk.X, pady=2)
        
        # Toggle button dengan warna
        self.toggle_btn = ttk.Button(animation_frame, text="Toggle Auto-Rotate", 
                                   command=self.toggle_auto_rotate)
        self.toggle_btn.pack(side=tk.LEFT, padx=5)
        
        # Status animasi
        self.anim_status_var = tk.StringVar(value="OFF")
        status_label = ttk.Label(animation_frame, textvariable=self.anim_status_var, 
                               foreground="red", font=("Arial", 8, "bold"))
        status_label.pack(side=tk.LEFT, padx=5)
        
        # Speed controls
        speed_frame = ttk.Frame(animation_frame)
        speed_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(speed_frame, text="Kecepatan (°/detik):").pack(anchor=tk.W)
        speed_controls = ttk.Frame(speed_frame)
        speed_controls.pack(fill=tk.X)
        
        ttk.Label(speed_controls, text="X:").pack(side=tk.LEFT)
        self.speed_x_var = tk.StringVar(value="30.0")
        speed_x_entry = ttk.Entry(speed_controls, textvariable=self.speed_x_var, width=8)
        speed_x_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(speed_controls, text="Y:").pack(side=tk.LEFT, padx=(10,0))
        self.speed_y_var = tk.StringVar(value="50.0")
        speed_y_entry = ttk.Entry(speed_controls, textvariable=self.speed_y_var, width=8)
        speed_y_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(speed_controls, text="Set Speed", 
                  command=self.update_rotation_speed).pack(side=tk.LEFT, padx=5)
        
        # Axis controls
        axis_frame = ttk.Frame(speed_frame)
        axis_frame.pack(fill=tk.X, pady=2)
        ttk.Label(axis_frame, text="Axis Aktif:").pack(side=tk.LEFT)
        
        self.axis_x_var = tk.BooleanVar(value=True)
        self.axis_y_var = tk.BooleanVar(value=True)
        
        axis_x_check = ttk.Checkbutton(axis_frame, text="X-Axis", variable=self.axis_x_var,
                                     command=self.update_rotation_axes)
        axis_x_check.pack(side=tk.LEFT, padx=5)
        
        axis_y_check = ttk.Checkbutton(axis_frame, text="Y-Axis", variable=self.axis_y_var,
                                     command=self.update_rotation_axes)
        axis_y_check.pack(side=tk.LEFT, padx=5)

        # Warna
        color_frame = ttk.LabelFrame(ctrl_frame, text="Warna", padding="5")
        color_frame.pack(fill=tk.X, pady=2)
        ttk.Button(color_frame, text="Ubah Warna Objek", command=self.pilih_warna_objek).pack(side=tk.LEFT, padx=5)
        ttk.Button(color_frame, text="Ubah Warna Border", command=self.pilih_warna_border).pack(side=tk.LEFT, padx=5)
        self.guci_side_btn = ttk.Button(
            color_frame, text="Rubah Warna Guci Sisi Atas dan Bawah", command=self.pilih_warna_guci_sides
        )
        self.guci_side_btn.pack(side=tk.LEFT, padx=5)
        self.check_guci_buttons()

        # Reset buttons
        reset_frame = ttk.Frame(main_frame)
        reset_frame.pack(fill=tk.X, pady=10)
        ttk.Button(reset_frame, text="Reset Posisi",
                   command=self.reset_position).pack(side=tk.LEFT, padx=5)
        ttk.Button(reset_frame, text="Reset Rotasi",
                   command=self.reset_rotation).pack(side=tk.LEFT, padx=5)
        ttk.Button(reset_frame, text="Reset Skala",
                   command=self.reset_scale).pack(side=tk.LEFT)
        # ✨ Reset animasi button
        ttk.Button(reset_frame, text="Reset Animasi",
                   command=self.reset_animation).pack(side=tk.LEFT, padx=5)

        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.status_text = tk.StringVar()
        self.status_text.set(self.get_status_text())
        ttk.Label(status_frame, textvariable=self.status_text,
                  wraplength=350).pack(fill=tk.BOTH, expand=True)
        
        # Exit button
        ttk.Button(main_frame, text="Keluar",
                   command=self.on_close).pack(fill=tk.X, pady=10)

        self.update_listbox_periodic()

    # ✨ Fungsi-fungsi animasi baru
    def toggle_auto_rotate(self):
        idx = self.state["selected_index"]
        if 0 <= idx < len(self.state["objects"]):
            obj = self.state["objects"][idx]
            if obj["type"] in ["talenan", "botol", "guci"]:
                obj["auto_rotate"] = not obj.get("auto_rotate", False)
                self.update_animation_controls()

    def update_rotation_speed(self):
        idx = self.state["selected_index"]
        if 0 <= idx < len(self.state["objects"]):
            obj = self.state["objects"][idx]
            if obj["type"] in ["talenan", "botol", "guci"]:
                try:
                    new_speed_x = float(self.speed_x_var.get())
                    new_speed_y = float(self.speed_y_var.get())
                    obj["auto_rotate_speed"] = [new_speed_x, new_speed_y]
                except ValueError:
                    # Reset ke nilai sebelumnya jika input invalid
                    current_speed = obj.get("auto_rotate_speed", [30.0, 50.0])
                    self.speed_x_var.set(str(current_speed[0]))
                    self.speed_y_var.set(str(current_speed[1]))

    def update_rotation_axes(self):
        idx = self.state["selected_index"]
        if 0 <= idx < len(self.state["objects"]):
            obj = self.state["objects"][idx]
            if obj["type"] in ["talenan", "botol", "guci"]:
                obj["auto_rotate_axes"] = [self.axis_x_var.get(), self.axis_y_var.get()]

    def update_animation_controls(self):
        idx = self.state["selected_index"]
        if 0 <= idx < len(self.state["objects"]):
            obj = self.state["objects"][idx]
            if obj["type"] in ["talenan", "botol", "guci"]:
                auto_rotate = obj.get("auto_rotate", False)
                
                # Update status
                if auto_rotate:
                    self.anim_status_var.set("🔄 ON")
                    # Ubah warna status jadi hijau (tapi ttk tidak support langsung)
                else:
                    self.anim_status_var.set("⏸ OFF")
                
                # Update speed values
                speed = obj.get("auto_rotate_speed", [30.0, 50.0])
                self.speed_x_var.set(str(speed[0]))
                self.speed_y_var.set(str(speed[1]))
                
                # Update axis checkboxes
                axes = obj.get("auto_rotate_axes", [True, True])
                self.axis_x_var.set(axes[0])
                self.axis_y_var.set(axes[1])
            else:
                self.anim_status_var.set("N/A")
        else:
            self.anim_status_var.set("N/A")

    def reset_animation(self):
        idx = self.state["selected_index"]
        if 0 <= idx < len(self.state["objects"]):
            obj = self.state["objects"][idx]
            if obj["type"] in ["talenan", "botol", "guci"]:
                obj["auto_rotate"] = False
                obj["auto_rotate_speed"] = [30.0, 50.0]
                obj["auto_rotate_axes"] = [True, True]
                self.update_animation_controls()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, obj in enumerate(self.state["objects"]):
            # ✨ Tambahkan indikator animasi
            auto_indicator = ""
            if obj["type"] in ["talenan", "botol", "guci"] and obj.get("auto_rotate", False):
                auto_indicator = " 🔄"
            label = f"{i+1}. {obj['type']}{auto_indicator}"
            self.listbox.insert(tk.END, label)
        idx = self.state["selected_index"]
        if idx >= 0 and self.state["objects"]:
            self.listbox.select_clear(0, tk.END)
            self.listbox.select_set(idx)
            self.listbox.see(idx)

    def update_listbox_periodic(self):
        # Sinkronisasi listbox dengan state
        self.update_listbox()
        self.update_status()
        self.check_guci_buttons()
        self.update_animation_controls()  # ✨ Update kontrol animasi
        self.root.after(500, self.update_listbox_periodic)

    def on_select_obj(self, evt):
        sel = self.listbox.curselection()
        if sel:
            self.state["selected_index"] = sel[0]
            self.update_animation_controls()  # ✨ Update saat objek dipilih

    def on_duplicate(self):
        idx = self.state["selected_index"]
        if 0 <= idx < len(self.state["objects"]):
            obj = copy.deepcopy(self.state["objects"][idx])
            obj["pos"] = [obj["pos"][0] + 0.5, obj["pos"][1], obj["pos"][2]]
            self.state["objects"].append(obj)
            self.state["selected_index"] = len(self.state["objects"]) - 1

    def on_delete(self):
        idx = self.state["selected_index"]
        if 0 <= idx < len(self.state["objects"]):
            del self.state["objects"][idx]
            if self.state["objects"]:
                self.state["selected_index"] = max(0, idx-1)
            else:
                self.state["selected_index"] = -1

    def on_add(self, obj_type):
        new_obj = default_object(obj_type)
        # ✨ Auto-enable animasi untuk objek 3D baru
        if obj_type in ["talenan", "botol", "guci"]:
            new_obj["auto_rotate"] = True
        self.state["objects"].append(new_obj)
        self.state["selected_index"] = len(self.state["objects"]) - 1

    def pilih_warna_objek(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        warna = colorchooser.askcolor(title="Pilih Warna Objek")
        if warna and warna[1]:
            rgb = self.rgb_to_float(warna[1])
            self.state["objects"][idx]["colors"]["fill"] = rgb
            # Jika objek daun, set warna tulang daun otomatis kontras
            if self.state["objects"][idx]["type"] == "leaf":
                # Jika fill terlalu terang, vein hitam, jika gelap vein putih
                if sum(rgb) > 2.2:
                    self.state["objects"][idx]["colors"]["vein"] = (0,0,0)
                else:
                    self.state["objects"][idx]["colors"]["vein"] = (1,1,1)

    def pilih_warna_border(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        warna = colorchooser.askcolor(title="Pilih Warna Border")
        if warna and warna[1]:
            rgb = self.rgb_to_float(warna[1])
            self.state["objects"][idx]["colors"]["border"] = rgb

    def pilih_warna_guci_sides(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        obj = self.state["objects"][idx]
        if obj["type"] != "guci": return
        warna_top = colorchooser.askcolor(title="Pilih Warna Sisi Atas Guci")
        warna_bottom = colorchooser.askcolor(title="Pilih Warna Sisi Bawah Guci")
        if warna_top and warna_top[1]:
            rgb_top = self.rgb_to_float(warna_top[1])
            obj["colors"]["top"] = rgb_top
        if warna_bottom and warna_bottom[1]:
            rgb_bottom = self.rgb_to_float(warna_bottom[1])
            obj["colors"]["bottom"] = rgb_bottom

    def rgb_to_float(self, rgb_hex):
        rgb = [int(rgb_hex[i:i+2], 16) for i in (1, 3, 5)]
        return tuple([v/255.0 for v in rgb])

    def check_guci_buttons(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]):
            self.guci_side_btn.state(["disabled"])
            return
        obj = self.state["objects"][idx]
        if obj["type"] == "guci":
            self.guci_side_btn.state(["!disabled"])
        else:
            self.guci_side_btn.state(["disabled"])

    def update_pos(self, axis, delta):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        self.state["objects"][idx]["pos"][axis] += delta

    def update_rotation(self, axis, delta):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        self.state["objects"][idx]["rotation"][axis] += delta

    def update_scale(self, factor):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        self.state["objects"][idx]["scale"] *= factor

    def reset_position(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        self.state["objects"][idx]["pos"] = [0.0, 0.0, 0.0]

    def reset_rotation(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        self.state["objects"][idx]["rotation"] = [0.0, 0.0]

    def reset_scale(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return
        self.state["objects"][idx]["scale"] = 1.0

    def get_status_text(self):
        idx = self.state["selected_index"]
        if idx < 0 or idx >= len(self.state["objects"]): return "Tidak ada objek dipilih."
        obj = self.state["objects"][idx]
        fill = obj["colors"]["fill"]
        border = obj["colors"]["border"]
        
        # ✨ Info animasi
        auto_rotate = obj.get("auto_rotate", False)
        rotate_speed = obj.get("auto_rotate_speed", [30.0, 50.0])
        rotate_axes = obj.get("auto_rotate_axes", [True, True])
        
        desc = (
            f"Objek: {obj['type'].upper()}\n"
            f"Posisi: X={obj['pos'][0]:.1f}, Y={obj['pos'][1]:.1f}, Z={obj['pos'][2]:.1f}\n"
            f"Rotasi: X={obj['rotation'][0]:.1f}°, Y={obj['rotation'][1]:.1f}°\n"
            f"Skala: {obj['scale']:.1f}x\n"
            f"Warna Isi: R={fill[0]:.2f},G={fill[1]:.2f},B={fill[2]:.2f}\n"
            f"Warna Border: R={border[0]:.2f},G={border[1]:.2f},B={border[2]:.2f}"
        )
        
        # ✨ Tambahan info animasi untuk objek 3D
        if obj["type"] in ["talenan", "botol", "guci"]:
            desc += f"\n\n🔄 Auto-Rotate: {'ON' if auto_rotate else 'OFF'}"
            if auto_rotate:
                desc += f"\n⚡ Speed: X={rotate_speed[0]:.1f}°/s, Y={rotate_speed[1]:.1f}°/s"
                active_axes = []
                if rotate_axes[0]: active_axes.append("X")
                if rotate_axes[1]: active_axes.append("Y")
                desc += f"\n🎯 Active Axes: {', '.join(active_axes) if active_axes else 'None'}"
        
        if obj["type"] == "guci":
            top = obj["colors"].get("top", (0.48, 0.37, 0.17))
            bottom = obj["colors"].get("bottom", (0.35, 0.22, 0.11))
            desc += (
                f"\nWarna Atas Guci: R={top[0]:.2f},G={top[1]:.2f},B={top[2]:.2f}"
                f"\nWarna Bawah Guci: R={bottom[0]:.2f},G={bottom[1]:.2f},B={bottom[2]:.2f}"
            )
        return desc

    def update_status(self):
        self.status_text.set(self.get_status_text())

    def on_close(self):
        self.state["running"] = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ObjectController(root)
    root.mainloop()

if __name__ == "__main__":
    main()