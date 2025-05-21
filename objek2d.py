from OpenGL.GL import *
from math import pi, cos, sin
import math

class UShape2D:
    def __init__(self):
        self.x, self.y = 0.0, 0.0
        self.scale = 1.0
        self.rotation = 0.0
        self.fill_color = (0.66, 0.66, 0.66)  # abu-abu
        self.border_color = (0, 0, 0)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glScalef(self.scale, self.scale, 1)
        glRotatef(math.degrees(self.rotation), 0, 0, 1)

        # Parameter U
        outer_r = 1.0
        inner_r = 0.6
        height = 0.4  # tinggi batang vertikal
        arc_steps = 40

        # 1. Draw left rectangle (batang kiri)
        glColor3f(*self.fill_color)
        glBegin(GL_QUADS)
        glVertex2f(-outer_r, -height)
        glVertex2f(-outer_r, outer_r)
        glVertex2f(-inner_r, outer_r)
        glVertex2f(-inner_r, -height)
        glEnd()

        # 2. Draw right rectangle (batang kanan)
        glBegin(GL_QUADS)
        glVertex2f(outer_r, -height)
        glVertex2f(outer_r, outer_r)
        glVertex2f(inner_r, outer_r)
        glVertex2f(inner_r, -height)
        glEnd()

        # 3. Draw top arc (tebal, seperti donat setengah)
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(arc_steps+1):
            angle = math.pi - (i * math.pi / arc_steps)
            # Luar
            x_outer = outer_r * math.cos(angle)
            y_outer = outer_r * math.sin(angle) + outer_r
            glVertex2f(x_outer, y_outer)
            # Dalam
            x_inner = inner_r * math.cos(angle)
            y_inner = inner_r * math.sin(angle) + outer_r
            glVertex2f(x_inner, y_inner)
        glEnd()

        # 4. Border (opsional)
        glColor3f(*self.border_color)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        # Kiri bawah ke atas
        glVertex2f(-outer_r, -height)
        glVertex2f(-outer_r, outer_r)
        # arc luar
        for i in range(arc_steps+1):
            angle = math.pi - (i * math.pi / arc_steps)
            x_outer = outer_r * math.cos(angle)
            y_outer = outer_r * math.sin(angle) + outer_r
            glVertex2f(x_outer, y_outer)
        # kanan atas ke bawah
        glVertex2f(outer_r, outer_r)
        glVertex2f(outer_r, -height)
        glEnd()

        glBegin(GL_LINE_STRIP)
        # kanan bawah ke atas dalam
        glVertex2f(inner_r, -height)
        glVertex2f(inner_r, outer_r)
        # arc dalam
        for i in range(arc_steps+1):
            angle = math.pi - (i * math.pi / arc_steps)
            x_inner = inner_r * math.cos(angle)
            y_inner = inner_r * math.sin(angle) + outer_r
            glVertex2f(x_inner, y_inner)
        # kiri atas dalam ke bawah
        glVertex2f(-inner_r, outer_r)
        glVertex2f(-inner_r, -height)
        glEnd()

        glPopMatrix()

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, d_angle):
        self.rotation += math.radians(d_angle)

    def scale_obj(self, factor):
        self.scale *= factor

