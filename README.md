# Conditional Tree Bayesian Network

This package can be used as a library to fit a `Conditional Tree Bayesian Network (CTBN)`[[1]](#1).

This package has been published to [pypi](https://pypi.org/project/CTBN/) and can be installed using pip
```
pip install CTBN
```

The main module is the `CTBN` class. 

1. Use the `fit()` method to fit the `CTBN` to your multi-label classification data [[1]](#1). This method generates an optimal `CTBN` which is an instance of [DirectedGraph](https://github.com/brijml/CTBN/blob/main/src/graph_preliminaries.py) using the [Chu-Liu-Edmond's algorithm](https://github.com/brijml/CTBN/blob/main/src/msa.py) for finding a maximum spanning arborescence [[2]](#2).
2. The `predict()` method returns the most likely assignment to the class variables along with the probability of the assignment. The predict method uses the junction tree algorithm[[3]](#3) to run the most likely explanation(MLE) query.

### Usage

An example of using the package can be found in the jupyter notebook [here](https://github.com/brijml/CTBN/blob/main/compare-multiclass-classifier.ipynb).

```
# Import the CTBN class and assuming you have a dataset X_train and Y_train which are numpy arrays.
from ctbn import CTBN
model = CTBN()
model.fit(X_train, Y_train)

#Calling the fit method will generate an optimal CTBN graph of type
#DirectedGraph defined in src/graph_preliminaries.py

#Get predictions and the probability of a prediction on a single sample
#using the predict method. This method will in turn call the junction tree
#algorithm to run the max-sum algorithm on a test_sample.

max_log_prob, max_assignment = model.predict(test_sample)
```

### References
<a id="1">[1]</a> 
Batal, Iyad and Hong, Charmgil and Hauskrecht, Milos (2013). 
An Efficient Probabilistic Framework for Multi-Dimensional Classification. In <em>Proceedings  of  the  22nd  ACM  International Conference  on  Information  amp;  Knowledge  Management</em>, CIKM ’13, New York, NY,USA, pp. 2417–2422. Association for Computing Machinery. [https://doi.org/10.1145/2505515.2505594](https://doi.org/10.1145/2505515.2505594)

<a id="2">[2]</a>
Chu, Y. J. and T. H. Liu, "On the Shortest Arborescence
of a Directed Graph," Sci. Sinica, 14, 1965, pp. 1396-1400. 

<a id="3">[3]</a>
Koller, D., & Friedman, N. (2009). Probabilistic Graphical Models: Principles and Techniques. MIT Press.
