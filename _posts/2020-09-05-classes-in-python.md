---
layout: post
title: Learning Classes in Python
date: 2020-09-05
tag:
 - dev
---

I am currently learning python having used a few scripts in some Github Actions to automated some processes using the free serverless compute offered by GitHub.

Having got a few scripts up and running I now want to progress a little more and learn some OOP.

so lets create a class and call it `Polygon`.

``` Python
class Polygon:
```

to instantiate the class we need to user a double under notation (known as dunder).

``` Python
class Polygon:
    def __init__(self, sides, name, size=100, color="blue", line_thickness=4):
```

Lets give our shapes some attributes: size, length etc. Note the use of self as the first item in the brackets.

``` Python
class Polygon:
    def __init__(self, sides, name, size=100, color="blue", line_thickness=4):
        self.sides = sides
        self.name = name
        self.size = size
        self.color = color
        self.line_thickness = line_thickness
        self.interior_angles = (self.sides - 2)*180
        self.angle = self.interior_angles/self.sides
```

In the above snippet we have assigned variables and does some geometry.

Next we will create a method called `draw`

``` Python
    def draw(self):
        turtle.begin_fill()
        turtle.color(self.color)
        turtle.pensize(self.line_thickness)
        for i in range(self.sides):
            turtle.forward(self.size)
            turtle.right(180 - self.angle)
        turtle.end_fill()
```

Note the use of turtle here, which is a packaged that can be used for drawing items. At the top of the file we'll include the package

``` Python
import turtle
```

And thats our class, before we get in to running some code to actually draw our shapes, lets make the `Polygon` class a super class and inherit it from a specific shape `Square`

``` Python
class Square(Polygon):
    def __init__(self):
        super().__init__(4, "square")
```

Notice the polygon in brackets and the use of `super()` which essentially says initiate the parent class. We pass in the `4` and the name `square` the rest of the values are default in the super class.

we add to the `square` class another method to draw, which inherits from the super class too.

``` Python
class Square(Polygon):
    def __init__(self):
        super().__init__(4, "square")

    def draw(self):
        super().draw()
```

So to draw a polygon and a square we can use

``` Python

shape = Polygon(6, "hexagon", color="pink")
shape.draw()
turtle.done()

square = Square()
square.draw()
turtle.done()

```

The `turtle.done()` call keeps the drawn item on screen like how `console.read()` would do the same in C#.

Square doesn't need any attributes passed in so works just fine with the defaults in its class and the parent class.

Shape, is given 6 sides and named hexagon and an override of the default colour.

That is [python classes](https://github.com/MatBenfiled/demo_python).
