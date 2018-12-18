import matplotlib.pyplot as plt
import numpy as np
import queue as Q
import sys
import re

    def get_bin(x, n):
        bit_string_list = list(format(abs(x), 'b').zfill(n))
        if(x<0):
            for i in range(len(bit_string_list)):
                bit_string_list[i] = '0' if bit_string_list[i] == '1' else '1'
            bit_string = ''.join(bit_string_list)
            x = int(bit_string,2)+1
            bit_string = format(abs(x), 'b')
        else:
            bit_string = ''.join(bit_string_list)
        return bit_string


def op_decoding(op,beg,dictt,opecode_dict,operand_dict):
    operand_opcode = ''
    additional_word = ''
    match = re.match(r"([@]*)([\-]*[0-9]+)(\([Rr][0-7]\))", op, flags=0) # case of the operand @XRn


    if match:
        at,x,reg=match.groups()
        operand=at+"x"+reg.lower()
        operand_opcode=operand_dict[operand]
        additional_word = get_bin(int(value), 16)   
        #print(operand_opcode,"  ",additional_word)
        return(operand_opcode, additional_word)

    match = re.match(r"(#)([\-]*[0-9]+)", op,flags=0)  # case of the operand immediate value
    if match:
        hashh, value = match.groups()
        operand ="(r6)+"
        operand_opcode = operand_dict[operand]
        additional_word = get_bin(int(value), 16)
        return(operand_opcode, additional_word)
    
    if op in dictt:    # case of variable  
        address = dictt[op]
        operand = "x(r6)"
        operand_opcode = operand_dict[operand]
        x=address-(beg+2)
        #print(" address to jumbp to "+str(address)+" current after fecthx x "+str(beg+2)+ " offset  "+ str(x))
        additional_word = get_bin(int(x), 16)
        #print(operand_opcode, additional_word)
        return(operand_opcode, additional_word)
    
    op2=op.lower()
    if op2 in operand_dict :       # case of ordinary addressing mode (@)(-)(rn)(+)
        operand_opcode = operand_dict[op2]
        #print(" normal ", operand_opcode+ "additional"+additional_word+"f")
        return (operand_opcode,additional_word)

    raise ValueError (" no such operand ")
    



def op2_decoding(line, beg, dictt, output, debug, opcode_dict,operand_dict,is_xnor):
    new_str = line.replace(" ", "")
    opcode=''
    if is_xnor:
        opcode = new_str[0:4]
    else:
        opcode = new_str[0:3]

    opcode=opcode.lower()
    output_fisrt_word=''
    output_additional_word=''
    #print(opcode)
    if opcode in opcode_dict:
        opcode=opcode_dict[opcode]
        output_fisrt_word = output_fisrt_word+opcode
    else : 
        print("error   ",line  )
        sys.exit()

    if is_xnor:
        new_str=new_str[4:]
    else:
        new_str = new_str[3:]

    try :
        op_1, semicomma, op_2 = new_str.partition(',')
        (op_1,additional_word1)=op_decoding(op_1,beg,dictt,opcode_dict,operand_dict)
        output_fisrt_word = output_fisrt_word+op_1
        if additional_word1 != '':
            beg=beg+1
            output_additional_word = output_additional_word+'\n'+additional_word1
        (op_2, additional_word2) = op_decoding(op_2, beg, dictt, opcode_dict, operand_dict)
        output_fisrt_word=output_fisrt_word+op_2
        if additional_word2 != '':
            beg = beg+1
            output_additional_word = output_additional_word+'\n'+additional_word2
        
        debug.writelines('\n' +(output_fisrt_word+output_additional_word)+'\n')
        return ((output_fisrt_word+output_additional_word),beg)
    except ValueError as err :
        print (err ,"in line", line)
        sys.exit()


def op1_decoding(line, beg, dictt, output, debug, opcode_dict, operand_dict):
    new_str = line.replace(" ", "")
    #print(new_str)
    opcode = new_str[0:3]
    opcode = opcode.lower()
    output_fisrt_word =''
    output_additional_word =''
    #print(opcode)
    if opcode in opcode_dict:
        opcode = opcode_dict[opcode]
        #print(opcode+'f')
        output_fisrt_word = output_fisrt_word+opcode
        #print(output_fisrt_word+"f")
    else:
        print("error no such opcode  in line   ", line)
        sys.exit()
    try:
        new_str = new_str[3:]
        op_1, semicomma, op_2 = new_str.partition(',')
        (op_1, additional_word1) = op_decoding(
            op_1, beg, dictt, opcode_dict, operand_dict)
        output_fisrt_word = output_fisrt_word+op_1
        if additional_word1 != '':
            beg = beg+1
            output_additional_word = output_additional_word+'\n'+additional_word1

        debug.writelines('\n' + (output_fisrt_word+output_additional_word)+'\n')
        return ((output_fisrt_word+output_additional_word), beg)
    except ValueError as err:
        print (err,"in line ",line)
        sys.exit()

    
