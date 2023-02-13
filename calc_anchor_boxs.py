from utils.autoanchor import *


kmean_anchors(dataset='./data/diff-char.yaml', n=9, img_size=416, thr=4.0, gen=1000, verbose=True)