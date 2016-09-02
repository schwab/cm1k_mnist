##
## Test SPI
##
## Series of SPI access to the Braincard including
## single and multiple Read/Write commands
##
## Adjust the clock speed settings if necessary for stability
##
import time

import Braincard
from constants import *

Braincard.connect(500000);

Braincard.write(CM1K,FORGET,0);

value1= 1;
value2= 4096;
value3=10;
length=10;
iteration=0;
error=0;

#while True:
while iteration<20:
    error=0;
    
    ## Single write to the MINIF and MAXIF registers
    value=Braincard.write(CM1K,MINIF, value1);
    value=Braincard.write(CM1K,MAXIF, value2);

    ## Multiple write to the COMP register
    ## after setting the neurons in save and restore mode
    Braincard.write(CM1K, NSR,16);
    Braincard.write(CM1K, RESETCHAIN,0);
    data=[0 for i in range(0,length)]
    for i in range(0,length):
        data[i]=value3+i;
    Braincard.writeAddr(0x01000001, length, data);
    Braincard.read(CM1K, CAT) ##to move to next neuron in the chain
    Braincard.write(CM1K, NSR,0); ##set CM1K in normal mode

    ## Single read to the MINIF and MAXIF registers
    ## and verification of the expected value
    value=Braincard.read(CM1K,MINIF);
    if (value!=value1):
        error=1;
        print("ERROR, incorrect Minif=%u" % value);
    
    value=Braincard.read(CM1K,MAXIF);
    if (value!=value2):
        error=2;
        print("ERROR2, incorrect Maxif=%u" % value);

    ## Multiple write to the COMP register
    ## after setting the neurons in save and restore mode
    Braincard.write(CM1K, NSR,16); ##set CM1K in save and restore mode
    Braincard.write(CM1K, RESETCHAIN,0);
    data=Braincard.readAddr(0x01000001, length);
    for i in range(0,length):
        if(data[i]!= value3+i):
            error=3;
            print("ERROR3, incorrect COMP %u = %u" % (i, data[i]));
    Braincard.read(CM1K, CAT) ##to move to next neuron in the chain
    Braincard.write(CM1K, NSR,0); ##set CM1K in normal mode

    if (error==0):
            print ("\nIteration= %u, Pass" % iteration);

    iteration=iteration+1;       
    value1=value1+1;
    if (value1==256):
        value1=0
    value2=value2-1;
    if (value2==0):
        value2=4096;
    value3=value3+1;
    if (value3==256):
        value3=0;


