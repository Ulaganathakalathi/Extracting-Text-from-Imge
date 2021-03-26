# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:03:23 2020

@author: us51114
crop the image
"""
import numpy as np
import cv2
import sys
from PIL import Image

def find_the_diff_corner(img,x_dim,y_dim,str_inp):
    if str_inp=='top':
        start_i=0;stop_i=x_dim;step_i=1
        start_j=0;stop_j=y_dim;step_j=1
        addin=-1
        x_var='i';y_var='j'
    elif str_inp=='bottom':
        start_i=x_dim-1;stop_i=-1;step_i=-1
        start_j=0;stop_j=y_dim-1;step_j=1
        addin=1
        x_var='i';y_var='j'
    elif str_inp=='left':
        start_i=0;stop_i=y_dim-1;step_i=1
        start_j=0;stop_j=x_dim-1;step_j=1
        addin=1
        x_var='j';y_var='i'
    elif str_inp=='right':
        start_i=y_dim-1;stop_i=-1;step_i=-1
        start_j=0;stop_j=x_dim-1;step_j=1
        addin=-1
        x_var='j';y_var='i'
    # print(start_i,":",stop_i,":",step_i)
    # print(start_j,":",stop_j,":",step_j)
    find_val=img[0,0]
    # print("find_val=",type(find_val))
    for i in range(start_i,stop_i,step_i):
        # for j in range(start_j,stop_j,step_j):
            # print(type(img[eval(x_var),eval(y_var)]))
        if x_var=='i':
            cur_val=img[eval(x_var),:]
        else:
            cur_val=img[:,eval(y_var)]
        # cur_val=img[eval(x_var),eval(y_var)]
        comparison = find_val == cur_val 
        equal_arrays = comparison.all() 
        if ~equal_arrays:
            # print('find_val:',find_val,',cur_val:',cur_val)
            index_found=i #+addin
            # print('index_found:',index_found,'i:',i)
            return index_found
            
def add_border(img,start_i,stop_i,cont_j,var_axis):
    if var_axis=='x':
        x_var='i';y_var='j'
    else:
        x_var='j';y_var='i'
    set_color=np.array([0,0,255]) #red [blue,green,red]
    for i in range(start_i,stop_i+1,1):
    # for j in range(start_j,stop_j,step_j):
        j=cont_j
        img[eval(x_var),eval(y_var)]=set_color
        # print(type(img[eval(x_var),eval(y_var)]))
        # cur_val=img[eval(x_var),eval(y_var)]
        # comparison = find_val == cur_val 
        # equal_arrays = comparison.all() 
        # if ~equal_arrays:
        #     index_found=i+addin
        #     return index_found

def give_the_index_val(inp_img):
    x=inp_img.shape[0]
    y=inp_img.shape[1]
    req_val=0
    find_val=[255,255,255]
    find_sum=np.sum(find_val)
    for i in range(x):
        for j in range(y):
            check_val=inp_img[i,j]
            comparison = find_val == check_val 
            equal_arrays = comparison.all() 
            if ~equal_arrays: #for not white
                 ch_sum=np.sum(check_val)
                 if ch_sum<0.9*find_sum:
                     inp_img[i,j]=[0,0,0] #black
                     req_val=req_val+(i+1)/x+(j+1)/y
                 else:
                     inp_img[i,j]=[255,255,255] #black
    return req_val,inp_img

def Auto_Crop_img(inp_img):
    x=inp_img.shape[0]
    y=inp_img.shape[1]
    top_loc=find_the_diff_corner(inp_img,x,y,'top')
    print('top_loc=',top_loc)
    bot_loc=find_the_diff_corner(inp_img,x,y,'bottom')
    left_loc=find_the_diff_corner(inp_img,x,y,'left')
    right_loc=find_the_diff_corner(inp_img,x,y,'right')
    crop_img=inp_img[top_loc:bot_loc+1,left_loc:right_loc+1]
    return crop_img

def adj_img_to_size(img,axis,req_size):
    #axis=0 (x-axis) or 1 (y-axis)
    colr=[255,255,255]
    x=img.shape[0]
    y=img.shape[1]
    act_size=img.shape[axis]
    # if act_size>=req_size:
    #     print('already at required size')
    #     return img
    if axis==0: #height
        # apd_img=img[0,:]
        apd_img=np.zeros([1,y,3])
    else: #width
        # apd_img=img[:,0]
        apd_img=np.zeros([x,1,3])
    apd_img[:]=colr
    # image_f[:]=image[0,0]
    print('shape1=',img.shape,apd_img.shape,axis)
    for i in range(act_size,req_size):
        img=np.concatenate((img,apd_img),axis)
    return img
        
def concate_img(img1,img2,axis):
    #axis=0:in x-axis,=1:in y-axis'
    # colr=[255,255,255]
    x1=img1.shape[0]
    y1=img1.shape[1]
    x2=img2.shape[0]
    y2=img2.shape[1]
    print('x1=',x1,y1,x2,y2,axis)
    if axis==0: #X-axis
        if y1!=y2:
            req_y=max(y1,y2)
            if req_y==y1: #img1
                img2=adj_img_to_size(img2,1,req_y)
            else: #img2
                img1=adj_img_to_size(img1,1,req_y)
    else:
        if x1!=x2:
            req_x=max(x1,x2)
            if req_x==x1: #img1
                img2=adj_img_to_size(img2,0,req_x)
            else: #img2
                img1=adj_img_to_size(img1,0,req_x)

            
            # new_img1=np.concatenate((img1,img2),0)
    print('shape=',img1.shape,img2.shape,axis)
    new_img1=np.concatenate((img1,img2),axis)
    return new_img1
    
# global junction_point,end_point
# junction_point=[];end_point=[]

def find_until_color_match_or_not(inp_img,start_x,start_y,find_color,right_or_left,match,end_y=-1):
    #right_or_left: 1-move right, 2-move left
    #match: 1-until match, 0-until not match
    y=inp_img.shape[1]
    if right_or_left=='right':
        incrm=1
        if end_y==-1:
            i_end_y=y
        else:
            i_end_y=end_y+incrm
        # i_start=start_y;i_end=i_end_y
    else:
        incrm=-1
        if end_y==-1:
            i_end_y=0
        else:
            i_end_y=end_y+incrm
    i_start=start_y;i_end=i_end_y
    
    #print('y=',y)
    # if end_y==-1:
    #     if right_or_left=='right':
    #         i_end_y=y
    #     else:
    #         i_end_y=0
    # else:
    #     i_end_y=end_y
    # # find_val=[0,0,0] #black
    # if right_or_left=='right': #fwd
    #     incrm=1;i_start=start_y;i_end=i_end_y
    # else:
    #     incrm=-1;i_start=i_end_y;i_end=start_y
    # if end_y!=-1:
    #     i_end=i_end+incrm
    #print("for loop:",i_start,i_end,incrm,'match',match)
    if match==1: #until match
        for i in range(i_start,i_end,incrm):
            check_val=inp_img[start_x,i]
            comparison1 = find_color == check_val
            if comparison1.all(): #not required color
                #print("return i=",i)
                return i
    else: #until not match
        for i in range(i_start,i_end,incrm):
            check_val=inp_img[start_x,i]
            comparison1 = find_color == check_val
            if not comparison1.all(): #not required color
                #print("return i=",i)
                return i-incrm
    #print("return i=",-1)
    return -1



def find_the_connection_down(inp_img,find_color,cont_fig,start_i,prev_left=0,prev_right=0): #considering only white & black
    global junction_point,min_x,min_y,max_x,max_y,end_point    
    out_img=inp_img[:]
    x=inp_img.shape[0]
    y=inp_img.shape[1]
    req_val=0
    #cont_fig=0
    # prev_left=0;prev_right=0
    # find_color=[0,0,0] #black
    find_sum=np.sum(find_color)
    right_y1=0
    for i in range(start_i,x):
        # for j in range(y):
            if cont_fig: #find connection for the identified black
                print('config: 1,i',i)
                check_val=inp_img[i,prev_left-1]
                comparison = find_color == check_val 
                if comparison.all(): # finding out left end of black
                    #find left end of black by move left
                    print('move end of black left prev_left',prev_left-1)
                    cur_left_y=find_until_color_match_or_not(inp_img,i,prev_left-1,find_color,'left',0,-1)
                    if cur_left_y==-1:
                        cur_left_y=prev_left-1
                else: #finding out right start of black
                    #find left end of black by move right
                    print('move end of black right prev_left-1',prev_left-1,'prev_right+1',prev_right+1)
                    cur_left_y=find_until_color_match_or_not(inp_img,i,prev_left-1,find_color,'right',1,prev_right+1)
                
                if cur_left_y!=-1: #incase of continuous identified
                    if cur_left_y<min_y:
                        min_y=cur_left_y
                    prev_left=cur_left_y
                    #find the end of cont black right
                    print('find the end of cont black right cur_left_y',cur_left_y,'prev_right+1',prev_right+1)
                    # if cur_left_y==prev_right+1:
                    #     cur_right_y=cur_left_y
                    # else:
                    cur_right_y=find_until_color_match_or_not(inp_img,i,cur_left_y,find_color,'right',0,-1) #prev_right+1)
                    right_y1=cur_right_y
                    #print('right_y1',right_y1,'prev_right',prev_right,'cur_right_y',cur_right_y)
                    if cur_right_y>max_y:
                        max_y=cur_right_y
                    while right_y1<prev_right and right_y1!=-1: #this is to find all the junctions, incase of current right is less that previous line right
                        #print('while righty:',right_y1,'prev_right',prev_right,'cur_right_y',cur_right_y)
                        #sys.exit()
                        #start of next black right
                        print('i=',i,'right_y1=',right_y1,'end_right=',prev_right+1)
                        right_y1_loc=right_y1
                        right_y1=find_until_color_match_or_not(inp_img,i,right_y1+1,find_color,'right',1,prev_right+1) #find next black
                        print('output=',right_y1)
                        if right_y1==-1:
                            break
                        if right_y1<=prev_right+1:
                            end_point.append([i,right_y1_loc])
                            junction_point.append([i,right_y1,'down',0])
                            #find the end of cont black right
                            right_y1=find_until_color_match_or_not(inp_img,i,right_y1,find_color,'right',0,prev_right+1) #find end of black
                            if right_y1>max_y:
                                max_y=right_y1
                            if right_y1>=prev_right:
                                break
                    loc_prev_right=prev_right
                    if cur_right_y>prev_right:
                        while cur_right_y>loc_prev_right and loc_prev_right!=-1:#need to check any connectivity in the top
                            #print('while righty:',right_y1,'loc_prev_right',loc_prev_right,'cur_right_y',cur_right_y)
                            #next start of black
                            loc_prev_right_temp=loc_prev_right
                            loc_prev_right=find_until_color_match_or_not(inp_img,i-1,loc_prev_right+1,find_color,'right',1,cur_right_y+1)
                            if loc_prev_right==-1:
                                break
                            if loc_prev_right<=cur_right_y+1:
                                end_point.append([i,loc_prev_right_temp])
                                junction_point.append([i-1,loc_prev_right,'up',0])
                                #find the end of cont black right
                                loc_prev_right=find_until_color_match_or_not(inp_img,i-1,loc_prev_right,find_color,'right',0,cur_right_y+1)
                                if loc_prev_right>max_y:
                                    max_y=loc_prev_right
                                if loc_prev_right>=cur_right_y:
                                    break
                    prev_right=cur_right_y
                    if cur_right_y>max_y:
                        max_y=cur_right_y
                    if max_x<i:
                        max_x=i
                else:
                    if max_x>min_x and 0:
                        #print('break here max_x, min_x',max_x,min_x)
                        ka=add_border(out_img,min_x-1,max_x+1,min_y-1,'x') #left border
                        ka=add_border(out_img,min_x-1,max_x+1,max_y+1,'x') #right border
                        ka=add_border(out_img,min_y-1,max_y+1,min_x-1,'y') #top border
                        ka=add_border(out_img,min_y-1,max_y+1,max_x+1,'y') #botom border
                        # for k in range(min_x,max_x+1):
                        #     for m in range(min_y,max_y+1):
                        #         out_img[k,m]=[255,0,0]
                        # cv2.imshow('image',out_img)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()
                    #below to provide the juction point color
                    # for each_j in junction_point:
                    #     if each_j[2]=="up":
                    #         out_img[each_j[0],each_j[1]]=[0,0,255] #Red'
                    #     else:
                    #         out_img[each_j[0],each_j[1]]=[0,255,0] #green
                    # for each_j in end_point:
                    #     out_img[each_j[0],each_j[1]]=[255,0,0] #blue'
                    return out_img
                    cont_fig=0
            else: #check the first black
                if len(junction_point)>0:
                    print(junction_point)
                junction_point.clear()
                end_point.clear()
                min_x=i;max_x=i
                #find the next black
                left_y=find_until_color_match_or_not(inp_img,i,prev_left,find_color,'right',1,-1)
                #print('newline',i,left_y)
                if left_y!=-1:
                    min_y=left_y
                    #find not equal to black
                    right_y=find_until_color_match_or_not(inp_img,i,left_y,find_color,'right',0,-1)
                    max_y=right_y
                    prev_left=left_y
                    prev_right=right_y
                    cont_fig=1
    return out_img

                
#import image
# img=cv2.imread('D:\\kalathi\\My_collection\\Python\\Auto_Crop_image\\Picture.jpg')

def bgr_2_rbg(inp_img):
    x=inp_img.shape[0]
    y=inp_img.shape[1]
    print('inp_img shape',img.shape)
    for i in range(x):
        for j in range(y):
            act_clr=inp_img[i,j]
            inp_img[i,j]=[act_clr[2],act_clr[1],act_clr[0]]
    return inp_img

if __name__ == "__main__":
    global junction_point,min_x,min_y,max_x,max_y,end_point
    min_x=0;min_y=0;max_x=0;max_y=0
    junction_point=[];end_point=[]
    comb_img=[];pre_img=[];pre_img_inp=[];comb_img_inp=[];crop_inp=[]
    no_of_let_in_r=0
    # for let_i in range(ord('a'), ord('z')+1):
    img=cv2.imread('Input.png') #Multiple_letter.png') Any_letter1.png
    # img=cv2.imread('letter_' + chr(let_i) + '.png')
    print(img.shape)
    print(img[0,0])
    x=img.shape[0]
    # print(x)
    y=img.shape[1]
    # top_loc=find_the_diff_corner(img,x,y,'top')
    # print('top_loc=',top_loc)
    # bot_loc=find_the_diff_corner(img,x,y,'bottom')
    # left_loc=find_the_diff_corner(img,x,y,'left')
    # right_loc=find_the_diff_corner(img,x,y,'right')
    # print('top_loc=',top_loc,'bot_loc=',bot_loc,'left_loc=',left_loc,'right_loc=',right_loc)
    
    req_val,black_wite=give_the_index_val(img)
    # ka=cv2.imwrite('output2.jpg',black_wite)
    # cv2.imshow('image',black_wite)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    crop_inp=np.empty_like(black_wite)
    crop_inp[:]=black_wite #cv2.imread('output2.jpg') #black_wite[:]
    crop_inp=Auto_Crop_img(crop_inp)
    # cv2.imshow('image',crop_inp)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    outimg=np.empty_like(black_wite)
    outimg[:]=black_wite
    
    # outimg=black_wite
    begin_i=0
    while 1: #to get first letter in all the row
        
        min_x=-1;min_y=-1;max_x=-1;max_y=-1
        print('begin i',begin_i)
        outimg=find_the_connection_down(black_wite,[0,0,0],0,begin_i)
        print('min_y:',min_y)
        if min_y==-1:
            break
        #below to check the all junctions
        # while 1: 
        for each_j in junction_point:
            if each_j[2]=="down" and each_j[3]==0:
                start_i=each_j[0]
                prev_left=each_j[1]
                prev_right=find_until_color_match_or_not(black_wite,start_i,prev_left,[0,0,0],'right',0,-1)
                if prev_left<min_y:
                    min_y=prev_left
                if prev_right>max_y:
                    max_y=prev_right
                # cv2.imshow('image',black_wite)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                outimg=find_the_connection_down(black_wite,[0,0,0],1,start_i+1,prev_left,prev_right)
                each_j[3]=1
        print('junction_point',junction_point)
        #below to color the junction
        # for each_j in junction_point:
        #     if each_j[2]=="up":
        #         outimg[each_j[0],each_j[1]]=[0,0,255] #Red'
        #     else:
        #         outimg[each_j[0],each_j[1]]=[0,255,0] #green
        # for each_j in end_point:
        #     outimg[each_j[0],each_j[1]]=[255,0,0] #blue'
            
        # #below to color the margins
        # outimg[min_x,min_y]=[255,255,0]
        # outimg[max_x,max_y]=[0,255,255]
        
        ka=add_border(outimg,min_x-1,max_x+1,min_y-1,'x') #left border
        ka=add_border(outimg,min_x-1,max_x+1,max_y+1,'x') #right border
        ka=add_border(outimg,min_y-1,max_y+1,min_x-1,'y') #top border
        ka=add_border(outimg,min_y-1,max_y+1,max_x+1,'y') #botom border
        begin_i=max_x+1
        
    # ka=cv2.imwrite('output_' + chr(let_i) + '.png',outimg)
    ka=cv2.imwrite('output.png',outimg)
    crop_out=Auto_Crop_img(outimg)

    
    cv2.imshow('image',outimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 