def branch(line,beg,dictt,opcode_dict):

    line = re.sub(' +', ' ', line)
    op, sep, label = line.partition(" ")
    op=op.lower()
    output_word=''
    if op in opcode_dict :
        output_word=output_word+opcode_dict[op]
    else :
        print(" error in opcode   ", line)
        sys.exit()

    if label in dictt:
        address=dictt[label]
        offset =address-(beg+1)
        def get_bin(x, n): return format(x, 'b').zfill(n)
        offset =list(get_bin(offset,11))
        if offset[0]=='-':
            offset[0]='1'
        offset=''.join(offset)    
        output_word = output_word+offset
        return output_word

    else:
        print(" no such label  ", label)
        sys.exit()
 

def get_tables():
    f=open("./codes.txt",'r')
    lines=f.readlines()
    operand={}
    opcode ={}
    for i in range(0,64):
        line=lines[i]
        line = re.sub(' +', ' ', line)
        line =line.replace("\n",'')
        key, space, value = line.partition(' ')
        operand[key]=value
    for i in range (64,94):
        line = lines[i]
        line = re.sub(' +', ' ', line)
        line = line.replace("\n", '')
        key, space, value = line.partition(' ')
        opcode[key] = value

    return opcode,operand

def generate_opcode(lines_with_type,dict,output,debug):
    beg=0
    opcode,operand=get_tables()
    for i in range (0,len(lines_with_type)):
        line,line_type = lines_with_type[i]
        debug.writelines(line+"  address  "+str(beg))

        if line_type == "2op" :
            (instructions_words,new_beg)=op2_decoding(line,beg,dict,output,debug,opcode,operand,False)
            beg = new_beg+1
            output.append(instructions_words+'\n')
        #elif line_type == "jsr":
        #mov label,tmp
        #mov pc,-(sp)
        #mov pc,tmp
        elif line_type=='xnor':
            (instructions_words,new_beg)=op2_decoding(line,beg,dict,output,debug,opcode,operand,True)
            beg = new_beg+1
            output.append(instructions_words+'\n')
        elif line_type == "1op":
            (instructions_words,new_beg)=op1_decoding(line,beg,dict,output,debug,opcode,operand)
            beg = new_beg+1
            output.append(instructions_words+'\n')
        elif line_type == "br":
            instructions_words = branch(line, beg, dict, opcode)
            debug.writelines("\n"+instructions_words+'\n')
            beg=beg+1
            output.append(instructions_words+'\n')

        elif line_type == "var":
            var,sep,value=line.partition(" ")
            def get_bin(x, n): return format(x, 'b').zfill(n)
            value=list(get_bin(int(value),16))
            if value[0]=='-':
                value[0]='1'
            value=''.join(value)
            debug.writelines("\n"+value+'\n')
            beg = beg+1
            output.append(value+'\n')
        elif line_type == "nop_rts_hlt_iret":
            line=line.replace(' ','')
            line=line.lower()
            if line in opcode :
               instructions_words = opcode[line]
               debug.writelines("\n"+instructions_words+'\n')
               output.append(instructions_words+'\n')
            else :
                print (" no such instruction "+line)
                sys.exit()
            beg=beg+1


    return

def get_instruction_word(input_str): # word needed for operands  input--> string of operands
                                    
    op=0
    #print(input_str)
    op_1, semicomma, op_2 = input_str.partition(',')
    #print (op_1+semicomma+op_2)
    if re.match(r"#", op_1, flags=0):
        op=op+1
    elif re.match(r"([@]*[rR][0-7]|[@]*\([Rr][0-7]\)\+|[@]*\-\([Rr][0-7]\))", op_1, flags=0):
        #print(" matched addressing modes", op_1)
        op=op
    elif re.match(r"[@]*[\-]*[0-9]+\([Rr][0-7]\)", op_1, flags=0):
        op=op+1
    else :
        op=op+1

    if (op_2==""):
        #print(" number of words needed by operands  ", op)
        return op   # if the str contain only one operand

    if re.match(r"#",op_2 , flags=0):
        op = op+1
    elif re.match(r"([@]*[rR][0-7]|[@]*\([Rr][0-7]\)\+|[@]*\-\([Rr][0-7]\))", op_2, flags=0):
        #print(" matched addressing modes", op_2)
        op=op
    elif re.match(r"[@]*[\-]*[0-9]+\([Rr][0-7]\)", op_2, flags=0):
        op=op+1
    else:
        op = op+1

    #print(" number of words needed by operands  ",op)
    return op

