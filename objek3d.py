from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Talenan3D:
    def __init__(self):
        self.width = 2.4
        self.height = 0.15
        self.depth = 1.6
        self.position = [0.0, 0.0, 0.0]
        self.angle_x = 20.0
        self.angle_y = 15.0
        self.scale_factor = 1.0
        self.fill_color = (0.85, 0.7, 0.4)    # warna utama permukaan
        self.border_color = (0.3, 0.23, 0.11)
        self.corner_radius = 0.18
        self.hole_radius = 0.13
        self.hole_offset_x = -self.width / 2 + self.corner_radius + 0.12
        self.hole_offset_y = self.depth / 2 - self.corner_radius - 0.12

    def set_position(self, pos):
        self.position = list(pos)

    def set_scale(self, scale):
        self.scale_factor = scale

    def set_rotation(self, angle_x, angle_y):
        self.angle_x = angle_x
        self.angle_y = angle_y

    def draw(self):
        w = self.width / 2 * self.scale_factor
        h = self.height / 2 * self.scale_factor
        d = self.depth / 2 * self.scale_factor
        r = min(self.corner_radius * self.scale_factor, w, d)

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

        # Permukaan atas dan bawah (isi)
        glColor3f(*self.fill_color)
        self.draw_rounded_rect_ring_with_hole(z=+h, w=w, d=d, r=r, normal=(0,0,1))
        self.draw_rounded_rect_ring_with_hole(z=-h, w=w, d=d, r=r, normal=(0,0,-1), flip_hole=True)

        # SISI SAMPING: gunakan fill_color juga!
        glColor3f(*self.fill_color)
        self.draw_rounded_sides(w, h, d, r)

        # Dinding lubang (pakai border_color)
        glColor3f(*self.border_color)
        self.draw_hole_wall(w, h, d)

        # Garis border outline talenan (border_color)
        self.draw_border(w, h, d, r)

        glPopMatrix()

    def draw_rounded_rect_ring_with_hole(self, z, w, d, r, normal=(0,0,1), steps=10, hole_steps=40, flip_hole=False):
        corners = [
            (+w-r, +d-r),
            (-w+r, +d-r),
            (-w+r, -d+r),
            (+w-r, -d+r)
        ]
        angles = [
            (0.0, math.pi/2),
            (math.pi/2, math.pi),
            (math.pi, 3*math.pi/2),
            (3*math.pi/2, 2*math.pi)
        ]
        outer = []
        for i in range(4):
            cx, cy = corners[i]
            theta0, theta1 = angles[i]
            for j in range(steps+1):
                theta = theta0 + (theta1-theta0)*j/steps
                x = cx + r * math.cos(theta)
                y = cy + r * math.sin(theta)
                outer.append((x, y))
        hole_x = self.hole_offset_x * self.scale_factor
        hole_y = self.hole_offset_y * self.scale_factor
        hole_r = self.hole_radius * self.scale_factor
        inner = []
        for i in range(hole_steps+1):
            t = (i if not flip_hole else (hole_steps-i))
            theta = 2 * math.pi * t / hole_steps
            x = hole_x + hole_r * math.cos(theta)
            y = hole_y + hole_r * math.sin(theta)
            inner.append((x, y))
        N = max(len(outer), len(inner))
        glBegin(GL_QUAD_STRIP)
        for i in range(N):
            idx_outer = i % len(outer)
            idx_inner = i % len(inner)
            glNormal3f(*normal)
            glVertex3f(outer[idx_outer][0], outer[idx_outer][1], z)
            glVertex3f(inner[idx_inner][0], inner[idx_inner][1], z)
        glNormal3f(*normal)
        glVertex3f(outer[0][0], outer[0][1], z)
        glVertex3f(inner[0][0], inner[0][1], z)
        glEnd()

    def draw_rounded_sides(self, w, h, d, r, steps=12):
        # Sisi lurus
        self.draw_side_strip((+w-r, +d), (-w+r, +d), +h, -h, r, 0.0, math.pi/2, steps)
        self.draw_side_strip((+w-r, -d), (-w+r, -d), +h, -h, r, 3*math.pi/2, 2*math.pi, steps)
        self.draw_side_strip((-w, +d-r), (-w, -d+r), +h, -h, r, math.pi/2, math.pi, steps)
        self.draw_side_strip((+w, +d-r), (+w, -d+r), +h, -h, r, 2*math.pi, 0.0, steps)
        # Sisi lengkung
        self.draw_corner_side(+w-r, +d-r, +h, -h, r, 0.0, math.pi/2, steps)
        self.draw_corner_side(-w+r, +d-r, +h, -h, r, math.pi/2, math.pi, steps)
        self.draw_corner_side(-w+r, -d+r, +h, -h, r, math.pi, 3*math.pi/2, steps)
        self.draw_corner_side(+w-r, -d+r, +h, -h, r, 3*math.pi/2, 2*math.pi, steps)

    def draw_side_strip(self, p1, p2, h_top, h_bot, r, start_angle, end_angle, steps):
        x1, y1 = p1
        x2, y2 = p2
        glBegin(GL_QUAD_STRIP)
        for i in range(steps+1):
            t = i / steps
            x = x1 + (x2-x1) * t
            y = y1 + (y2-y1) * t
            glNormal3f(x, y, 0)
            glVertex3f(x, y, h_top)
            glVertex3f(x, y, h_bot)
        glEnd()

    def draw_corner_side(self, cx, cy, h_top, h_bot, r, angle0, angle1, steps):
        glBegin(GL_QUAD_STRIP)
        for i in range(steps+1):
            theta = angle0 + (angle1-angle0)*i/steps
            x = cx + r*math.cos(theta)
            y = cy + r*math.sin(theta)
            glNormal3f(math.cos(theta), math.sin(theta), 0)
            glVertex3f(x, y, h_top)
            glVertex3f(x, y, h_bot)
        glEnd()

    def draw_hole_wall(self, w, h, d, hole_steps=40):
        x = self.hole_offset_x * self.scale_factor
        y = self.hole_offset_y * self.scale_factor
        z_top = h
        z_bot = -h
        r = self.hole_radius * self.scale_factor
        glBegin(GL_QUAD_STRIP)
        for i in range(hole_steps+1):
            theta = 2 * math.pi * i / hole_steps
            dx = r * math.cos(theta)
            dy = r * math.sin(theta)
            glNormal3f(dx, dy, 0)
            glVertex3f(x + dx, y + dy, z_top)
            glVertex3f(x + dx, y + dy, z_bot)
        glEnd()

    def draw_border(self, w, h, d, r, steps=48):
        # Border outline di semua tepi talenan (atas, bawah, samping)
        glLineWidth(2.5)
        glColor3f(*self.border_color)
        # Outline atas
        self._draw_rounded_rect_outline(z=+h, w=w, d=d, r=r, steps=steps)
        # Outline bawah
        self._draw_rounded_rect_outline(z=-h, w=w, d=d, r=r, steps=steps)
        # Garis tepi vertical (pinggir body)
        for (x, y) in [  # 4 titik pojok luar
            (+w-r, +d), (-w+r, +d), (-w+r, -d), (+w-r, -d)
        ]:
            glBegin(GL_LINES)
            glVertex3f(x, y, +h)
            glVertex3f(x, y, -h)
            glEnd()

    def _draw_rounded_rect_outline(self, z, w, d, r, steps=48):
        # Menggambar outline bentuk rounded rectangle di z tertentu
        corners = [
            (+w-r, +d-r),
            (-w+r, +d-r),
            (-w+r, -d+r),
            (+w-r, -d+r)
        ]
        angles = [
            (0.0, math.pi/2),
            (math.pi/2, math.pi),
            (math.pi, 3*math.pi/2),
            (3*math.pi/2, 2*math.pi)
        ]
        pts = []
        for i in range(4):
            cx, cy = corners[i]
            theta0, theta1 = angles[i]
            for j in range(steps+1):
                theta = theta0 + (theta1-theta0)*j/steps
                x = cx + r * math.cos(theta)
                y = cy + r * math.sin(theta)
                pts.append((x, y))
        glBegin(GL_LINE_LOOP)
        for x, y in pts:
            glVertex3f(x, y, z)
        glEnd()

