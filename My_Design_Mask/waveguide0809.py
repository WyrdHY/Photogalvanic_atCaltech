import nazca as nd
import numpy as np


######for layer1 
wg_length = 15000
wg_width =50 
layer1 = (1,0)
radius = 100000 / 2
filename = r"D:\Caltech\Mask\My_Design\test.gds"
# Define the outer square (side = 20,000)
outer_square = [
    (-10000, -10000),
    (10000, -10000),
    (10000, 10000),
    (-10000, 10000),
    (-10000, -10000)
]

# Define the inner square (side = 18,000)
inner_square = [
    (-9000, -9000),
    (9000, -9000),
    (9000, 9000),
    (-9000, 9000),
    (-9000, -9000)
]

# Reverse the direction of the inner square to perform the subtraction
frame_points = outer_square + inner_square[::-1]

with nd.Cell("safe_zone") as safe_zone:
    nd.Polygon(layer=layer1, points=frame_points).put()

with nd.Cell("5pac") as five_wave: #overall cell width is 370
    for i in range(5):
        x_loc = i*80
        nd.strt(length=wg_length, width=wg_width,layer=layer1).put(x_loc, 0,90)

with nd.Cell("disk") as disk:
    nd.bend(radius=100000/2, angle=360, width=100,layer=layer1).put(0, 0)

#Massively filled the square
with nd.Cell("one_square") as single:
    k = -8700
    while (k<9000-570):
        five_wave.put(k, -7500, align='center')
        k += 570
    safe_zone.put(0, 0, align='center')

'''
single.put(0,0)
disk.put(0,-50000) #place the center of the circle at (0,0)
#nd.export_gds(topcells=single, filename=filename)
nd.export_plt()
'''

# Create the filling cell with "single" cells
with nd.Cell("filled_disk") as filled_disk:
    grid_step = 20000  # Assuming the width of "single" is 370 units
    for x in np.arange(-radius, radius, grid_step):
        for y in np.arange(-radius, radius, grid_step):
            if x**2 + y**2 <= (radius-15000)**2:  # Check if the center is inside the circle
                single.put(x, y, align='center')

with nd.Cell("ultimate_fucker") as ultimate_fucker:
    filled_disk.put(0, 0)
    disk.put(0, -50000)

#Silk layer
text_content = "substrate thickness \n = 500nm"   
with nd.Cell("wafer_thickness_label") as subthickness:
    nd.text(text=text_content, height=1000 , layer=layer1).put(0, 0)

ultimate_fucker.put(0,0)
subthickness.put(-32000,30000)
# Export the design to a GDS file or plot it
#nd.export_gds(filename=filename)
#nd.export_plt()
'''
########################### Flipped the color and uncolored region for layer1 into another layer coded as (3,0)
layer1 = (3,0)

with nd.Cell("safe_zone") as safe_zone:
    nd.Polygon(layer=layer1, points=frame_points).put()

with nd.Cell("5pac") as five_wave: #overall cell width is 370
    for i in range(5):
        x_loc = i*80
        nd.strt(length=wg_length, width=wg_width,layer=layer1).put(x_loc, 0,90)

with nd.Cell("disk") as disk:
    nd.bend(radius=100000/2, angle=360, width=100,layer=layer1).put(0, 0)

#Massively filled the square
with nd.Cell("one_square") as single:
    k = -8700
    # Define the main area (victim) that will be subtracted from
    victim = nd.Polygon(layer=layer1, points=inner_square)
    
    # Initialize the current_area as the victim
    current_area = victim
    
    while k < 9000 - 570:
        # Define the area to subtract
        subtract_cell = five_wave  # Reference the five_wave cell directly
        subtract = subtract_cell.put(k, -7500, align='center')
        
        # Perform the subtraction
        current_area = nd.diff(current_area, subtract_cell)
        
        k += 570
    
    # Place the final shape in the safe_zone cell
    current_area.put(0, 0, align='center')
    safe_zone.put(0, 0, align='center')

# Create the filling cell with "single" cells
with nd.Cell("filled_disk") as filled_disk:
    grid_step = 20000  # Assuming the width of "single" is 370 units
    for x in np.arange(-radius, radius, grid_step):
        for y in np.arange(-radius, radius, grid_step):
            if x**2 + y**2 <= (radius-15000)**2:  # Check if the center is inside the circle
                single.put(x, y, align='center')

with nd.Cell("ultimate_fucker") as ultimate_fucker:
    filled_disk.put(0, 0)
    disk.put(0, -50000)

#Silk layer
text_content = "substrate thickness \n = 500nm"   
with nd.Cell("wafer_thickness_label") as subthickness:
    nd.text(text=text_content, height=1000 , layer=layer1).put(0, 0)

ultimate_fucker.put(0,0)
subthickness.put(-32000,30000)

'''










