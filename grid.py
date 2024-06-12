import MicroTurtle
from MicroTurtle import Turtle



def CreateGrid(x1 = -200,y1 = -200,x2 = 200,y2 = 200,gap=(),pos=(0,0)):


    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    turtle.speed(0)
    #CreateBackGround(x1,y1,x2,y2)
    
    turtle.hideturtle() 

    turtle.penup()

    Rows = Turtle()
    Cols = Turtle()

    Rows.speed(0)
    Cols.speed(0)


    gridCol = []
    gridRows = []

    Cols.hideturtle()
    Rows.hideturtle() 
    
    Cols.penup()
    Rows.penup()
    Rows.goto(x1,y2)
    Cols.goto(x2,y2)
    Cols.pendown()
    Rows.pendown()
    turtle.pendown()
    Rows.goto(x2,y2)
    Cols.goto(x2,y1)



    for x in range(x1,x2,int(gap[0])):
        #turtle.penup()
        gridRows.append('up')

        #turtle.goto(x,y)
        gridRows.append((x+pos[0],y1+pos[1]))
        gridRows.append('down')
        gridRows.append((x+pos[0],y2+pos[1]))
        #turtle.pendown()

    for y in range(y1,y2,int(gap[1])):
        #turtle.penup()
        gridRows.append('up')

        #turtle.goto(x,y)
        gridRows.append((x1,y))
        gridRows.append('down')
        gridRows.append((x2,y))
        #turtle.pendown()

    for i in range(len(gridRows)):
        if i >= len(gridRows):
            row = "up"
        else:
            row = gridRows[i]
        if i >= len(gridCol):
            col = "up"
        else:
            col = gridCol[i]
        
        if row == "up":
            Rows.penup()
        elif row == "down":
            Rows.pendown()
        else:
            x,y = row
            while x > x2:
                x = x-x2
            Rows.goto(x,y)
            
        if col == "up":
            Cols.penup()
        elif col == "down":
            Cols.pendown()
        else:
            x,y = col
            Cols.goto(x,y)
def CreateBackGround(x1,y1,x2,y2):
    turtle.color("black")
    turtle.Screen().bgcolor("black")
    turtle.fillcolor("white")
    turtle.penup()
    turtle.goto(x1,y1)
    turtle.pendown()
    turtle.begin_fill()
    turtle.goto(x2,y1)
    turtle.goto(x2,y2)
    turtle.goto(x1,y2)
    turtle.goto(x1,y1)
    turtle.end_fill()
if __name__ == '__main__':
    CreateGrid()
