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
    def verifyData(self,cnt):
        if not self.bl.trvecRed or len(self.bl.trvecRed) < 1:
            if  not self.bl.trvec or len(self.bl.trvec) < 1:
                print 'loading mnist training data'
                self.bl.loadMnist()
            self.bl.compressTrvecRange(cnt)
    
    # creates a sample of full and compressed images
    def generateSampleImages(self,count):
        c = converter(self.image_dir)
        ct = compression_templates()
        for x in range(0,count):
            print "trvecRed[x] 0:30", self.bl.trvecRed[x][0:30]
            expanded = ct.expandBytesToPixels(self.bl.trvecRed[x])
            print "Expanded array size", len(expanded), expanded
            c.save_image(expanded,os.path.join(self.image_dir,"expand_" + str(self.bl.train_labels[x])))
        print "saved", count,"images to", self.image_dir
        
if __name__ =="__main__":
    cs = create_samples()
    cs.verifyData(10)
    cs.generateSampleImages(10)

    
