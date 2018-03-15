import turtle

n = 5
start_size = 800

turtle.penup()

def draw_triangle(dist, rep):
	turtle.forward(dist)
	turtle.left(120)
	turtle.forward(dist)
	turtle.left(120)
	turtle.forward(dist)
	turtle.left(120)
	
	if rep > 0:
		new_dist = dist/2
		draw_triangle(new_dist, rep-1)
		turtle.forward(new_dist)
		draw_triangle(new_dist, rep-1)
		turtle.left(120)
		turtle.forward(new_dist)
		turtle.right(120)
		draw_triangle(new_dist, rep-1)
		turtle.right(120)
		turtle.forward(new_dist)
		turtle.left(120)

turtle.setpos(-350, -350)
turtle.pendown()

draw_triangle(start_size, n)

while True:
	pass