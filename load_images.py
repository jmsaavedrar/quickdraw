# Copyright 2017 Google Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct
from struct import unpack
import numpy as np
import skimage.draw  as draw
import matplotlib.pyplot as plt  
import os

def unpack_drawing(file_handle):
    key_id, = unpack('Q', file_handle.read(8))
    country_code, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))
    image = []
    
    for i in range(n_strokes):
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        x = unpack(fmt, file_handle.read(n_points))
        y = unpack(fmt, file_handle.read(n_points))
        image.append((y,x))

    return {
        'key_id': key_id,
        'country_code': country_code,
        'recognized': recognized,
        'timestamp': timestamp,
        'image': image
        
        
    }


def unpack_drawings(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield unpack_drawing(f)
            except struct.error:
                break


path = '/mnt/hd-data/Datasets/quickdraw/binary'
for drawing in unpack_drawings(os.path.join(path, 'bee.bin')):
    # do something with the drawing
    print(drawing['key_id'])
    sketch = np.zeros((256,256), dtype = np.uint8)
    strokes = drawing['image']   
    for stroke in strokes :
        ys = stroke[0]        
        xs = stroke[1]
        for i  in range(1,len(ys)) :                        
            rr,cc = draw.line(ys[i-1], xs[i-1], ys[i], xs[i])
            sketch[rr,cc] = 255
        
    plt.imshow(sketch, cmap = 'gray')
    plt.show()
    