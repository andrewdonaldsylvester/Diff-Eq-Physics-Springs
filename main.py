import tkinter as tk
import time
import math

H, W = 480, 640

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
        force = - self.spring_const * (self.length - self.equilibrium_length)

        theta = calculate_angle(self.M1, self.M2)
        # print(theta)

        self.M1.ax += -force / self.M1.mass * math.cos(theta)
        self.M1.ay += -force / self.M1.mass * math.sin(theta)

        self.M2.ax += force / self.M2.mass * math.cos(theta)
        self.M2.ay += force / self.M2.mass * math.sin(theta)


m1 = Mass(c, W/2, H/2 + 100, 1)
m2 = Mass(c, 100, H/2, 1, color="blue")
m3 = Mass(c, 250, H/2 - 100, 1, color="green")

s1 = Spring(c, m2, m3, 1, 200)
s2 = Spring(c, m1, m3, 1, 200)
s3 = Spring(c, m1, m2, 1, 200)

while True:
    m1.update_physics(0.01)
    m2.update_physics(0.01)
    m3.update_physics(0.01)

    s1.update_physics(0.01)
    s2.update_physics(0.01)
    s3.update_physics(0.01)

    m1.draw()
    m2.draw()
    m3.draw()

    s1.draw()
    s2.draw()
    s3.draw()

    root.update_idletasks()
    root.update()
