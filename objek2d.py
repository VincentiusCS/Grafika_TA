from OpenGL.GL import *
from math import pi, cos, sin, radians

class UShape2D:
    def __init__(self):
        self.x, self.y = 0.0, 0.0
        self.scale_factor = 1.0
        self.rotation = 0.0  # dalam radian
        self.fill_color = (0.66, 0.66, 0.66)  # abu-abu
        self.border_color = (0, 0, 0)

    def set_position(self, pos):
        self.x, self.y = pos[0], pos[1]

    def set_scale(self, scale):
        self.scale_factor = scale

    def set_rotation(self, angle_degrees):
        self.rotation = radians(angle_degrees)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glScalef(self.scale_factor, self.scale_factor, 1)
        glRotatef(self.rotation * 180.0 / pi, 0, 0, 1)

        outer_r = 1.0
        inner_r = 0.6
        height = 0.4
        arc_steps = 40

        glColor3f(*self.fill_color)

        # Batang kiri
        glBegin(GL_QUADS)
        glVertex2f(-outer_r, -height)
        glVertex2f(-outer_r, outer_r)
        glVertex2f(-inner_r, outer_r)
        glVertex2f(-inner_r, -height)
        glEnd()

        # Batang kanan
        glBegin(GL_QUADS)
        glVertex2f(outer_r, -height)
        glVertex2f(outer_r, outer_r)
        glVertex2f(inner_r, outer_r)
        glVertex2f(inner_r, -height)
        glEnd()

        # Lengkungan atas
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(arc_steps + 1):
            angle = pi - (i * pi / arc_steps)
            x_outer = outer_r * cos(angle)
            y_outer = outer_r * sin(angle) + outer_r
            x_inner = inner_r * cos(angle)
            y_inner = inner_r * sin(angle) + outer_r
            glVertex2f(x_outer, y_outer)
            glVertex2f(x_inner, y_inner)
        glEnd()

        # Border - DIPERBAIKI: Pisahkan menjadi segmen terpisah
        glColor3f(*self.border_color)
        glLineWidth(3)
        
        # Border kiri (dari bawah ke atas)
        glBegin(GL_LINE_STRIP)
        glVertex2f(-outer_r, -height)
        glVertex2f(-outer_r, outer_r)
        glEnd()
        
        # Border lengkungan luar
        glBegin(GL_LINE_STRIP)
        glVertex2f(-outer_r, outer_r)
        for i in range(arc_steps + 1):
            angle = pi - (i * pi / arc_steps)
            x = outer_r * cos(angle)
            y = outer_r * sin(angle) + outer_r
            glVertex2f(x, y)
        glVertex2f(outer_r, outer_r)
        glEnd()
        
        # Border kanan (dari atas ke bawah)
        glBegin(GL_LINE_STRIP)
        glVertex2f(outer_r, outer_r)
        glVertex2f(outer_r, -height)
        glEnd()

        # Border dalam - bagian kiri (dari bawah ke atas)
        glBegin(GL_LINE_STRIP)
        glVertex2f(-inner_r, -height)
        glVertex2f(-inner_r, outer_r)
        glEnd()
        
        # Border lengkungan dalam
        glBegin(GL_LINE_STRIP)
        glVertex2f(-inner_r, outer_r)
        for i in range(arc_steps + 1):
            angle = pi - (i * pi / arc_steps)
            x = inner_r * cos(angle)
            y = inner_r * sin(angle) + outer_r
            glVertex2f(x, y)
        glVertex2f(inner_r, outer_r)
        glEnd()
        
        # Border dalam - bagian kanan (dari atas ke bawah)
        glBegin(GL_LINE_STRIP)
        glVertex2f(inner_r, outer_r)
        glVertex2f(inner_r, -height)
        glEnd()

        glPopMatrix()

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, d_angle_degrees):
        self.rotation += radians(d_angle_degrees)

    def scale(self, factor):
        self.scale_factor *= factor