class BotolBir3D:
    def __init__(self):
        self.position = [0.0, 0.0, 0.0]
        self.scale_factor = 1.0
        self.angle_x = -60.0
        self.angle_y = 90.0
        self.fill_color = (0.6, 0.3, 0.1)
        self.border_color = (0.5, 0.25, 0.1)  # default border
        self.top_color = (0.8, 0.6, 0.2)      # warna tutup tetap

    def set_position(self, pos):
        self.position = list(pos)

    def set_scale(self, scale):
        self.scale_factor = scale

    def set_rotation(self, angle_x, angle_y):
        self.angle_x = angle_x
        self.angle_y = angle_y

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glScalef(self.scale_factor, self.scale_factor, self.scale_factor)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

        quad = gluNewQuadric()

        # BADAN BAWAH
        glColor3f(*self.fill_color)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        gluCylinder(quad, 0.25, 0.23, 0.7, 32, 8)
        glPushMatrix()
        glRotatef(180, 1, 0, 0)
        gluDisk(quad, 0.0, 0.25, 32, 1)
        glPopMatrix()
        glPopMatrix()

        # LEHER
        glColor3f(*self.fill_color)
        glPushMatrix()
        glTranslatef(0, 0, 0.7)
        gluCylinder(quad, 0.13, 0.13, 0.3, 32, 8)
        glPopMatrix()

        # PINGGIR LEHER
        glColor3f(*self.fill_color)
        glPushMatrix()
        glTranslatef(0, 0, 0.7)
        gluCylinder(quad, 0.23, 0.13, 0.08, 32, 8)
        glPopMatrix()

        # TUTUP
        glColor3f(*self.top_color)
        glPushMatrix()
        glTranslatef(0, 0, 1.0)
        gluCylinder(quad, 0.10, 0.10, 0.08, 32, 8)
        glPushMatrix()
        glTranslatef(0, 0, 0.08)
        gluDisk(quad, 0.0, 0.10, 32, 1)
        glPopMatrix()
        glPopMatrix()

        # ===== BORDER =====
        glLineWidth(2.5)
        # Border badan bawah
        glColor3f(*self.border_color)
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            theta = 2 * math.pi * i / 32
            x = 0.25 * math.cos(theta)
            y = 0.25 * math.sin(theta)
            glVertex3f(x, y, 0)
        glEnd()
        # Border badan atas
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            theta = 2 * math.pi * i / 32
            x = 0.23 * math.cos(theta)
            y = 0.23 * math.sin(theta)
            glVertex3f(x, y, 0.7)
        glEnd()
        # Border leher bawah
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            theta = 2 * math.pi * i / 32
            x = 0.13 * math.cos(theta)
            y = 0.13 * math.sin(theta)
            glVertex3f(x, y, 0.7)
        glEnd()
        # Border leher atas
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            theta = 2 * math.pi * i / 32
            x = 0.13 * math.cos(theta)
            y = 0.13 * math.sin(theta)
            glVertex3f(x, y, 1.0)
        glEnd()
        # Border tutup bawah
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            theta = 2 * math.pi * i / 32
            x = 0.10 * math.cos(theta)
            y = 0.10 * math.sin(theta)
            glVertex3f(x, y, 1.0)
        glEnd()
        # Border tutup atas
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            theta = 2 * math.pi * i / 32
            x = 0.10 * math.cos(theta)
            y = 0.10 * math.sin(theta)
            glVertex3f(x, y, 1.08)
        glEnd()

        gluDeleteQuadric(quad)
        glPopMatrix()

