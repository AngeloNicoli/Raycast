import numpy as np
import math
from tkinter import *
import os  

# Create Column 
n_rows = 10
n_columns = 10

#x = np.arange(100).reshape(n_rows,n_columns)
#print(type((x[2][3])))

Player_Angle = [0]
Player_coord = [0]
Player_center = [0]
Player_size = [20]
Player_Ray = []
Ray_size =[100]

path="Map.txt" 

if os.path.isfile(path):  
    print("\n File exist")  
else:  
    x = np.zeros(n_rows*n_columns).reshape(n_rows,n_columns)   # Inizialize Map
    x[4][5] = 1 
    x[3][7] = 1
    x[3][2] = 2
    np.savetxt("Map.txt", x, delimiter=',')
    #print(x)
    #print("File does not exist")


x = np.loadtxt("Map.txt" , dtype="U", delimiter=",", quotechar='"')
#print(y)
#print(type(y))
#print(type((y[2][3])))

x = x.astype(float)
x = x.astype(int)
#print(type((y[2][3])))

#y = np.zeros(100).reshape(10,10)
#print(y)

Canvas_Coord = np.zeros(100).reshape(n_rows,n_columns)
x_entry = {}

#y[6][5] = 8
#print(y)

# Size of Main Window
master = Tk()
master.title("Raycast 2D")
master.configure(bg="#3e3e42")  

# Size of Canvas and pixel 
canvas_width = 600
canvas_height = 600
pixel_size = 60
n_pixel_x = canvas_width/pixel_size
n_pixel_y = canvas_height/pixel_size

def Map_Draw():
    global Player_coord
    for row_counter in range(n_rows):
        #print(str(row_counter))
        for col_counter in range(n_columns):
            #print(col_counter)
            if x[row_counter][col_counter] == 0:
                Canvas_Coord[row_counter][col_counter] = Main_Canvas.create_rectangle((row_counter*pixel_size),(col_counter*pixel_size),(row_counter*pixel_size)+ pixel_size,(col_counter*pixel_size) + pixel_size,width = 1, fill = "white" ,outline='black'  ,tags= str(row_counter) + str(col_counter))
            elif x[row_counter][col_counter] == 1:
                Canvas_Coord[row_counter][col_counter] = Main_Canvas.create_rectangle((row_counter*pixel_size),(col_counter*pixel_size),(row_counter*pixel_size)+ pixel_size,(col_counter*pixel_size) + pixel_size,width = 1, fill = "green" ,outline='black' ,tags= str(row_counter) + str(col_counter)) 
            elif x[row_counter][col_counter] == 2:
                Player_center = [((row_counter+0.5)*pixel_size),((col_counter+0.5)*pixel_size)]
                Canvas_Coord[row_counter][col_counter] = Main_Canvas.create_oval(Player_center[0]- Player_size[0],Player_center[1] - Player_size[0],Player_center[0]+ Player_size[0], Player_center[1]+ Player_size[0],width = 1, fill = "red" ,outline='black' ,tags= "Player") 
                Player_coord = [(row_counter),(col_counter)]
                #print("Player Coordinates are" + str(Player_coord))
                Player_Ray = [Player_center[0],Player_center[1],Player_center[0] + Ray_size[0] * math.cos(Player_Angle[0]), Player_center[1]+ Ray_size[0] * math.sin(Player_Angle[0])]
                Main_Canvas.delete("Raycast")
                Ray = Main_Canvas.create_line(Player_Ray,tags= "Raycast",width=3) 
                Raycaster(Player_Ray)
            elif x[row_counter][col_counter] == 3:
                 Canvas_Coord[row_counter][col_counter] = Main_Canvas.create_rectangle((row_counter*pixel_size),(col_counter*pixel_size),(row_counter*pixel_size)+ pixel_size,(col_counter*pixel_size) + pixel_size,width = 1, fill = "Blue" ,outline='black' ,tags= str(row_counter) + str(col_counter)) 
        
        Main_Canvas.tag_raise("Raycast")
        Main_Canvas.tag_raise("Ray")

def Save():
    np.savetxt("Map.txt", x, delimiter=',')

def data_table():
    top = Toplevel()
    Change_Value = Button(top, text="Change",bg="white", command=lambda :Update_Destroy(top))
    Change_Value.grid(row=11, column=0)

    for n in range(n_rows):
        x_entry["Row"+str(n)] = [None]*10
        for i in range(n_columns):
            x_entry["Row"+str(n)][i]= Entry(top, width=10)
            x_entry["Row"+str(n)][i].insert(0, x[i][n])
            x_entry["Row"+str(n)][i].grid(row=n, column=i)
    #print(x_entry)
    #print(type(x_entry))


def Ray_intersection(Ray,Line):
    global Main_Canvas
    #print("Ray vale" + str(Ray))
    #print("Line vale" + str(Line))      
    x1,y1,x2,y2 = Ray
    x3,y3,x4,y4 = Line

    den = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))
    if den == 0:
        pass
        #print("Denominatore = 0")
                
    ua_num = ((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))
    ub_num = ((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))

    if den != 0:
        ua = ua_num / den
        ub = ub_num / den
        if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
            px = x1 + (ua * (x2 - x1))
            py = y1 + (ua * (y2 - y1))
           # print("intersezione" +str(px) +"," + str(py))  
        
            Main_Canvas.create_oval(px-5,py-5,px+5,py+5,tags= "Ray") 


