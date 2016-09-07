from mnist_1 import brain_learn
class create_samples:
    bl = None
    def __init__(self):
        bl = brain_learn()

    # verify the mnist data is loaded and the images have been compressed
    def verifyData(self):
        if not bl.trvecRed or len(bl.trvecRed) < 1:
            if  not bl bl.trvec and len(bl.trvec) < 1:
                print 'loading mnist training data'
                bl.loadMnist()
            bl.compressAllTrvec()
    
    # creates a sample of full and compressed images
    def generateSampleImages(self,count):
        pass
        


    