class Guci3D:
    def __init__(self):
        self.position = [0.0, 0.0, 0.0]
        self.scale_factor = 3.5
        self.angle_x = -30.0
        self.angle_y = 20.0
        self.profile = [
            (0.13, 0.0),
            (0.15, 0.08),
            (0.19, 0.18),
            (0.28, 0.32),
            (0.34, 0.60),
            (0.33, 0.92),
            (0.28, 1.12),
            (0.20, 1.26),
            (0.22, 1.32),
            (0.19, 1.35),
            (0.17, 1.38),
        ]
        self.fill_color = (0.53, 0.42, 0.22)
        self.border_color = (0.35, 0.25, 0.13)
        self.top_color = (0.48, 0.37, 0.17)
        self.bottom_color = (0.35, 0.22, 0.11)

    def set_position(self, pos):
        self.position = list(pos)
    def set_scale(self, scale):
        self.scale_factor = scale
    def set_rotation(self, angle_x, angle_y):
        self.angle_x = angle_x
        self.angle_y = angle_y
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glScalef(self.scale_factor, self.scale_factor, self.scale_factor)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)
        self.draw_body()
        self.draw_border()  # <-- Tambahkan border setelah body
        glPopMatrix()

    def draw_body(self, slices=72):
        # Bawah guci
        glColor3f(*self.bottom_color)
        self.draw_profile_section(0, 2, slices)
        # Badan guci
        glColor3f(*self.fill_color)
        self.draw_profile_section(2, 6, slices)
        # Leher guci
        glColor3f(*self.top_color)
        self.draw_profile_section(6, len(self.profile)-1, slices)
        # Ring atas
        glColor3f(*self.border_color)
        self.draw_profile_section(len(self.profile)-2, len(self.profile)-1, slices)

    def draw_profile_section(self, idx_start, idx_end, slices):
        for i in range(idx_start, idx_end):
            r0, z0 = self.profile[i]
            r1, z1 = self.profile[i+1]
            glBegin(GL_QUAD_STRIP)
            for j in range(slices+1):
                theta = 2 * math.pi * j / slices
                x0 = r0 * math.cos(theta)
                y0 = r0 * math.sin(theta)
                x1 = r1 * math.cos(theta)
                y1 = r1 * math.sin(theta)
                nx0, ny0 = math.cos(theta), math.sin(theta)
                nx1, ny1 = math.cos(theta), math.sin(theta)
                glNormal3f(nx0, ny0, 0)
                glVertex3f(x0, y0, z0)
                glNormal3f(nx1, ny1, 0)
                glVertex3f(x1, y1, z1)
            glEnd()

    def draw_border(self, slices=72):
        glLineWidth(2.5)
        glColor3f(*self.border_color)
        # Garis border pada setiap ring profile guci
        for i in range(len(self.profile)):
            r, z = self.profile[i]
            glBegin(GL_LINE_LOOP)
            for j in range(slices):
                theta = 2 * math.pi * j / slices
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                glVertex3f(x, y, z)
            glEnd()