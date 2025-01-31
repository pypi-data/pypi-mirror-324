import numpy as np

X = np.array(['yes', 'no', 'maybe'])

uniques = np.unique(X)
n_examples, n_classes = len(X), len(uniques)

masks = X[None ,:] == uniques[:, None]
masks = masks.astype('int')

print(masks)