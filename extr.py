import matplotlib.pyplot as plt
import numpy as np
import queue as Q
import math as m
import sys
import re


def Richardson_extrapolation_3_order( x,h_min ,h_degree):
    current_h=h_min/2
    arr=[]
    for i in range(0, int(h_degree/2)):
            current_h = round((2)*current_h, 4)
            f_x_m_2 = (x-(current_h*2))*m.exp((x-(current_h*2)))
            f_x_m_1 = (x-(current_h*1))*m.exp((x-(current_h*1)))
            f_x_p_1 = (x+(current_h*1))*m.exp((x+(current_h*1)))
            f_x_p_2 = (x+(current_h*2))*m.exp((x+(current_h*2)))
            val = ((-0.5*f_x_m_2)+(f_x_m_1)-(f_x_p_1) +(0.5*f_x_p_2))/(current_h**3)
            arr.append(val)

            print("val at h  =  " + str(current_h)+" =  "+str(val))

    for i in range(0,int(h_degree/2)-1):
        extrapolation_degree = i+1
        ex_deg=extrapolation_degree
        new_arr = []
        print("\n"+str(extrapolation_degree)+ "  extrapolation " )
        for j in range (0, len (arr)-1):
            val = (((4**ex_deg)*arr[j])-(arr[j+1]))/((4**ex_deg)-1)
            print(str(j)+ " "+ str(val))
            new_arr.append(val)
        

        arr=new_arr

    true_val = x*m.exp(x)+3*m.exp(x)
    print (" Output is "+ str(arr[0]))
    print(" ture value  is " + str(true_val))
    print (" true error  is "+str((m.fabs(true_val-arr[0])/(true_val))*100))



Richardson_extrapolation_3_order(2, 0.1, 6)




        