def count_words(input_str,beg,dict,output):
    op_2 = r"[a-zA-Z][a-zA-Z][a-zA-Z]\s+.+,.+"      # two operand instrcutions
    reg = r"[a-zA-Z][a-zA-Z][a-zA-Z]\s+.+"         # any instruction on format 3char + space + manycharacter (branch or 1operand)
    variables = r"[dD][eE][fF][iI][nN][eE]\s+.+\s+.+"
    hlt_nop_rts_iret = r"([Hh][lL][tT]|[rR][tT][Ss]|[nN][oO][pP]|[Ii][rR][eE][tT])"
    br=r"[bB][rR]\s+.+"
    xnor=r"[xX][nN][oO][rR]"
    label=r"[a-zA-Z0-9]+[:]"

    count=1

    if re.match(op_2, input_str, flags=0):
        #print(" 2 operand instructions")
        new_str = input_str.replace(" ", "")

        m = get_instruction_word(new_str[3:])
        count=count+m

        output.append((input_str,"2op"))

    elif re.match(hlt_nop_rts_iret, input_str, flags=0):
        #print(" no operand or rts or iret")
        if(len(input_str.split())<2 ):
            output.append((input_str, "nop_rts_hlt_iret"))  
        else:
            raise ValueError('A syntx error', input_str)

    elif re.match(reg, input_str, flags=0):
        jsr = r"[jJ][sS][rR]\s+.+"
        op_1 = r"[^bB][a-zA-Z][a-zA-Z]\s+.+"
        if re.search(jsr, input_str, flags=0):
            #print(" jump to sub instruction")
            output.append((input_str, "jsr"))

        elif re.search(op_1, input_str, flags=0):
            #print(" 1 operand instructions")
            new_str = input_str.replace(" ", "")

            m = get_instruction_word(new_str[3:])
            count = count+m
            output.append((input_str, "1op"))

        else :
            #print(" Branch instructions")
            output.append((input_str, "br"))

        
    elif re.match(br,input_str,flags=0) :                # special case instrunction BR 
        #print(" Branch instructions")
        output.append((input_str, "br"))
    elif re.match(xnor,input_str,flags=0):
        output.append((input_str, "xnor"))
    elif re.match(variables, input_str, flags=0):
        #print(" variables")   
        input_str=re.sub(' +', ' ', input_str)
        s = input_str.find(' ')
        input_str=input_str[s+1:]
        var, semicomma, val = input_str.partition(' ')
        #print("var name " ,var)
        dict[var]=beg

        output.append((input_str, "var"))

        #print(input_str)


    elif re.match(label, input_str, flags=0):
        count=0
        new_str = input_str.replace(":", "")
        #print(new_str+"end")
        dict[new_str] = beg
    else: 
        raise ValueError('A syntx error', input_str)

    return count

def assembler(lines,debug):
    ##################################ss###################
    # remove all white spaces except spaces from each line and remove comments
    new_lines=[]   # after remove comments and newlines;
    lines_with_type=[]  # pair of line with type of command
    dictionary={}   # store variable and labels and their address
    output=[]    # output op code
    for i in range(0,len(lines)):
        head, semicomma, comment = lines[i].partition(';')
        head = ' '.join(head.split())
        print (head)
        if (head!=''):
            new_lines.append(head)

    #######################################################
    # to determine address of variables and map them
    beg=0
    for i in range(0, len(new_lines)):
        debug.writelines(new_lines[i]+"      "+ "address " +str(beg)+'\n')
        try :
            m = count_words(new_lines[i], beg, dictionary, lines_with_type)
            beg=beg+m
        except ValueError as err:
            print(err.args)
            sys.exit()
    
    debug.writelines("-------------------"+'\n')

    generate_opcode(lines_with_type,dictionary,output,debug)

    debug.writelines("--------------------"+'\n')
    debug.writelines("successful"+'\n')
    
    return output
    

def main():
    #input_fil_name = input("input filename:")
    #output_fil_name = input("output filename:")
    #debug_fil_name = input("debug filename:")

    input_fil_name = "input.txt"
    output_fil_name = "out.txt"
    debug_fil_name = "debug.txt"   

    try:
        
        f = open(input_fil_name, 'r')
        lines = f.readlines()
        debug = open(debug_fil_name, 'w')
        output = open(output_fil_name, "w")
        out=assembler(lines,debug)
        output.writelines(out)

        f.close()
        output.close()
        debug.close()
    except IOError:
        print("Could not open or read one of the files:")
        sys.exit()
    
main() 

