# Braincard module
# Copyright 2016 General Vision Inc.
#
# uses the module https://github.com/doceme/py-spidev

from constants import *

import spidev
spi = spidev.SpiDev()

def connect(speed):
    spi.open(0,0)
    spi.max_speed_hz = speed

def disconnect():
    spi.close()
    
#---------------------------------------
# read the register of a given module
#---------------------------------------
def read(module, reg):
    cmdread=[0x01, module, 0x00, 0x00, reg, 0x00, 0x00, 0x01, 0x00, 0x00];
    data= spi.xfer2(cmdread);
    return ((data[8] << 8) + data[9]);

#---------------------------------------
# write the register of a given module
#---------------------------------------
def write(module, reg, data):
    cmdwrite=[0x01, module + 0x80, 0x00, 0x00, reg, 0x00, 0x00, 0x01, (data & 0xFF00)>> 8, data & 0x00FF];
    data= spi.xfer2(cmdwrite);
  
#-----------------------------------------------
# broadcast a vector
#-----------------------------------------------
def broadcast(vector):
    l=len(vector);
    if l>1:
        for i in range(0,l-1):
            write(CM1K,COMP, vector[i]);
    write(CM1K, LCOMP, vector[l-1]);

#-----------------------------------------------
# Learn a vector using the current context value
#-----------------------------------------------
def learn(vector, category):
    broadcast(vector);
    write(CM1K, CAT,category);
    return(read(CM1K, NCOUNT));

#----------------------------------------------
# Recognize a vector and return the best match, or the 
# category, distance and identifier of the top firing neuron
#----------------------------------------------
def bestmatch(vector):
    broadcast(vector);
    distance = read(CM1K, DIST);
    category= read(CM1K, CAT); 
    nid =read(CM1K, NID);
    return(distance,category, nid);

#----------------------------------------------
# Recognize a vector and return the response  of up to K top firing neurons
# The response includes the distance, category and identifier of the neuron
# The Degenerated flag of the category is masked,
# Return the number of firing neurons or K whichever is smaller
#----------------------------------------------
def recognize(vector, K):
    broadcast(vector)
    results=[[0 for col in range(0,3)] for row in range(0,K)]
    recoNbr=0;
    while recoNbr<K:
        results[recoNbr][0]= read(CM1K, DIST);
        results[recoNbr][1]= read(CM1K, CAT) & 0x7FFF;
        results[recoNbr][2]= read(CM1K, NID);
        if results[recoNbr][0]==65535:
            break
        else:
            recoNbr=recoNbr+1
    return(recoNbr,results);
#---------------------------------------
# read word array at address
#---------------------------------------
def readAddr(address, length):   
    addr0=(int)(address & 0xFF000000) >> 24;
    addr1=(address & 0x00FF0000) >> 16;
    addr2=(address & 0x0000FF00) >> 8;
    addr3=address & 0x000000FF;
    len0=(length & 0x00FF0000) >> 16;
    len1=(length & 0x0000FF00) >> 8;
    len2=length & 0x000000FF;
    cmdread=[0x01, addr0, addr1, addr2, addr3, len0, len1, len2];
    databyte=[0 for i in range(0,length*2)]
    databyte2=spi.xfer2(cmdread+databyte);
    data=[0 for i in range(0,length)]
    for i in range(0,length):
        data[i] = (databyte2[8+(i*2)] << 8) + databyte2[8+(i*2)+1];
    return(data)

#---------------------------------------
# write word array at address
#---------------------------------------
def writeAddr(address, length, data):
    addr0=(int)(address & 0xFF000000) >> 24;
    addr1=(address & 0x00FF0000) >> 16;
    addr2=(address & 0x0000FF00) >> 8;
    addr3=address & 0x000000FF;
    len0=(length & 0x00FF0000) >> 16;
    len1=(length & 0x0000FF00) >> 8;
    len2=length & 0x000000FF;
    cmdwrite=[0x01, addr0 + 0x80, addr1, addr2, addr3, len0, len1, len2];
    databyte=[0 for i in range(0,length *2)]
    for i in range(0,length):
           databyte[(i*2)]= data[i] >> 8;
           databyte[(i*2)+1]=data[i] & 0x00FF;
    spi.xfer2(cmdwrite+databyte);
    
#--------------------------------------------------------------------------------------
# Read the contents of the neuron pointed by index in the chain of neurons
# Returns its context, model (256 bytes), active infuence field, minimum influence field, and category
#--------------------------------------------------------------------------------------
def reviewNeuron(index):
    TempNSR=read(CM1K, NSR); # backup the NSR
    write(CM1K,  NSR, 0x0010); # set the NSR to Save and Restore mode   
    write(CM1K,  RESETCHAIN, 0);
    # move to the neuron pointed by index in the chain
    for i in range(0,index):
        Temp=read(CM1K,  CAT); 
    # read the registers and memory of the neuron in focus
    ncr=read(CM1K, NCR);
    model=[0 for i in range(0,256)]
    for i in range(0,256):
        model[i]=read(CM1K, COMP);
    aif=read(CM1K, AIF);
    minif=read(CM1K, MINIF);
    cat=read(CM1K, CAT);
    write(1,  NSR, TempNSR); # restore the NSR
    return(ncr, model, aif, minif, cat);

