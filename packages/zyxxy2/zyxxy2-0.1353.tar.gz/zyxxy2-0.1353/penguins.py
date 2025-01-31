import sys; sys.path.append('src')

import numpy as np

from zyxxy2 import *

def draw_a_semicircle(turn, **kwargs):
  return draw_a_sector(angle_start=turn, angle_end=turn+6, **kwargs)

#########################################################
## THE PENGUINS                                        ##
#########################################################
def example_penguins(model="https://i.pinimg.com/564x/fc/90/7d/fc907dc3638cfd64aa2c3ba56e216b92.jpg",
                     snowflakes_qty=150, ice_shards_qty=800, sas=True):
  
  def draw_orange_semicircle(turn, **kwargs):
    return draw_a_semicircle(turn=turn, radius=6, color='orangered', **kwargs)

  def draw_big_semicircle(turn, **kwargs):
    return draw_a_semicircle(turn=turn, radius=30, **kwargs)

  def draw_head_and_eyes(center_x_head, centers_x_eyes):
    # head
    draw_a_circle(diamond=[center_x_head, 80], radius=15, color='black')
    # eyes
    for center_x_eyes in centers_x_eyes:
      draw_a_circle(diamond=[center_x_eyes, 85], radius=3, color=None, outline_color='white', outline_linewidth=5)
  #######################################################
  # Creating the canvas!                               ##  
  create_canvas_and_axes(canvas_width=320,
                                canvas_height=180,
                                #title="Penguin Conversation",
                                #tick_step = 10,
                                #model=model,
                                background_color='lightskyblue')

  #######################################################
  # Now let's draw the shapes!                         ##
  # snowflakes
  
  ice_colors = ['aliceblue', 'steelblue', 'skyblue']
  for _ in range(ice_shards_qty):
    draw_a_triangle(tip=random_point_on_axes(y_max=35),
                    height=random_number(15, 30), 
                    width=random_number(8, 15), 
                    turn=random_number(2, 10),
                    color = random_element(ice_colors)) 
    
  snowflakes = [draw_a_star(diamond=random_point_on_axes(y_max=180+90/3), 
                            radius_1=1, radius_2=3, ends_qty=8, color='aliceblue')
                                                      for _ in range(snowflakes_qty)]

  # penguins!

  # the penguin on the right
  # first foot 
  draw_orange_semicircle(diamond=[270, 16], turn=9)
  # body - white
  draw_big_semicircle(diamond=[280, 50], color='white', turn=5)
  # second foot 
  draw_orange_semicircle(diamond=[280, 15], turn=8)
  # body - black
  draw_big_semicircle(diamond=[290, 50], color='black', turn=5)
  # beck
  draw_orange_semicircle(diamond=[255, 75], turn=8 + 1/2)
  # head and an eye
  draw_head_and_eyes(center_x_head=270, centers_x_eyes=[263])

 # the penguin on the left
  # body
  draw_a_circle(diamond=[60, 45], radius=25, color='white')
  # feet
  draw_orange_semicircle(diamond=[54, 16], turn=8.5)
  draw_orange_semicircle(diamond=[66, 16], turn=9.5)
  # head and the eyes
  draw_head_and_eyes(center_x_head=60, centers_x_eyes=[55, 65])
  # wings
  right_wing = draw_big_semicircle(diamond=[31, 60], color='black', turn=2)
  left_wing = draw_big_semicircle(diamond=[89, 60], color='black', turn=4)
  # beck
  draw_an_elliptic_sector(diamond=[58, 76], angle_start=0, angle_end=3, height=12, width=18, turn=0.5, color='orangered')

  set_default_text_style(linewidth=5, fontsize=20, triangle_width=8)
  text_right = draw_a_speech_bubble(text="Where is fish?", x =180, y=120, position='lt', start=[240, 85], background_color='white')
  text_left = draw_a_speech_bubble(text="I don't know...",x=140, y=120, position='rt', start=[ 82, 85], background_color='white')

  if sas:
    show_and_save()
  return snowflakes, left_wing, right_wing, text_left, text_right

#########################################################
def penguins_animation():

  snowflakes, left_wing, right_wing, text_left, text_right = \
    example_penguins(model=None, sas=False)

  wing_diamond = (60, 75)

  left_wing.turn( 0.25, diamond_override=wing_diamond)
  right_wing.turn(-0.25, diamond_override=wing_diamond)

  # fish_layer = new_layer()
  # make_layers_invisible(fish_layer)

  snowflake_shift=1/3
  frames_qty=102

  for snowflake in snowflakes:
      snowflake.shift_y(-snowflake_shift*frames_qty)

  def init_func():
    for snowflake in snowflakes:
      snowflake.shift_y(snowflake_shift*frames_qty)

  def animate(i):
    for snowflake in snowflakes:
      snowflake.shift_y(-snowflake_shift)
    if i == 0:
      text_left.make_invisible()
      text_right.make_visible()
      text_right.set_text("Where         ")
    if i == 12:
      text_right.set_text("Where is      ")
    if i == 24:
      text_right.set_text("Where is fish?")
    if i == 48:
      text_right.make_invisible()
      text_left.make_visible()
    if i >= 72:
      turn = -1/30 if i < 87 else 1/30
      left_wing.turn( turn, diamond_override=wing_diamond)
      right_wing.turn(-turn, diamond_override=wing_diamond)

  show_and_save(animation_func=animate, animation_init=init_func, nb_of_frames=frames_qty)

  #  animation_interval=100)

##################################################################################################################

penguins_animation() # example_penguins() # 