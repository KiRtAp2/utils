import turtle

def array(length, nx, ny):
    wy = length/ny
    wx = length/nx
    
    t = turtle.Turtle()
    t.penup()
    t.setpos(-350,350)
    t.pendown()
    
    t.forward(length)
    t.right(90)
    t.forward(length)
    t.right(90)
    t.forward(length)
    t.right(90)
    t.forward(length)
    t.right(90)

    for _ in range(nx-1):
        t.forward(wx)
        t.right(90)
        t.forward(length)
        t.back(length)
        t.left(90)

    t.forward(wx)
    t.right(90)
    
    for _ in range(ny-1):
        t.forward(wy)
        t.right(90)
        t.forward(length)
        t.back(length)
        t.left(90)

    t.forward(wy)
    t.penup()
    t.forward(500)
        

array(350, 4, 4)
