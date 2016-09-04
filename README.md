## MNIST on a CM1K
This research project is to attempt to implent a full MNIST recognizer on the CMK1 with only 1K neurons.  The CM1K is a hardware implemenation of a neural network array.  This chip is fully parallized and requires a fixed amount of time (nano seconds) to perform a single data recogniztion.  The word from the manufacture is that the CM1K cannot store enough data to recognize all the images in the minst dataset at the same time.  

The most limiting factor seems to be that even though there are 1000 nuerons, each one can only "see" 255 inputs at time The neurons are arranged as a fully parrallel single layer perception.  This means a method must be deviced to reduce the >700 pixels of each MNIST image to something <= 255 without loosing any information that would impede its recognition ability.  The plan is to perform even this image compression with CM1K itself reducing each ~64 bits of the input image to 8 thereby reducing the overall image to < 255 bytes for a second recognition pass.

### Proposed Flow
1. CPU - produce a map of each 8 byte combination mapped to a compressed 1 byte outpu
2. CPU - expose the CM1K to the map and train it
3. CM1K - extract the learned memory back to the cpu for caching for later
4. CM1K - Generate 1byte ouputs for each 8bytes of the training data
5. CPU - store the 1byte * ~255 outputs as "scaled_training" 
6. CM1K - train on some of the 60K scaled_training data 
7. CPU - peform a custom training algorithm optimized for high speed learning (details to be discussed later)
8. 
## Usage
```
./get_data.sh   # download the mnist data to the data/ folder
```
## Relies on code from 
* python-mnist : https://pypi.python.org/pypi/python-mnist/0.3
* BSP_BrainCard/RaspberryPi : 