#--------------------------------------------------------------------------------------
# Read the contents of the neuron pointed by index in the chain of neurons
# Returns an array of 264 bytes with the following format
# 2-bytes NCR, 256-bytes COMP, 2-bytes AIF, 2-bytes MINIF, 2-bytes CAT
#--------------------------------------------------------------------------------------
def readNeuron(index):
    TempNSR=read(CM1K, NSR); # backup the NSR
    write(CM1K,  NSR, 0x0010); # set the NSR to Save and Restore mode   
    write(CM1K,  RESETCHAIN, 0);
    # move to the neuron pointed by index in the chain
    for i in range(0,index):
        Temp=read(CM1K,  CAT); 
    # read the registers and memory of the neuron in focus
    neuron=[0 for i in range(0,264)]
    Temp=read(CM1K, NCR); 
    neuron[0]=(Temp & 0xFF00)>>8;
    neuron[1]= Temp & 0x00FF;
    for i in range(0,256):
        neuron[i+2]= read(CM1K, COMP);
    Temp=read(CM1K, AIF);
    neuron[258]=(Temp & 0xFF00)>>8;
    neuron[259]=Temp & 0x00FF;
    Temp=read(CM1K, MINIF);
    neuron[260]=(Temp & 0xFF00)>>8;
    neuron[261]=Temp & 0x00FF;
    Temp=read(CM1K, CAT);
    neuron[262]=(Temp & 0xFF00)>>8;
    neuron[263]=Temp & 0x00FF;
    write(1,  NSR, TempNSR); # restore the NSR
    return(neuron);

#-------------------------------------------------------------
# Read the contents of "ncount" neurons, with ncount being less than or equal
# to the number of committed neurons. 
# Returns an array of ncount records of 264 bytes with the following format
# 2-bytes NCR, 256-bytes COMP, 2-bytes AIF, 2-bytes MINIF, 2-bytes CAT
#-------------------------------------------------------------
def readNeurons(ncount):
    TempNSR=read(CM1K, NSR); # backup the NSR
    write(CM1K,  NSR, 0x0010); # set the NSR to Save and Restore mode
    write(CM1K,  RESETCHAIN, 0)
    neurons=[0 for i in range(0,ncount*264)]
    for i in range(0,ncount):
        Temp=read(CM1K, NCR);
        neurons[(i*264)]=(Temp & 0xFF00)>>8;
        neurons[(i*264)+1]=Temp & 0x00FF;
        for j in range(0,256):
            neurons[(i*264)+j+2]= read(CM1K, COMP);
        Temp=read(CM1K, AIF);
        neurons[(i*264)+258]=(Temp & 0xFF00)>>8;
        neurons[(i*264)+259]=Temp & 0x00FF;
        Temp=read(CM1K, MINIF);
        neurons[(i*264)+260]=(Temp & 0xFF00)>>8;
        neurons[(i*264)+261]=Temp & 0x00FF;
        Temp=read(CM1K, CAT);
        neurons[(i*264)+262]=(Temp & 0xFF00)>>8;
        neurons[(i*264)+263]=Temp & 0x00FF;
    write(1, NSR, TempNSR);
    return(neurons);

#-------------------------------------------------------------
# Clear and restore the content of ncount neurons from an array of
# ncount records of 264 bytes with the following format:
# 2-bytes NCR, 256-bytes COMP, 2-bytes AIF, 2-bytes MINIF, 2-bytes CAT
#-------------------------------------------------------------
def writeNeurons(neurons, ncount):
    TempNSR=read(CM1K, NSR);
    TempGCR=read(CM1K, GCR);
    write(CM1K, FORGET, 0);
    write(CM1K, NSR, 0x0010);
    write(CM1K, RESETCHAIN,0 );
    for i in range(0,ncount):
        write(CM1K, NCR, (neurons[i*264]<<8)+neurons[(i*264)+1]);
        for j in range(0,256):
            write(CM1K, COMP, neurons[(i*264)+2+j]);
        write(CM1K, AIF, (neurons[(i*264)+258]<<8)+neurons[(i*264)+259]);
        write(CM1K, MINIF, (neurons[(i*264)+260]<<8)+neurons[(i*264)+261]);
        write(CM1K, CAT, (neurons[(i*264)+262]<<8)+neurons[(i*264)+263]);
    write(CM1K, NSR, TempNSR);
    write(CM1K, GCR, TempGCR);

