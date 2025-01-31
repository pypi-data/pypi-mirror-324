import sys; sys.path.append('src')

from zyxxy2 import *



create_canvas_and_axes(canvas_width=30, canvas_height=30, tick_step=1)

r2 = draw_a_rectangle(left=20, bottom=20, width=4, height=6, color='blue')
i = 0
def check():
   # wait_for_enter()
   global i
   i += 1
   print(i, r2.diamond_names, r2.diamond_coords, r2.get_xy())

check()
r2.width=8
check()
r2.width=5
check()
r2.left=20
check()
show_and_save()
