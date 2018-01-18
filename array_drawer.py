import turtle

def preglednica(dolzina, nx, ny):
    wy = dolzina/ny
    wx = dolzina/nx
    
    t = turtle.Turtle()
    t.penup()
    t.setpos(-350,350)
    t.pendown()
    
    t.forward(dolzina)
    t.right(90)
    t.forward(dolzina)
    t.right(90)
    t.forward(dolzina)
    t.right(90)
    t.forward(dolzina)
    t.right(90)

    for _ in range(nx-1):
        t.forward(wx)
        t.right(90)
        t.forward(dolzina)
        t.back(dolzina)
        t.left(90)

    t.forward(wx)
    t.right(90)
    
    for _ in range(ny-1):
        t.forward(wy)
        t.right(90)
        t.forward(dolzina)
        t.back(dolzina)
        t.left(90)

    t.forward(wy)
    t.penup()
    t.forward(500)
        

preglednica(350, 4, 4)
