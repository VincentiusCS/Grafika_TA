from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Talenan3D:
    def __init__(self):  # <-- Perbaiki dari _init_ ke __init__
        self.width = 2.4
        self.height = 0.15
        self.depth = 1.6
        self.position = [0.0, 0.0, 0.0]
        self.angle_x = 20.0
        self.angle_y = 15.0
        self.scale_factor = 1.0
        self.color = (0.85, 0.7, 0.4)

    def draw(self):
        w = self.width / 2 * self.scale_factor
        h = self.height / 2 * self.scale_factor
        d = self.depth / 2 * self.scale_factor

        vertices = [
            [ w,  h, -d],  # 0 kanan atas belakang
            [ w, -h, -d],  # 1 kanan bawah belakang
            [-w, -h, -d],  # 2 kiri bawah belakang
            [-w,  h, -d],  # 3 kiri atas belakang
            [ w,  h,  d],  # 4 kanan atas depan
            [ w, -h,  d],  # 5 kanan bawah depan
            [-w, -h,  d],  # 6 kiri bawah depan
            [-w,  h,  d],  # 7 kiri atas depan
        ]
        faces = [
            [0, 1, 2, 3],  # Belakang
            [4, 5, 6, 7],  # Depan
            [0, 4, 5, 1],  # Kanan
            [3, 7, 6, 2],  # Kiri
            [0, 3, 7, 4],  # Atas
            [1, 2, 6, 5],  # Bawah
        ]

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)
        glColor3f(*self.color)
        for face in faces:
            glBegin(GL_QUADS)
            for vertex in face:
                glVertex3fv(vertices[vertex])
            glEnd()
        glPopMatrix()

    def translate(self, dx, dy, dz):
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz

    def rotate(self, d_angle_x=0, d_angle_y=0):
        self.angle_x += d_angle_x
        self.angle_y += d_angle_y

    def scale(self, factor):
        self.scale_factor *= factor

class BotolBir3D:
    def __init__(self):  # <-- Perbaiki dari _init_ ke __init__
        self.pos = [0, 0, 0]
        self.scale = 1.0
        self.rot_x = -60  # Lihat dari samping atas
        self.rot_y = 90

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glScalef(self.scale, self.scale, self.scale)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)

        quad = gluNewQuadric()

        # Bagian bawah botol (tabung besar)
        glColor3f(0.6, 0.3, 0.1)  # coklat tua
        glPushMatrix()
        glTranslatef(0, 0, 0)
        gluCylinder(quad, 0.25, 0.23, 0.7, 32, 8)
        # Alas bawah botol
        glPushMatrix()
        glRotatef(180, 1, 0, 0)
        gluDisk(quad, 0.0, 0.25, 32, 1)
        glPopMatrix()
        glPopMatrix()

        # Leher botol
        glColor3f(0.5, 0.25, 0.1)
        glPushMatrix()
        glTranslatef(0, 0, 0.7)
        gluCylinder(quad, 0.13, 0.13, 0.3, 32, 8)
        glPopMatrix()

        # Mulut botol
        glColor3f(0.8, 0.6, 0.2)
        glPushMatrix()
        glTranslatef(0, 0, 1.0)
        gluCylinder(quad, 0.10, 0.10, 0.08, 32, 8)
        # Tutup atas
        glPushMatrix()
        glTranslatef(0, 0, 0.08)
        gluDisk(quad, 0.0, 0.10, 32, 1)
        glPopMatrix()
        glPopMatrix()

        # Dada botol (transisi melengkung ke leher)
        glColor3f(0.6, 0.3, 0.1)
        glPushMatrix()
        glTranslatef(0, 0, 0.7)
        gluCylinder(quad, 0.23, 0.13, 0.08, 32, 8)
        glPopMatrix()

        gluDeleteQuadric(quad)
        glPopMatrix()

    def translate(self, dx, dy, dz):
        self.pos[0] += dx
        self.pos[1] += dy
        self.pos[2] += dz

    def rotate(self, dx=0, dy=0):
        self.rot_x += dx
        self.rot_y += dy

    def scale_obj(self, factor):
        self.scale *= factor

class Guci3D:
    def __init__(self):  # <-- Perbaiki dari _init_ ke __init__
        self.pos = [0, 0, 0]
        self.scale = 3.5   # Agar besar di layar
        self.rot_x = -30   # Supaya tampak 3D dari depan
        self.rot_y = 20
        # Profil siluet guci, (radius, tinggi), meniru bentuk pada gambar 3 (dan tanpa polygon bawah)
        self.profile = [
            (0.13, 0.0),   # dasar bawah (kecil)
            (0.15, 0.08),  # bagian bawah mulai membesar (warna tanah)
            (0.19, 0.18),  # mulai perut bawah
            (0.28, 0.32),  # perut mulai membulat
            (0.34, 0.60),  # perut paling lebar
            (0.33, 0.92),  # mulai mengecil ke leher
            (0.28, 1.12),  # bagian leher bawah
            (0.20, 1.26),  # leher atas
            (0.22, 1.32),  # bibir luar atas
            (0.19, 1.35),  # bibir dalam atas
            (0.17, 1.38),  # ujung dalam mulut
        ]
        # Warna guci: agak coklat tanah, sedikit glossy
        self.body_color = (0.53, 0.42, 0.22)
        self.neck_color = (0.48, 0.37, 0.17)
        self.bottom_color = (0.35, 0.22, 0.11)

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glScalef(self.scale, self.scale, self.scale)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        self.draw_body()
        glPopMatrix()

    def draw_body(self, slices=72):
        # Surface of revolution (lathe)
        # Bagian bawah/dasar
        glColor3f(*self.bottom_color)
        self.draw_profile_section(0, 2, slices)
        # Bagian badan (perut)
        glColor3f(*self.body_color)
        self.draw_profile_section(2, 6, slices)
        # Bagian leher dan bibir
        glColor3f(*self.neck_color)
        self.draw_profile_section(6, len(self.profile)-1, slices)
        # Bibir atas agak gelap/kontras
        glColor3f(0.35, 0.25, 0.13)
        self.draw_profile_section(len(self.profile)-2, len(self.profile)-1, slices)
        # Jangan gambar polygon bawah agar tidak ada bulatan kecil
        # r0, z0 = self.profile[0]
        # glColor3f(*self.bottom_color)
        # glBegin(GL_POLYGON)
        # glNormal3f(0, 0, -1)
        # for j in range(slices):
        #     theta = 2 * math.pi * j / slices
        #     x = r0 * math.cos(theta)
        #     y = r0 * math.sin(theta)
        #     glVertex3f(x, y, z0)
        # glEnd()

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
                # normal sederhana, cukup arah radial
                nx0, ny0 = math.cos(theta), math.sin(theta)
                nx1, ny1 = math.cos(theta), math.sin(theta)
                glNormal3f(nx0, ny0, 0)
                glVertex3f(x0, y0, z0)
                glNormal3f(nx1, ny1, 0)
                glVertex3f(x1, y1, z1)
            glEnd()

    def translate(self, dx, dy, dz):
        self.pos[0] += dx
        self.pos[1] += dy
        self.pos[2] += dz

    def rotate(self, dx=0, dy=0):
        self.rot_x += dx
        self.rot_y += dy

    def scale_obj(self, factor):
        self.scale *= factor