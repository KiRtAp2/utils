import turtle

n = 5
start_len = 600

turtle.penup()
turtle.setpos(-300, 200)

turtle.pendown()

def side(l, depth):
	if depth <= 0:
		turtle.forward(l)
	else:
		new_l = l/3
		side(new_l, depth-1)
		turtle.left(60)
		side(new_l, depth-1)
		turtle.right(120)
		side(new_l, depth-1)
		turtle.left(60)
		side(new_l, depth-1)

side(start_len, n)
turtle.right(120)
side(start_len, n)
turtle.right(120)
side(start_len, n)

while True:
	pass