The pdf in this repo has information on the math behind the physics. This file will talk about how the code works.

The code starts with some basic imports and setting up variables. The root variable and c (canvas) variable are used by tkinter, the graphics drawing library.

```python
import tkinter as tk
import time
import math

H, W = 480, 640

masses = []
springs = []

root = tk.Tk()
c = tk.Canvas(root, height=H, width=W, bg="gray")
c.pack()
```

I've defined two functions to calculate physical values that we will need. They both take in two mass classes which have properties for their x and y position

```python
def calculate_length(M1, M2):
    length = math.sqrt(
        (M1.x - M2.x) ** 2 +
        (M1.y - M2.y) ** 2
    )
    return length


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
```

This is just basic algebra and trig to find lengths and angles.

Next is the Mass class, which represents a point mass .

```python
class Mass:
    def __init__(self, canvas, x, y, m, color="red", radius=25, show_forces=False):
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

        self.show_forces = show_forces

        if self.show_forces:
            self.force_arrow = self.canvas.create_line(self.x, H - self.y, self.x + self.ax * self.mass,
                                                       H - self.y - (self.ay * self.mass), fill="green", width=10)
```

It has properties for its position, velocity, and acceleration in terms of x and y. It also has a mass m. THe radius and sprite variables are for drawing the object. We can also decide if we want to show the forces on the mass when we draw it.

The draw funciton is simple, it just updates the coordinates of the sprite.

```python
    def draw(self):
        self.canvas.coords(self.sprite, self.x - self.radius, H - self.y - self.radius,
                           self.x + self.radius, H - self.y + self.radius)

        if self.show_forces:
            self.canvas.coords(self.force_arrow, self.x, H - self.y, self.x + self.ax * self.mass, H - self.y - (self.ay * self.mass))
```

The physics update function is also simple, we just increment position by velocity and increment velocity by acceleration. We need to multiply by the step value or delta time. The acceleration is reset each time because we need to recalculate it each time the displacement of a spring changes.

```python
    def update_physics(self, d_time):
        self.x += self.vx * d_time
        self.y += self.vy * d_time

        self.vx += self.ax * d_time
        self.vy += self.ay * d_time

        self.ax = 0
        self.ay = 0
```

We also have a class for a spring between two masses. It has four physical properties. Two masses on it's ends, a spring constant, and an equilibrium length. 

```python
class Spring:
    def __init__(self, canvas, M1, M2, spring_const, equilibrium_length):
        global springs
        springs.append(self)

        self.canvas = canvas

        self.M1 = M1
        self.M2 = M2

        self.spring_const = spring_const
        self.equilibrium_length = equilibrium_length

        self.length = calculate_length(self.M1, self.M2)

        self.sprite = self.canvas.create_line(self.M1.x, H - self.M1.y, self.M2.x, H - self.M2.y, width=5)
```

The physics for the spring is also pretty basic. With Hooke's law we know that the force is negative the spring constant times the displacement of the spring. We convert this to acceleration for each mass by dividing by the mass, and then we split the acceleration into components by multiplying by the corresponding trig function of the angle between the masses.

```python
    def update_physics(self, d_time):
        force = - self.spring_const * (calculate_length(self.M1, self.M2) - self.equilibrium_length)

        theta = calculate_angle(self.M1, self.M2)

        self.M1.ax += -force * math.cos(theta) / self.M1.mass
        self.M1.ay += -force * math.sin(theta) / self.M1.mass

        self.M2.ax += force * math.cos(theta) / self.M2.mass
        self.M2.ay += force * math.sin(theta) / self.M2.mass
```

We can know define some masses and springs:

```python
m1 = Mass(c, W/2, H/2, 1, show_forces=False)
m2 = Mass(c, W/2 + 120, H/2, 1, show_forces=False)
m3 = Mass(c, W/2 - 50, H/2 + 170, 1, show_forces=False)

Spring(c, m1, m2, 1, 100)
Spring(c, m2, m3, 1, 100)
Spring(c, m1, m3, 1, 100)
```

And then we can loop the physics functions and draw functions and watch our simulation!

```python

while True:
    total_energy = 0

    for m in masses:
        m.update_physics(0.01)
        total_energy += m.calculate_energy()

    for s in springs:
        s.update_physics(0.01)
        total_energy += s.calculate_energy()

    for m in masses:
        m.draw()

    for s in springs:
        s.draw()

    print(total_energy)

    root.update_idletasks()
    root.update()
```

If you want to make your own graphics program with python, use tkinter, specifically the canvas widget and the coords function to draw and update sprites.
