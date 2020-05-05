# file         : image_blocks.py
# Description  : Code to slice up image into blocks , which can be reassembled , 
#                scrambled , used to make mosaic , .. etc 
# Date         : 05/01/2020
# Author       : mcalyer
# Works with   : python 3.7 , PIL 7.1.1 , pygame 1.9.6
# Release      : first : 05/01/2020
# 
# Notes:       : How image gets sliced into blocks depended on user ,
#                image size, number of width blocks , number of height blocks                

from PIL import Image 
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

  
def blocks(image_file,wn,hn):
    # Description : Slice image file into blocks 
    # Input       : image file name , width, height number of blocks
    # Output      : table (dict) of PIL images with meta data
    try:
        im = Image.open(image_file) 
    except:
        return None , 'Can not open image file : ' +  image_file     
    image_table = {}  
    im_w, im_h = im.size   
    w      = im_w//wn   
    h      = im_h//hn        
    left   = 0
    top    = 0
    right  = w
    bottom = h      
    i = 0
    ipd = {}
    for _ in range(0,im_h,h): 
        left  = 0 
        right = w
        for _ in range(0,im_w,w):
            imx = im.crop((left, top, right, bottom))                        
            image_table[i]  = [imx,left,top] 
            ipd[(left,top)] = imx            
            left  = left  + w           
            right = right + w
            i = i + 1
        top = top + h
        bottom =  bottom + h  
    image_table['name']        = image_file
    image_table['img_size']    = (im_w,im_h)
    image_table['blocks']      = (wn,hn)
    image_table['block_sizes'] = (w,h)
    image_table['size']        = i   
    image_table['mode']        = im.mode
    image_table['mosaic']      = (0,0)
    image_table['ipd']         = ipd
    im.close() 
    return image_table , None         
       
def reconstruct(image_table,file_name):  
    # Description : Puts sliced image back together , creates image file 
    # Input       : image table , image file name
    # Output      : image file     
    im_w,im_h = image_table['img_size'] 
    N = image_table['size']     
    imc = Image.new('RGB',(im_w, im_h))        
    for i in range(N):      
        imx,left,top = image_table[i]        
        imc.paste(imx,(left, top)) 
    if file_name is not None:
        try:
            imc.save(file_name) 
            return True , None
        except:
            return False , 'Can not save image file : ' + file_name  
    imc.show()
    return True , None 


def scramble(image_table):  
    rimage_table = image_table.copy()
    N = image_table['size']  
    im_r = random.sample(range(N),N)   
    for i in range(N):
        imgx = image_table[i][0]         
        _,left,top = image_table[im_r[i]]          
        rimage_table[i] = (imgx,left,top)     
    return rimage_table   

    
def scramble_one(image_table,rimage_table):  
    # Description : Scrambles image table , 2 elements at a time  
    # Input       : image table , scramble table
    # Output      : Done = False/True , scrambled table     
    N = image_table['size']  
    same_list = [i for i in range(N) if rimage_table[i] == image_table[i]]
    if len(same_list) == 0:
        return True , rimage_table
    random.shuffle(same_list)    
    i = same_list[0]  
    j = same_list[1]  
    q,l,t = image_table[i]       
    I,L,T = rimage_table[j]          
    rimage_table[i] = [q,L,T] 
    rimage_table[j] = [I,l,t]   
    return False, rimage_table       
       
def unscramble_random(image_table, rimage_table): 
    # Description : Unscrambles image table , ramdomized   
    # Input       : scrambled image table, unscramled image table  
    # Output      : less scrambled image table        
    i_list = []
    N = image_table['size']  
    _i_list = [i for i in range(N) if rimage_table[i] != image_table[i]] 
    if len(_i_list) == 0:
        return True, rimage_table
    im_r = _i_list.copy()    
    random.shuffle(im_r)     
    for i,q in enumerate(_i_list):      
        image_good = False        
        imgx = image_table[q][0]         
        _,left,top = image_table[im_r[i]]          
        rimage_table[q] = [imgx,left,top]     
    return False , rimage_table      

def unscramble(image_table,rimage_table):
    # Description : Unscrambles image table , element at a time 
    #               Swaps elements    
    # Input       : unscramled image table , scrambled image table
    # Output      : image file      
    unscramble_table = rimage_table.copy()
    rimg_table = rimage_table.copy()
    ipd_table  = image_table['ipd']    
    N = image_table['size'] 
    not_list = [i for i in range(N) if rimage_table[i] != image_table[i]]            
    for i in not_list:
        I0,L0,T0        = image_table[i]
        I1,L1,T1        = rimg_table[i]       
        I3              = ipd_table[(L0,T0)]
        list_k          = list(ipd_table) 
        k               = list_k.index((L0,T0))             
        unscramble_table[i] = [I0,L0,T0] 
        rimg_table[i]       = [I0,L0,T0] 
        rimg_table[k]       = [I3,L1,T1]         
    return unscramble_table  
    