def Raycaster(Ray):
    Main_Canvas.delete("Ray")
    for row_counter in range(n_rows):
        for col_counter in range(n_columns):
            if x[row_counter][col_counter] == 1:
                #print("Ho trovato il muro. Analizzo le coordinate")  
                Perimeter = [None] * 4
                Perimeter[0] = (row_counter*pixel_size),(col_counter*pixel_size),(row_counter*pixel_size)+pixel_size,(col_counter*pixel_size)
                Perimeter[1] = (row_counter*pixel_size),(col_counter*pixel_size)+pixel_size,(row_counter*pixel_size)+pixel_size,(col_counter*pixel_size+pixel_size)
                Perimeter[2] = (row_counter*pixel_size),(col_counter*pixel_size),(row_counter*pixel_size),(col_counter*pixel_size+pixel_size)
                Perimeter[3] = (row_counter*pixel_size)+pixel_size,(col_counter*pixel_size),(row_counter*pixel_size)+pixel_size,(col_counter*pixel_size+pixel_size)
                for j in range(4):
                    Line = Perimeter[j]
                    Ray_intersection(Ray,Line)
    #print("Il raggio ha coordinate" +str(Ray))
    pass

def Update_Destroy(top):
    global x_entry
    global x 
    for n in range(n_rows):
        for i in range(n_columns):
            #(x_entry["Row"+str(n)][i])
            x_entry["Row"+str(n)][i].get()
            #print(x_entry["Row"+str(n)][i].get())
            x[i][n] = x_entry["Row"+str(n)][i].get()
    Map_Draw()  
    #print(x)      
    top.destroy()


def Rotate_Player(Rotation_Type):
    global horizontal2
    Main_Canvas.delete("Player")
    Main_Canvas.delete("Raycast")

    Player_Angle[0] = math.radians(horizontal2.get())
    print(Player_Angle[0])
    Map_Draw()


def Move_Player(Direction_Player):
    Main_Canvas.delete("all")

    if Direction_Player ==1 and x[Player_coord[0]-1][Player_coord[1]] == 0:
        x[Player_coord[0]][Player_coord[1]] = 0
        Player_coord[0] -= 1
    elif Direction_Player ==2 and x[Player_coord[0]+1][Player_coord[1]] == 0:
        x[Player_coord[0]][Player_coord[1]] = 0
        Player_coord[0] += 1 
    elif Direction_Player ==3 and x[Player_coord[0]][Player_coord[1]+1] == 0:
        x[Player_coord[0]][Player_coord[1]] = 0
        Player_coord[1] += 1   
    elif Direction_Player ==4 and x[Player_coord[0]][Player_coord[1]-1] == 0:
        x[Player_coord[0]][Player_coord[1]] = 0
        Player_coord[1] -= 1      


    x[Player_coord[0]][Player_coord[1]] = 2
    #print("Player Coordinates are" + str(Player_coord))
    Map_Draw()
    pass

Main_Canvas = Canvas(master, width=canvas_width, height=canvas_height, bg="gray")
Main_Canvas.grid(row=0, column=3, rowspan=10,columnspan=7)

Text_Label = Label(master, text="Rotate Player",bg="gray")
Text_Label.grid(row=0, column=0, columnspan=3,padx=10,sticky=EW)

Coordinates_entry = Label(master, text="Raycast", bg="gray")
Coordinates_entry.grid(row=2, column=0, columnspan=3,padx=10,sticky=EW)



Player_Move_xm = Button(master, text="Move Left",bg="gray", command=lambda :Move_Player(1))
Player_Move_xm.grid(row=5, column=0, rowspan=1)

Player_Move_xp = Button(master, text="Move Right",bg="gray", command=lambda :Move_Player(2))
Player_Move_xp.grid(row=5, column=2, rowspan=1,)

Player_Move_ym = Button(master, text="Move Up",bg="gray", command=lambda :Move_Player(4))
Player_Move_ym.grid(row=4, column=1, rowspan=1,sticky=EW)

Player_Move_yp = Button(master, text="Move Down",bg="gray", command=lambda :Move_Player(3))
Player_Move_yp.grid(row=5, column=1, rowspan=1,sticky=EW)

Edit_Label = Label(master, text="Edit Map", bg="gray")
Edit_Label.grid(row=6, column=0, columnspan=3,padx=10,sticky=EW)

Save_Map = Button(master, text="Save_Map",bg="gray", command=Save)
Save_Map.grid(row=7, column=0, rowspan=1)

Edit_Map = Button(master, text="Edit Map",bg="gray", command=lambda :data_table())
Edit_Map.grid(row=7, column=1, rowspan=1)

Log_Label = Label(master, text="Additional Information ....",bg="gray", anchor=W)
Log_Label.grid(row=8, column=0,  columnspan=3, padx=10, sticky=EW)


def slide(v):
    Ray_size[0] = horizontal.get()
    #print(Ray_size[0])
    Map_Draw()
    pass

horizontal  = Scale(master,from_=10, to=300, orient=HORIZONTAL, command=slide)
horizontal.grid(row=3, column=0,columnspan=3, sticky=W+E, padx=20)
horizontal.set(100)

horizontal2  = Scale(master,from_=-360, to=360, orient=HORIZONTAL, command=Rotate_Player)
horizontal2.grid(row=1, column=0,columnspan=3, sticky=W+E, padx=20)
horizontal2.set(0)


Map_Draw()
mainloop()
