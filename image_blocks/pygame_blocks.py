# file         : pygame_blocks.py
# Description  : Some code to dynamicaly play with image blocks               
# Date         : 05/01/2020
# Author       : mcalyer
# Works with   : python 3.7 , PIL 7.1.1 , pygame 1.9.6
# Release      : first : 05/01/2020
# 
# Notes:       :                    


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys, pygame , time
from image_blocks import *

def center(image_table):
    # Center image offset    
    N         = image_table['size']
    im_w,im_h = image_table['img_size'] 
    off_x     = (w - im_w)//2
    off_y     = (h - im_h)//2
    for i in range(N):
        imx,L,T = image_table[i]    
        image_table[i] = (imx,L+off_x,T+off_y)  
    return image_table 
 
def pyg_display(image_table):   
    N = image_table['size']   
    for i in range(N):    
        pyi,L,T = image_table[i]             
        screen.blit(pyi,(L,T)) 

# Must do this 
pygame.init()

# Get Modes
mode = w,h = (1280,960)
modes = pygame.display.list_modes()

# Set Mode
if mode in modes:
    screen = pygame.display.set_mode(mode)
 
# Caption 
pygame.display.set_caption('Image Blocks')

# Create image blocks 
file = 'yb.jpg'   
image_table , message = blocks(file,40,32)
if image_table is None : print(message) ; exit(0)
user_image_table = image_table.copy()

# Center image
user_image_table   = center(user_image_table)
# Convert image table to pygame surfaces
pyg_image_table    = pyg_surface_table(user_image_table)
# Scramble image
pyg_scramble_table = scramble(pyg_image_table)
# Display
pyg_display(pyg_scramble_table)
pygame.display.update()

time.sleep(1)

# Create clock , track time  
clock = pygame.time.Clock()

######################################### Display Loop ####################################################
i = 0
unscramble_flag = True
while 1:    
    for event in pygame.event.get():
       if event.type == pygame.QUIT: sys.exit()
  
    if unscramble_flag:    
        done,pyg_scramble_table = unscramble_random(pyg_image_table,pyg_scramble_table) 
        if(done) : 
           unscramble_flag = False          
           i = 0
           time.sleep(5)
           
    if False == unscramble_flag:
          done,pyg_scramble_table = scramble_one(pyg_image_table,pyg_scramble_table)
          if(done) :           
            i = 0
            unscramble_flag = True
            time.sleep(5)
    pyg_display(pyg_scramble_table)
    i = i + 1
    
        
    pygame.display.update()
    # Frame rate
    clock.tick(60)
   
