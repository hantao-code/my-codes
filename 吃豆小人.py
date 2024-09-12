from random import choice
from turtle import *
import pygame
from freegames import floor, vector

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(10, 0)  # 增加了速度，因为方块大小变大了
pacman = vector(-80, -160)
ghosts = [
    [vector(-360, 320), vector(10, 0), 'B'],
    [vector(-360, -320), vector(0, 10), 'P'],
    [vector(200, 320), vector(0, -10), 'i'],
    [vector(200, -320), vector(-10, 0), 'C'],
]
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on

def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(40)  # 增大方块大小
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 40) + 400) / 40  # 调整偏移量
    y = (360 - floor(point.y, 40)) / 40  # 调整偏移量
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 39)

    if tiles[index] == 0:
        return False

    return point.x % 40 == 0 or point.y % 40 == 0


def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 40 - 400  # 调整坐标
            y = 360 - (index // 20) * 40  # 调整坐标
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 20, y + 20)
                path.dot(4, 'white')  # 调整点的大小


def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'], align="right", font=("Arial", 14, "normal"))

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 40 - 400
        y = 360 - (index // 20) * 40
        square(x, y)

    up()
    goto(pacman.x + 20, pacman.y + 20)
    dot(40, 'yellow')  # 调整点的大小

    for point, course, name in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
            ]

            plan = choice(options)
            course.x = plan.x
            course.y =plan.y

        up()
        goto(point.x + 20, point.y + 20)
        dot(40, 'red')  # 调整点的大小
        goto(point.x + 10, point.y + 10)
        color('white')
        write(name, align="center", font=("Arial", 10, "normal"))  # 显示鬼的名字

    update()

    for point, course, name in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 150)


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(820, 820, 370, 0)  # 调整窗口大小
hideturtle()
tracer(False)
writer.goto(160, 360)  # 调整分数位置
writer.color('white')
writer.write(state['score'], align="right", font=("Arial", 14, "normal"))
listen()
onkey(lambda: change(40, 0), 'Right')  # 调整移动步长
onkey(lambda: change(-40, 0), 'Left')  # 调整移动步长
onkey(lambda: change(0, 40), 'Up')  # 调整移动步长
onkey(lambda: change(0, -40), 'Down')  # 调整移动步长
world()
move()
done()
