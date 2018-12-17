import matplotlib.pyplot as plt
import numpy as np
import queue as Q
import sys
import re


def get_bin(x, n):
    bit_string_list = list(format(abs(x), 'b').zfill(n))
    if(x < 0):
        for i in range(len(bit_string_list)):
            bit_string_list[i] = '0' if bit_string_list[i] == '1' else '1'
        bit_string = ''.join(bit_string_list)
        x = int(bit_string, 2)+1
        bit_string = format(abs(x), 'b')
    else:
        bit_string = ''.join(bit_string_list)
    return bit_string

def get_tables():
    f = open("./micro_codes_f0.txt", 'r')
    lines = f.readlines()
    f0 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line =line.lower()
        value, space, key = line.partition(' ')
        f0[key] = value
        print ("--key ="+key+"--value ="+value+"--"  )
    
    f.close()

    f = open("./micro_codes_f1.txt", 'r')
    lines = f.readlines()
    f1 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f1[key] = value
        print("--key ="+key+"--value ="+value+"--")

    f.close()


    f = open("./micro_codes_f2.txt", 'r')
    lines = f.readlines()
    f2 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f2[key] = value
        print("--key ="+key+"--value ="+value+"--")
    f.close()

    f = open("./micro_codes_f3.txt", 'r')
    lines = f.readlines()
    f3 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f3[key] = value
        print("--key ="+key+"--value ="+value+"--")
    f.close()

    f = open("./micro_codes_f4.txt", 'r')
    lines = f.readlines()
    f4 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f4[key] = value
        print("--key ="+key+"--value ="+value+"--")
    f.close()

    f = open("./micro_codes_f5.txt", 'r')
    lines = f.readlines()
    f5 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f5[key] = value
        print("--key ="+key+"--value ="+value+"--")
    f.close()

    f = open("./micro_codes_f6.txt", 'r')
    lines = f.readlines()
    f6 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f6[key] = value
        print("--key ="+key+"--value ="+value+"--")
    f.close()

    f = open("./micro_codes_f7.txt", 'r')
    lines = f.readlines()
    f7 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f7[key] = value
        print("--key ="+key+"--value ="+value+"--")
    f.close()

    f = open("./micro_codes_f8.txt", 'r')
    lines = f.readlines()
    f8 = {}
    for i in range(0, len(lines)):
        line = lines[i]
        line = ' '.join(line.split())
        line = line.replace("\n", '')
        line = line.lower()
        value, space, key = line.partition(' ')
        f8[key] = value
        print("--key ="+key+"--value ="+value+"--")
    f.close()

    
    return [f0, f1, f2, f3,f4,f5,f6,f7,f8]


def micro_assembler (lines,debug,out):

    flist= get_tables()
    print(" start assembling ")
    for i in range (0,len(lines)):
        #print ("i-----------------> "+lines[i])
        output=['' for i in range(0,len(flist))]
        line = ''.join(lines[i].split())
        signals = line.split(',')
        for j in range(0,len(signals)-1):
            #print("j------->"+signals[j])
            signal = signals[j].lower()
            for k in range (0,len(flist)):
                if signal in flist[k]:
                    if (output[k] != '')  : 
                        print (" error in mutual exlusive") 
                        exit(0)
                    else :
                        output[k]=flist[k][signal]  ## first time to set the part
                        #print (" output ["+str(k)+"] ="+output[k])
        
        signal =signals[len(signals)-1]
        next_address=get_bin(int(signal),6)


        
        header=''
        debug_line =''
        code_line=''

        if output[0] == '':                      ###### assume oalways f0 is alu operation
            output[0] = flist[0]["f=aandb"]
        debug_line = debug_line + "\t\t" + output[0]
        code_line=code_line+output[0]
        header=header+"\t\t"+"F"+str(0)
        
        for j in range (1,len(flist)):
            if output[j] == '':
                #print("inside")
                #print(j)
                output[j] = flist[j]["nooperation"]
                #print (j)
            debug_line = debug_line + "\t\t" + output[j]
            header = header+"\t\t"+"F"+str(j)
            code_line=code_line+output[j]

        debug_line = debug_line + "\t\t" + next_address
        code_line = code_line+next_address
        header = header+"\t\t"+" next address"
        
        header = header.split()    # Splits on whitespace
        header = '{0[0]:<10}{0[1]:<10}{0[2]:<10}{0[3]:<10}{0[4]:>10}{0[5]:>10}{0[6]:>10}{0[7]:>10}{0[8]:>10}{0[9]:>10}'.format(
            header)

        debug_line = debug_line.split()    # Splits on whitespace
        debug_line = '{0[0]:<10}{0[1]:<10}{0[2]:<10}{0[3]:<10}{0[4]:>10}{0[5]:>10}{0[6]:>10}{0[7]:>10}{0[8]:>10}{0[9]:>10}'.format(
            debug_line)
        debug.writelines([lines[i],'\n'])
        debug.writelines(header+'\n')
        debug.writelines(debug_line+'\n\n')
        out.writelines(code_line+'\n')



            


def main():
    #input_fil_name = input("input filename:")
    #output_fil_name = input("output filename:")
    #debug_fil_name = input("debug filename:")
    if (len(sys.argv) != 4):
        print("Wrong number of parameters")
        sys.exit()
    input_fil_name = sys.argv[1]
    output_fil_name = sys.argv[2]
    debug_fil_name = sys.argv[3]
    try:

        f = open(input_fil_name, 'r')
        lines = f.readlines()
        debug = open(debug_fil_name, 'w')
        output = open(output_fil_name, "w")
        micro_assembler(lines, debug,output)

        f.close()
        output.close()
        debug.close()
    except IOError:
        print("Could not open or read one of the files:")
        sys.exit()


main()
