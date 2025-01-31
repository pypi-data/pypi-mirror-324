import datetime
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .canvas import prepare_axes, _find_scale_place_axes
from .word_bubbles import draw_a_speech_bubble
from .utils import random_integer_number, random_element # get_random_int

##########################################################################################
def _get_inspirations():
  inspirations = []
  p = Path(__file__).with_name('inspiration.txt')
  with p.open('r') as handle:
    for l in handle:
      inspirations.append(l.strip())
  return inspirations

inspirations = _get_inspirations()

def get_random_inspiration(name):
  insp = random_element(inspirations)
  if insp.startswith("You're") and random_integer_number(0, 1):
    insp = "You a"+ insp[4:]
  if random_integer_number(0, 1):
    if insp.startswith("You"):
      insp = f"{name}, y" + insp[1:]
    else:
      insp = insp[:-1] + f", {name}!"
  return insp
  
##########################################################################################
def get_all_children(parent=None):
  new_children = [parent if parent else plt.gcf()]
  result = []
  while new_children:
    new_new_children = []
    for c in new_children:
      new_new_children += c.get_children()
    new_new_children = [c for c in new_new_children if isinstance(c, (plt.Axes, matplotlib.patches.Patch, matplotlib.text.Text))]
    result = new_new_children + result
    new_children = new_new_children
  #result = plt.gca().get_children()
  return result

##########################################################################################
def remove_what_possible_except(what_to_keep):
  all_ = get_all_children()
  for c in all_:
    if c in what_to_keep:
      continue
    try:
      c.remove()
    except:
      pass # print(c)

##########################################################################################
def place_text(text, x, y, **kwargs):
  xlim = plt.gca().get_xlim() 
  ylim = plt.gca().get_ylim() 
  sb = draw_a_speech_bubble(text=text, x=x*(xlim[1]-xlim[0]), y=y*(ylim[1]-ylim[0]), **kwargs)
  return sb

##########################################################################################
def place_axes(axes_bbox, canvas_width, canvas_height, gap_x, gap_y):

  _ax = _find_scale_place_axes(
    max_width=axes_bbox[1][0] - axes_bbox[0][0] - 2 * gap_x,
    max_height=axes_bbox[1][1] - axes_bbox[0][1] - 2 * gap_y,
    canvas_width=canvas_width,
    canvas_height=canvas_height,
    min_margin=0,
    font_size={},
    title_pad=0,
    xlabel="",
    ylabel="",
    tick_step_x=None, tick_step_y=None,
    xy=(axes_bbox[0][0]+gap_x, axes_bbox[0][1]+gap_y))

  canvas_parameters = {
    'canvas_width': canvas_width,
    'canvas_height': canvas_height,
    'tick_step_x': None,
    'tick_step_y': None,
    'add_border': False
  }
  prepare_axes(ax=_ax, **canvas_parameters)
  return _ax

##########################################################################################
def place_watermarks(generator, max_per_line=20, fontsize=8, layer_nb=-5, line_gap=1., color='lightgrey'):  

  t = plt.gca().get_ylim()[1]
  while t > 0:
    wm_array = [generator() for _ in range(max_per_line)]
    wm_array[0] = wm_array[0][random_integer_number(1, len(wm_array[0])//2):].strip()
    new_wm = ' '.join(wm_array)
    wm_text = draw_a_speech_bubble(text=new_wm, x=0, y=t, fontsize=fontsize, position='lt', color=color, layer_nb=layer_nb, wrap=False)
    t = wm_text.bottom * (1 + line_gap) - line_gap * wm_text.top

##########################################################################################
def create_a_page(page_size, dpi, wm_generator=None, header=None, header_fontsize=20, margin=.05, header_top_margin=.02, **wm_kwargs):

  plt.figure(figsize=page_size, dpi=dpi)
  place_axes(axes_bbox=[[margin, margin], [1-margin, 1-margin]], canvas_width=(1-2*margin)*page_size[0], canvas_height=(1-2*margin)*page_size[1], gap_x=0, gap_y=0)

  if wm_generator:
    _wm_kwargs = {key[3:]:value for key, value in wm_kwargs.items()}
    place_watermarks(generator=wm_generator, **_wm_kwargs)

  if header:
    title = place_text(text=header, x=.5, y=1-header_top_margin, position='ct', fontsize=header_fontsize)
  else:
    title = None
    
  return title
  
##########################################################################################
_infodoc_keys = ['Title', 'Author', 'Subject', 'Keywords', 'CreationDate', 'ModDate', 'Producer']

def _singleton_fig_yielder():
  yield plt.gcf()
  
def create_a_pdf(filename, page_yielder=_singleton_fig_yielder, show=False, pdf_info={}):
  assert not {k for k in pdf_info if k not in _infodoc_keys}
  
  with PdfPages(filename if filename.endswith('.pdf') else (filename+'.pdf')) as pdf:
    for page in page_yielder():
      if show:
        plt.show(block=False)
        input('Press Enter to continue...')
      pdf.savefig(page)

    infodict_ref = pdf.infodict()
    infodict_ref = {**infodict_ref, 'Author' : "", 'Producer' : "", 'ModDate' : datetime.datetime.today(), 
                                      'CreationDate' : datetime.datetime.today(), **pdf_info}
    return pdf
  