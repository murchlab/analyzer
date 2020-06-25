# Analyzer
Version  0.1

Tools for analyzing and processing the measurement data

## Design logic and Terminology

* Native python data types are preferred (without introducing too many customized classes)
* A **sequence** comprises many **steps**
* A **Sequence** object is implemented as a python `list` of **step** objects
* The function `analyzer.broadcast` is for broadcasting a function over a **Sequence** object
* `num_step` defines the number of steps in a sequence

## Data visualization

![quantum trajectory sequence](images/quantum_trajectory_sequence.png)

For the usage please check out

`examples/display_sequence.py`