class Leaf2D:
    def __init__(self):
        # Bentuk daun
        self.vertices = [
            [0.0, 1.0],
            [-0.3, 0.8],
            [-0.5, 0.6],
            [-0.6, 0.3],
            [-0.65, 0.0],
            [-0.6, -0.3],
            [-0.5, -0.6],
            [-0.3, -0.8],
            [0.0, -1.0],
            [0.3, -0.8],
            [0.5, -0.6],
            [0.6, -0.3],
            [0.65, 0.0],
            [0.6, 0.3],
            [0.5, 0.6],
            [0.3, 0.8],
        ]
        self.color = (0.0, 0.8, 0.0)  # Hijau daun
        self.position = [0.0, 0.0]
        self.angle = 0
        self.scale_factor = 1.0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 0)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(self.scale_factor, self.scale_factor, 1)

        # Gambar daun utama
        glColor3f(*self.color)
        glBegin(GL_POLYGON)
        for v in self.vertices:
            glVertex2f(v[0], v[1])
        glEnd()

        # Gambar border
        glColor3f(0, 0.4, 0)
        glBegin(GL_LINE_LOOP)
        for v in self.vertices:
            glVertex2f(v[0], v[1])
        glEnd()

        # ===== Tambahkan urat daun (tulang) =====
        glColor3f(0.1, 0.3, 0.1)  # Hijau tua

        # Tulang utama (dari atas ke bawah)
        glBegin(GL_LINES)
        glVertex2f(0.0, 1.0)
        glVertex2f(0.0, -1.0)
        glEnd()

        # Tulang cabang kiri dan kanan
        veins = [
            ([-0.1, 0.7], [-0.5, 0.6]),
            ([-0.1, 0.4], [-0.6, 0.3]),
            ([-0.1, 0.1], [-0.65, 0.0]),
            ([-0.1, -0.2], [-0.6, -0.3]),
            ([-0.1, -0.5], [-0.5, -0.6]),
            ([0.1, 0.7], [0.5, 0.6]),
            ([0.1, 0.4], [0.6, 0.3]),
            ([0.1, 0.1], [0.65, 0.0]),
            ([0.1, -0.2], [0.6, -0.3]),
            ([0.1, -0.5], [0.5, -0.6]),
        ]

        glBegin(GL_LINES)
        for start, end in veins:
            glVertex2f(start[0], start[1])
            glVertex2f(end[0], end[1])
        glEnd()

        glPopMatrix()

    def translate(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def rotate(self, d_angle):
        self.angle += d_angle

    def scale(self, factor):
        self.scale_factor *= factor

class FanShape2D:
    def __init__(self, radius=1.0, handle_height=0.5, segments=100):
        self.radius = radius
        self.handle_height = handle_height
        self.segments = segments
        self.position = [0.0, 0.0]
        self.angle = 0
        self.scale_factor = 1.0

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position, 0)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(self.scale_factor, self.scale_factor, 1)

        top_offset = 0.1  # naikkan putih agar menyatu

        # --- Bagian Merah (Setengah Lingkaran Atas) ---
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for i in range(self.segments + 1):
            theta = pi * i / self.segments
            x = self.radius * cos(theta)
            y = self.radius * sin(theta)
            glVertex2f(x, y)
        glEnd()

        # --- Bagian Putih Bawah (Menutup Setengah Lingkaran Bawah) ---
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)
        for i in range(self.segments + 1):
            theta = pi - (pi * i / self.segments)
            x = self.radius * cos(theta)
            y = self.radius * sin(theta)
            glVertex2f(x, y - top_offset)  # geser ke bawah agar pas
        glEnd()

        # --- Gagang (Handle) ---
        glColor3f(1.0, 1.0, 1.0)
        handle_width = 0.15 * self.radius
        glBegin(GL_QUADS)
        glVertex2f(-handle_width / 2, -top_offset)
        glVertex2f(handle_width / 2, -top_offset)
        glVertex2f(handle_width / 2, -top_offset - self.handle_height)
        glVertex2f(-handle_width / 2, -top_offset - self.handle_height)
        glEnd()

        # --- Outline Hitam ---
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2.0)

        # Lingkaran luar
        glBegin(GL_LINE_STRIP)
        for i in range(self.segments + 1):
            theta = pi * i / self.segments
            x = self.radius * cos(theta)
            y = self.radius * sin(theta)
            glVertex2f(x, y)
        glEnd()

        # Lengkungan putih bawah
        glBegin(GL_LINE_STRIP)
        for i in range(self.segments + 1):
            theta = pi * i / self.segments
            x = self.radius * cos(theta)
            y = self.radius * sin(theta) - top_offset
            glVertex2f(x, y)
        glEnd()

        # Handle
        glBegin(GL_LINE_LOOP)
        glVertex2f(-handle_width / 2, -top_offset)
        glVertex2f(handle_width / 2, -top_offset)
        glVertex2f(handle_width / 2, -top_offset - self.handle_height)
        glVertex2f(-handle_width / 2, -top_offset - self.handle_height)
        glEnd()

        glPopMatrix()

    def translate(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def rotate(self, d_angle):
        self.angle += d_angle

    def scale(self, factor):
        self.scale_factor *= factor