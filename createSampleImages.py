from mnist_1 import brain_learn
from array_converter import converter
from algorithms import compression_templates
import os
class create_samples:
    bl = None
    image_dir = 'images/'
    def __init__(self,imagedir = 'images/'):
        self.bl = brain_learn()
        self.image_dir = imagedir

    # verify the mnist data is loaded and the images have been compressed
    def verifyData(self):
        if not self.bl.trvecRed or len(self.bl.trvecRed) < 1:
            if  not self.bl.trvec and len(self.bl.trvec) < 1:
                print 'loading mnist training data'
                bl.loadMnist()
            bl.compressAllTrvec()
    
    # creates a sample of full and compressed images
    def generateSampleImages(self,count):
        c = converter(self.image_dir)
        ct = compression_templates()
        for x in range(0,count):
            expanded = ct.expandBytesToPixels(self.bl.trvecRed[x])
            c.save_image(expanded,os.path.combine(self.image_dir,"expand_" + str(self.bl.train_lables[x])))
        print "saved", count,"images to",
        
if __name__ =="__main__":
    cs = create_samples("web/src/assets/images")
    cs.verifyData()
    cs.generateSampleImages(10)

    