class Leaf2D:
    def __init__(self):
        self.vertices = [
            [0.0, 1.0], [-0.3, 0.8], [-0.5, 0.6], [-0.6, 0.3], [-0.65, 0.0],
            [-0.6, -0.3], [-0.5, -0.6], [-0.3, -0.8], [0.0, -1.0],
            [0.3, -0.8], [0.5, -0.6], [0.6, -0.3], [0.65, 0.0], [0.6, 0.3],
            [0.5, 0.6], [0.3, 0.8]
        ]
        self.fill_color = (0.0, 0.8, 0.0)
        self.border_color = (0, 0.4, 0)
        self.position = [0.0, 0.0]
        self.angle = 0.0  # derajat
        self.scale_factor = 1.0

    def set_position(self, pos):
        self.position[0], self.position[1] = pos[0], pos[1]

    def set_scale(self, scale):
        self.scale_factor = scale

    def set_rotation(self, angle_degrees):
        self.angle = angle_degrees

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position, 0)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(self.scale_factor, self.scale_factor, 1)

        glColor3f(*self.fill_color)
        glBegin(GL_POLYGON)
        for v in self.vertices:
            glVertex2f(*v)
        glEnd()

        glColor3f(*self.border_color)
        glLineWidth(2.5)
        glBegin(GL_LINE_LOOP)
        for v in self.vertices:
            glVertex2f(*v)
        glEnd()

        # Tulang daun utama
        glColor3f(0.1, 0.3, 0.1)
        glBegin(GL_LINES)
        glVertex2f(0.0, 1.0)
        glVertex2f(0.0, -1.0)
        glEnd()

        # Tulang cabang
        veins = [
            ([-0.1, 0.7], [-0.5, 0.6]), ([-0.1, 0.4], [-0.6, 0.3]), ([-0.1, 0.1], [-0.65, 0.0]),
            ([-0.1, -0.2], [-0.6, -0.3]), ([-0.1, -0.5], [-0.5, -0.6]),
            ([0.1, 0.7], [0.5, 0.6]), ([0.1, 0.4], [0.6, 0.3]), ([0.1, 0.1], [0.65, 0.0]),
            ([0.1, -0.2], [0.6, -0.3]), ([0.1, -0.5], [0.5, -0.6]),
        ]
        glBegin(GL_LINES)
        for start, end in veins:
            glVertex2f(*start)
            glVertex2f(*end)
        glEnd()

        glPopMatrix()

    def translate(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def rotate(self, d_angle_degrees):
        self.angle += d_angle_degrees

    def scale(self, factor):
        self.scale_factor *= factor


class FanShape2D:
    def __init__(self, radius=1.0, handle_height=0.5, segments=100):
        self.radius = radius
        self.handle_height = handle_height
        self.segments = segments
        self.position = [0.0, 0.0]
        self.angle = 0.0  # derajat
        self.scale_factor = 1.0
        self.fill_color = (1.0, 0.0, 0.0)
        self.border_color = (0.0, 0.0, 0.0)

    def set_position(self, pos):
        self.position[0], self.position[1] = pos[0], pos[1]

    def set_scale(self, scale):
        self.scale_factor = scale

    def set_rotation(self, angle_degrees):
        self.angle = angle_degrees

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position, 0)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(self.scale_factor, self.scale_factor, 1)

        top_offset = 0.1
        handle_width = 0.15 * self.radius

        # Fill - Merah (atau sesuai fill_color)
        glColor3f(*self.fill_color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for i in range(self.segments + 1):
            theta = pi * i / self.segments
            glVertex2f(self.radius * cos(theta), self.radius * sin(theta))
        glEnd()

        # Border
        glColor3f(*self.border_color)
        glLineWidth(2.5)
        glBegin(GL_LINE_STRIP)
        for i in range(self.segments + 1):
            theta = pi * i / self.segments
            glVertex2f(self.radius * cos(theta), self.radius * sin(theta))
        glEnd()

        # Putih - bawah (tidak diubah warnanya)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)
        for i in range(self.segments + 1):
            theta = pi - (pi * i / self.segments)
            x = self.radius * cos(theta)
            y = self.radius * sin(theta)
            glVertex2f(x, y - top_offset)
        glEnd()

        # Gagang kipas
        glColor3f(0.65, 0.5, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(-handle_width / 2, -self.handle_height)
        glVertex2f(handle_width / 2, -self.handle_height)
        glVertex2f(handle_width / 2, 0)
        glVertex2f(-handle_width / 2, 0)
        glEnd()

        glPopMatrix()

    def translate(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def rotate(self, d_angle_degrees):
        self.angle += d_angle_degrees

    def scale(self, factor):
        self.scale_factor *= factor