##
## Simple Script to test access to the neurons of the BrainCard
##
## Refer to Docs/Test_SimpleScript.pdf from General Vision for
## details about this script.
##
import time
import Braincard
from constants import *

Braincard.connect(500000);

Braincard.write(CM1K,FORGET,0);
time.sleep(0.1);

value=Braincard.read(CM1K,MINIF);
print ("Read default Minif=%u" % value);

value=Braincard.read(CM1K,MAXIF);
print ("Read default Maxif=%u" % value);

len=750;
vector=[0 for i in range(len)]

print("\nLearn as category 55 the vector "),
for i in range(0,len):
    vector[i]=11
    print("%u, " % (vector[i])),
Braincard.learn(vector,55);

print("\nLearn as category 33 the vector "),
for i in range(0,len):
    vector[i]=15
    print("%u, " % (vector[i])),
Braincard.learn(vector,33);

print("\nLearn as category 100 the vector "),
for i in range(0,len):
    vector[i]=20
    print("%u, " % (vector[i])),
ncount=Braincard.learn(vector,100);

## display the content of the neurons
print("\n\nRead the content of the %u committed neurons" % ncount);
for i in range(0,ncount):
    ncr, model, aif, minif, cat = Braincard.reviewNeuron(i)
    print("\nncr=%u \tcat=%u \taif=%u \tmodel:" % (ncr, cat, aif)),
    for j in range(0,len(model) -1):
        print("\t%u" % model[j]),        

## In case of multiple firing, read the response of
## at least the top 3 firing neurons
K=3;

print("\n\nBroadcast vector "),
for i in range(0,len):
    vector[i]=12
    print("%u, " % (vector[i])),
print("");
respLevel, results=Braincard.recognize(vector,K);
for i in range(0,respLevel):
    print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
print("Observation: recognized by neurons 1 and 2, but closer to 1\n");

print("\nBroadcast vector "),
for i in range(0,len):
    vector[i]=14
    print("%u, " % (vector[i])),
print("");
respLevel, results=Braincard.recognize(vector,K);
for i in range(0,respLevel):
    print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
print("Observation: recognized by neurons 1 and 2, but closer to 2\n");

print("\nRecognize vector "),
for i in range(0,len):
    vector[i]=13
    print("%u, " % (vector[i])),
print("");
respLevel, results=Braincard.recognize(vector,K);
for i in range(0,respLevel):
    print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
print("Observation: equi-distant to neurons 1 and 2\n");

print("\nBroadcast vector "),
for i in range(0,len):
    vector[i]=30
    print("%u, " % (vector[i])),
print("");
respLevel, results=Braincard.recognize(vector,K);
for i in range(0,respLevel):
    print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
print("Observation: unknown to all neurons");

print("\nLearn as category 100 vector "),
for i in range(0,len):
    vector[i]=13
    print("%u, " % (vector[i])),
ncount=Braincard.learn(vector,100);

## display the content of the neurons
print("\n\nRead the content of the %u committed neurons" % ncount);
for i in range(0,ncount):
    ncr, model, aif, minif, cat = Braincard.reviewNeuron(i)
    print("\nncr=%u \tcat=%u \taif=%u \tmodel:" % (ncr, cat, aif)),
    for j in range(0,len):
        print("\t%u" % model[j]),    
    
## save knowledge
## neuronsContent=Braincard.readNeurons(ncount);
