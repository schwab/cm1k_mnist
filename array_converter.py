import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random 
from PIL import Image

class converter:
    base_folder=''
    def __init__(self,folder='image/'):
        self.base_folder=folder
    def save_image(self,data,filename):
        plt.imsave(this.base_folder + filename,data.reshape(28,28),cmap=cm.gray)

    def randomArray(self,alen):
        aset = np.zeros(alen)
        for x in range(0,alen):
            p = random.randint(0,2)       
            if p >= 1:
                aset[x] = random.randint(0,255)
        return aset
