import tkinter as tk
import time
import math

H, W = 480, 640

masses = []
springs = []

root = tk.Tk()
c = tk.Canvas(root, height=H, width=W, bg="gray")
c.pack()


def calculate_angle(M1, M2):
    if M1.x <= M2.x and M1.y <= M2.y:
        if M1.x - M2.x != 0:
            theta = math.atan(
                (M1.y - M2.y) / (M1.x - M2.x)
            )
        else:
            theta = math.pi / 2
        return theta

    if M1.x >= M2.x and M1.y <= M2.y:
        if M1.x - M2.x != 0:
            theta = math.atan(
                (M1.y - M2.y) / (M1.x - M2.x)
            ) + math.pi
        else:
            theta = math.pi/2
        return theta

    if M1.x >= M2.x and M1.y >= M2.y:
        if M1.x - M2.x != 0:
            theta = math.atan(
                (M1.y - M2.y) / (M1.x - M2.x)
            ) + math.pi
        else:
            theta = 3/2 * math.pi
        return theta

    if M1.x <= M2.x and M1.y >= M2.y:
        if M1.x - M2.x != 0:
            theta = math.atan(
                (M1.y - M2.y) / (M1.x - M2.x)
            ) + 2 * math.pi
        else:
            theta = 3/2 * math.pi
        return theta


class Mass:
    def __init__(self, canvas, x, y, m, color="red", radius=25):
        global masses
        masses.append(self)

        self.canvas = canvas
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

        self.mass = m

        self.radius = radius

        self.sprite = self.canvas.create_oval(self.x - self.radius, H - self.y - self.radius,
                                              self.x + self.radius, H - self.y + self.radius,
                                              fill=color)

    def draw(self):
        self.canvas.coords(self.sprite, self.x - self.radius, H - self.y - self.radius,
                           self.x + self.radius, H - self.y + self.radius)

    def update_physics(self, d_time):
        self.x += self.vx * d_time
        self.y += self.vy * d_time

        self.vx += self.ax * d_time
        self.vy += self.ay * d_time

        self.ax = 0
        self.ay = 0


class Spring:
    def __init__(self, canvas, M1, M2, spring_const, equilibrium_length):
        global springs
        springs.append(self)

        self.canvas = canvas

        self.M1 = M1
        self.M2 = M2

        self.spring_const = spring_const
        self.equilibrium_length = equilibrium_length

        self.length = 0
        self.calculate_length()

        self.sprite = self.canvas.create_line(self.M1.x, H - self.M1.y, self.M2.x, H - self.M2.y, width=5)

    def calculate_length(self):
        self.length = math.sqrt(
            (self.M1.x - self.M2.x)**2 +
            (self.M1.y - self.M2.y)**2
        )

    def draw(self):
        self.canvas.coords(self.sprite, self.M1.x, H - self.M1.y, self.M2.x, H - self.M2.y)

    def update_physics(self, d_time):
        self.calculate_length()
        force = - self.spring_const * abs(self.length - self.equilibrium_length)

        theta = calculate_angle(self.M1, self.M2)

        self.M1.ax += -force * math.cos(theta) / self.M1.mass
        self.M1.ay += -force * math.sin(theta) / self.M1.mass

        self.M2.ax += force * math.cos(theta) / self.M2.mass
        self.M2.ay += force * math.sin(theta) / self.M2.mass


m1 = Mass(c, W/2, H/2, 2, color="maroon")
m2 = Mass(c, W/2 + 120, H/2, 1)
m3 = Mass(c, W/2 - 50, H/2 + 170, 1)

Spring(c, m1, m2, 2, 100)
Spring(c, m2, m3, 1, 100)
Spring(c, m1, m3, 2, 100)

while True:
    for m in masses:
        m.update_physics(0.01)

    for s in springs:
        s.update_physics(0.01)

    for m in masses:
        m.draw()

    for s in springs:
        s.draw()

    root.update_idletasks()
    root.update()
