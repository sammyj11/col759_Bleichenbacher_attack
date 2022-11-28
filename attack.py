from rsa import check_padding

import sys

import math
from rsa import *



"""

Takes a ciphertext, public modulus and public exponent as input as input

PARAMS:

ciphertext: a list of integers of size 128 bytes

N: the public modulus of size 128 bytes

e: the public exponent

"""
print("ans", file=open("dumpFile",'w'))

MAX_INT = sys.maxsize

k=128
def ceil(a, b):
    return a // b + (a % b > 0)

def floor(a, b):
    return a // b

def base_s_calculator(cipher_text,  num , N, e):

    flag = True
    print(cipher_text, int.from_bytes(cipher_text, 'big'))
    s = num
    i=0
    while flag:
        j= int.from_bytes(cipher_text, byteorder="big").bit_length()
        j = j//8 + (j%8>0)
        print(j,  file=open("dumpFile",'a'))
        modified_cipher_text = ((pow(s,e,N))*int.from_bytes(cipher_text, 'big'))%N
        length = modified_cipher_text.bit_length()

        length = length//8 + (length %8 >0)

        # print("hi1", length)
        
            
        checker = check_padding(list(modified_cipher_text.to_bytes(128, byteorder='big')))
        # print("here",i)
        if(s==118915):
            print(checker)

        
        
        
		
        if(checker):

            flag = False

            return s

        s+=1



def search_s_multiple(interval_list, cipher_text, N, e, old_s):
    # return 523918
    s_new = old_s

    flag = True

    while flag:

        modified_cipher_text = ((pow(s_new,e,N))*int.from_bytes(cipher_text, byteorder="big"))%N
        length = modified_cipher_text.bit_length()
        length = length//8 + (length %8 >0)
        checker = check_padding(list(modified_cipher_text.to_bytes(128, byteorder="big")))
        # print("in multiple")
        if(checker):

            flag = False

            return s_new

        s_new+=1



def search_s_singleton(interval, cipher_text, N, e, old_s, byteLen):

    r =  ceil(2*(interval[1]*old_s-2*byteLen),N)

    #check for ceil/floor in lower bound

    while True:

        for svalues in range( ceil((2*byteLen+r*N),interval[1]), ceil((3*byteLen+r*N),interval[0])):

            modified_cipher_text = ((pow(svalues,e,N))*int.from_bytes(cipher_text, byteorder="big"))%N
            length = modified_cipher_text.bit_length()
            length = length//8 + (length %8>0)
            checker = check_padding(list(modified_cipher_text.to_bytes(128, byteorder="big")))
            print("in singleton")
            if(checker ):

                

                return svalues

        

        r+=1




def update_interval(interval_list, s, byteLen, N):

    new_interval_list = []
    print(len(interval_list))
    print(s)
    for intervals in interval_list:
        print("yo")
        
        print(( ceil((intervals[0]*s-3*byteLen+1),N),  ceil((intervals[1]*s-2*byteLen),N)), len(interval_list), intervals , file=open("dumpFile",'a'))
        for r in range( ceil((intervals[0]*s-3*byteLen+1),N),  ceil((intervals[1]*s-2*byteLen),N)):

            new_interval_lower_bound = max(intervals[0], ceil((2*byteLen+r*N),s))
            new_interval_upper_bound = min(intervals[1], floor((3*byteLen-1+r*N),s))
            print("yo1", new_interval_lower_bound, new_interval_upper_bound  , file=open("dumpFile",'a') )
            flagg = False
            for i in range(len(new_interval_list)):
                
                #overlap check

                

                if(new_interval_list[i][0] <= new_interval_upper_bound and new_interval_list[i][1] >= new_interval_lower_bound):
                    print("overlap check dine", file=open("dumpFile",'a') )
                    new_interval_lower_bound_dash = min(new_interval_list[i][0],new_interval_lower_bound)

                    new_interval_upper_bound_dash = max(new_interval_upper_bound,new_interval_list[i][1])

                    new_interval_list[i] = (new_interval_lower_bound_dash,new_interval_upper_bound_dash)

                    flagg = True

                    break

            if(not(flagg)):

                #no overlap                 

                new_interval_list.append((new_interval_lower_bound,new_interval_upper_bound))

    
    # print(new_interval_list)
    return new_interval_list





def attack(cipher_text, N, e):

    """

    TODO: Implement your code here

    """

    byteLen = 2**(8*126)

    start_interval = [(2*byteLen, 3*byteLen-1)]

    num =  ceil(N,(3*byteLen))
    print(num,  file=open("dumpFile",'a'))
    print(N, 3*byteLen , file=open("dumpFile",'a'))
    first_s = base_s_calculator(cipher_text,num, N, e)
    print("hi", first_s, file=open("dumpFile",'a'))	
    # print(( ceil((start_interval[0]*first_s-3*byteLen+1),N),  ceil((start_interval[1]*first_s-2*byteLen),N)), file=open("dumpFile",'a'))
    print("done", first_s)
    # first_s = 456442

    new_interval_list = update_interval(start_interval, first_s, byteLen, N )
    print(new_interval_list, len(new_interval_list), file=open("dumpFile",'a'))


    flag = True

    

    while flag:



        if(len(new_interval_list)==1):

            if(new_interval_list[0][0]== new_interval_list[0][1]):

                flag = False

                return new_interval_list[0][0]%N

            

            first_s= search_s_singleton(new_interval_list[0],cipher_text, N, e, first_s, byteLen)

        

        elif(len(new_interval_list)>=2):

            first_s = search_s_multiple(new_interval_list, cipher_text, N, e, first_s+1)


        print("updating", len(new_interval_list), first_s,file=open("dumpFile",'a') )
        new_interval_list = update_interval(new_interval_list, first_s, byteLen, N)
        # print("updated", len(new_interval_list), first_s)




    """

    Return a list of integers representing the original message

    """

    return new_interval_list[0][0] %N
    
    
    
msg = 'Can you give 10 to me'
msg = list(bytes(msg, 'raw_unicode_escape'))
print(msg)
encrypted_msg = encryption(msg)
# print(pubKey.n)
# p=8176903505593156854431402498273534814878692959512360955565018584995350271585640492851236116512559338049248980432359822323415574668648147496967868563175768836250819375849491688485731635918360669937096148276708919163503399795407812994023044755615814912750399492819409752263037671326399577617970880313913198
p=attack(encrypted_msg, pubKey.n, pubKey.e)
bytelist= (list(p.to_bytes(128, byteorder="big")))
# print(''.join(bytelist).decode('utf-8'))
impIndex=0
for i in range(len(bytelist)):
    if i <=9:
        continue
    else:
        if(bytelist[i]==0):
            impIndex = i+1
            break
message = bytelist[impIndex:]
string = ''.join(map(chr, message))
# message = message.decode()
print(string)
print("done")
