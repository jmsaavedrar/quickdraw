"""
This scripts allows us to process the quickdraw dataset
We load the information fron ndjson files, filtering those images well recognized

Quickdraw dataset can be download by
gsutil -m cp 'gs://quickdraw_dataset/full/simplified/*.ndjson' .
"""
import pandas as pd
import numpy as np
import skimage.draw as draw
import matplotlib.pyplot as plt
import skimage.morphology as morph
import skimage.io as io
import argparse
import os
def compose_sketch(strokes, padding) :
    
    rows = []
    cols = []    
    # --------------------------------------------------
    # read rows and cols
    sketch = np.zeros((256 + 2*padding, 256+2*padding ), dtype = np.uint8)
    max_x = -1
    max_y = -1
    for stroke in strokes :        
        ys = stroke[1]        
        xs = stroke[0]                       
        for i  in range(1,len(ys)) :                        
            rr,cc = draw.line(ys[i-1], xs[i-1], ys[i], xs[i])
            max_x = max(np.max(cc), max_x) 
            max_y = max(np.max(rr), max_y)
            sketch[rr, cc] = 1
    
    ox = 127 - max_x // 2 
    oy = 127 - max_y // 2
    rr, cc = np.where(sketch == 1)
    sketch[:,:]=0
    sketch[rr + oy + padding, cc + ox + padding] = 1                   
    sketch = morph.binary_dilation(sketch, np.array([[0,1,0],[1,1,1],[0,1,0]]))
    return sketch

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', type=str, required = True)
    parser.add_argument('-category', type=str, required = True, help = 'a category name or a category file')
    parser.add_argument('-sample', type=int, required = True)
    args = parser.parse_args()
    sample_size = args.sample #1100  1000 train 100 test
    #category = 'nose'
    #category = '/mnt/hd-data/Datasets/quickdraw/categories.txt'
    category = args.category
    
    categories = []
    if os.path.isfile(category) :        
        with open(category) as fin :
            for category in fin :
                categories.append(category.strip())
    else :
        categories.append(category)
    #----------------------------------------------------
    # setting paths
    #path =  '/mnt/hd-data/Datasets/quickdraw/ndjson/'
    path = args.dir
    destine_path = os.path.join(path, '..', 'sketches')
    assert os.path.isdir(destine_path), '{} does not exist'.format(destine_path)
    for category in categories :
        destine_path = os.path.join(destine_path, category)
        if not os.path.isdir(destine_path) :
            os.mkdir(destine_path)
        #----------------------------------------------------
        # loading data as panda dataframe
        fname = os.path.join(path, category + '.ndjson')
        print('* Reading data from {}'.format(fname))
        df = pd.read_json(fname, lines = True)
        # setting image parameters 
        padding = 20
        size = 256
        #-----------------------------------------------------
        # filtering by recognized == True
        filter_values = np.where(df['recognized'] == True)
        df = df.loc[filter_values]
        df = df.sample(sample_size)    
        #-----------------------------------------------------
        total = len(df)
        print('----Number of sketches for {} -> {}'.format(category, total))
        print('----saving  sketches to {}'.format(destine_path))
        key_ids = df['key_id']
        drawings = df['drawing']    
        # random sampling             
        for i, index in enumerate(df.index):
            strokes = drawings[index]        
            sketch = compose_sketch(strokes, padding = padding)*255
            sketch = sketch.astype(np.uint8)
            sketch_id = key_ids[index]
            fout = os.path.join(destine_path, str(sketch_id) + '.png')
            io.imsave(fout, sketch)
            if (i + 1)  % 100 == 0 :
                print('----{}/{} saved'.format(i + 1, total))
                            
            
#             plt.imshow(sketch, cmap = 'gray')
#             plt.waitforbuttonpress(0.5)