#############################################################################################for layer2
wg_length = 15000
wg_width =50 
layer2 = (2,0)
radius = 100000 / 2
#filename = r"D:\Caltech\Mask\My_Design\test.gds"

a=0
bitch=0.5
core=15
execution_list = np.arange(500,3600,100)/1000
counter = 0 
side_length = 100


with nd.Cell("safe_zone") as safe_zone:
    nd.Polygon(layer=layer2, points=frame_points).put()
    

'''
with nd.Cell("5pac") as five_wave: #overall cell width is 370
    for i in range(5):
        x_loc = i*80
        nd.strt(length=wg_length, width=core).put(0, 0,90, align='center')
        nd.strt(length=wg_length, width=bitch).put(core/2+5, 0,90, align='center')
        nd.strt(length=wg_length, width=bitch).put(-core/2-5, 0,90, align='center')
'''

def neighbourhood(coree, bitch, wg_length, cell_name,layer=(2,0)):
    delta = (wg_width/2-coree/2)/2+coree/2+3

    with nd.Cell(cell_name) as five_wave:
        for i in range(5):
            x_loc = i * 80
            nd.strt(length=wg_length, width=coree, layer=layer).put(x_loc, 0, 90, align='center')
            nd.strt(length=wg_length, width=bitch, layer=layer).put(x_loc+delta, 0, 90, align='center')
            nd.strt(length=wg_length, width=bitch, layer=layer).put(x_loc-delta, 0, 90, align='center')

        text_content = f"{bitch} um"
        nd.text(text=text_content, height=80, layer=layer, align='cc').put(2*80, wg_length + 100, 0)    
    return five_wave


with nd.Cell("disk") as disk:
    nd.bend(radius=100000/2, angle=360, width=100,layer=layer2).put(0, 0)

counter = 0 
#alignment marker
with nd.Cell("square") as square_cell:
    nd.Polygon(points=[
        (-side_length/2, -side_length/2),  # Bottom-left corner
        (side_length/2, -side_length/2),   # Bottom-right corner
        (side_length/2, side_length/2),    # Top-right corner
        (-side_length/2, side_length/2),   # Top-left corner
        (-side_length/2, -side_length/2)   # Closing the polygon
    ], layer=layer2).put(0, 0)
with nd.Cell("alignment") as align:
    square_cell.put(-100,100)
    square_cell.put(100,100)
    square_cell.put(-100,-100)
    square_cell.put(100,-100)




#Filled one square
with nd.Cell("one_square") as single:
    k = -8700
    while (k<9000-570):
        bitch = execution_list[counter]
        neighbourhood(core,bitch,wg_length,layer=layer2,cell_name=str(counter)).put(k, -7500, align='center')
        k += 570
        counter+=1
    safe_zone.put(0, 0, align='center')
    align.put(-8500,8500)
    align.put(8500,8500)

    align.put(-8500,-8500)
    align.put(8500,-8500)
#print(f'The number of 5pacs is {counter}.')

with nd.Cell("filled_disk") as filled_disk:
    grid_step = 20000
    for x in np.arange(-radius, radius, grid_step):
        for y in np.arange(-radius, radius, grid_step):
            if x**2 + y**2 <= (radius-15000)**2:
                single.put(x, y, align='center')

with nd.Cell("ultimate_fucker") as ultimate_fucker:
    filled_disk.put(0, 0)
    disk.put(0, -50000)

text_content = "substrate thickness \n = 500nm"   
with nd.Cell("wafer_thickness_label") as subthickness:
    nd.text(text=text_content, height=1000 , layer=layer2).put(0, 0)

ultimate_fucker.put(0,0)
subthickness.put(-32000,30000)

nd.export_gds(filename=filename)