def gen_unscramble(image_table,rimage_table):
    # Description : Generator for unscramble 
    unscramble_table = rimage_table.copy()
    rimg_table = rimage_table.copy()
    ipd_table  = image_table['ipd']   
    N = image_table['size']      
    for i in range(N):        
        I0,L0,T0  = image_table[i]
        I1,L1,T1  = rimg_table[i]       
        I3              = ipd_table[(L0,T0)]
        list_k          = list(ipd_table) 
        k               = list_k.index((L0,T0))             
        unscramble_table[i] = (I0,L0,T0) 
        rimg_table[i] = [I0,L0,T0] 
        rimg_table[k] = [I3,L1,T1] 
        flag = True if (i == 63) else False 
        yield (flag,unscramble_table)      
           
def mosaic(image_table,delta_x,delta_y):
    # Description : Change image block position to create spacing between image blocks
    #               Spacing is delta x , delta y    
    # Input       : image table  
    # Output      : image table with changed left,top        
    mosaic_image_table = image_table.copy() 
    mosaic_image_table['mosaic'] = (delta_x,delta_y)    
    N          = image_table['size']   
    wn, hn     = image_table['blocks']   
    w, h       = image_table['block_sizes'] 
    i = 0  
    T_off = 0
    for _ in range(hn):
        L_off = 0
        for _ in range(0,wn):
            imx,left,top = image_table[i]            
            L,T = L_off,T_off           
            mosaic_image_table[i] = [imx,L,T]           
            i = i + 1
            L_off = L_off + delta_x + w
        T_off = T_off + delta_y + h      
    return mosaic_image_table  
    
def mosaic_save(image_table,file_name):
    # Description : Saves mosaic image table as file                  
    # Input       : image table  
    # Output      : image file    
    N = image_table['size']  
    dx,dy      = image_table['mosaic']        
    im_w, im_h = image_table['img_size'] 
    wn, hn     = image_table['blocks']   
    w, h       = image_table['block_sizes']      
    im_w = im_w + ((wn - 1) * dx)    
    im_h = im_h + ((hn - 1) * dy)    
    imc = Image.new('RGB',(im_w, im_h)) 
    for i in range(N):
        imx,L,T = image_table[i]
        imc.paste(imx,(L,T))
    try:
        imc.save(file_name) 
        return True , None
    except:
         return False , 'Can not save image file : ' + file_name 
            
def pyg_surface_table(image_table):  
    # Description : Convert PIL image to pygame surfaces
    # Input       : image table
    # Output      : pygame surface table   
    pyg_table = image_table.copy()
    N   = image_table['size'] 
    w,h = image_table['block_sizes'] 
    m   = image_table['mode']    
    for i in range(N):
        imx,L,T = image_table[i]
        img = pygame.image.fromstring(imx.tobytes(), (w,h), m)              
        pyg_table[i] = [img,L,T]   
    return pyg_table
 
def main():
    file = 'yb.jpg'   
    # for yb.jpg , size 1200x896 , mode RGB 
    # Blocks that work : 2x2,4x4,8x8,16x16,40x32,60x64,120x128,1200x64
    image_table , message = blocks(file,8,8)
    if image_table is None : print(message) ; exit(0)
    reconstruct(image_table,'re_' + file)  
    
   
    ra_image_table = scramble(image_table)
    reconstruct(ra_image_table,'ra_' + file)     
   
    mosaic_image_table = mosaic(image_table,2,2)
    mosaic_save(mosaic_image_table,'mosaic_bear.jpg')
    
    unscramble_table = unscramble(image_table,ra_image_table)
    reconstruct(unscramble_table,'un_' + file) 

    pyg_table =  pyg_surface_table(image_table) 

    done, scramble_table = scramble_one(image_table,image_table)
    done, scramble_table = scramble_one(image_table,image_table)  
    done, scramble_table = scramble_one(image_table,image_table)   
    reconstruct(scramble_table,'scr_one.jpg')    
    
    
    exit(0)
    



if __name__ == "__main__":    
    main()
            
       
       
       
       
       
       
                 