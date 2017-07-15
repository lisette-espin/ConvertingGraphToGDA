# ConvertingGraphToGDA

This script converts a graph file to GDA. The main goal is to pass a GDA file to the NetKit-srl[2] software for classification using relational classifiers.
Format files supported:
- .mat used in the paper "Social Structure of Facebook Networks"[1].

## Usage:
```
python to_gda.py <path_to_file>/<filename>.mat <classname> <value_missing_value> <path_output>
```

### Example:
```
python to_gda.py /Users/espin/Documents/Caltech36.mat status 0 results/
```

#### [File.mat]
Contains the graph Caltech36.mat, writen in .mat format to be converted
- attribute A contains the adjacency matrix and local_info the node attrinutes

#### [classname]
Every node in this graph contains 7 attributes: LA = ['status', 'gender', 'major', '2major', 'dorm', 'year', 'highschool']
- Thus, classname should be listed in LA
- The column classname is sent as last in a dataframe 

#### [value_missing_value]
Missing values in this type of graph are represented as 0
- Thus, if this parameter is set to zero, then all zeros are converted to '?'

#### [path_output]
Where to store the .gda files

## Output:
This script returns two .gda files:
- nodes.gda: every line (row) represents a node, and every column an attribute (comma separated)
```
Name,attr1,att2,att3,att4,att5,att6,att7
node237,1,199,?,169,2008,3387,1
node546,1,199,?,165,2006,3172,1
node547,1,201,?,171,2008,9773,2
...
```

- edges.gda: ever two lines represent a simple link between 2 nodes (link1 nodeA \n link2 nodeB: nodeA -- nodeB)
```
link,entity
link1,node541
link1,node38
link2,node541
...
```

## [References]
1. Caltech36,mat: Amanda L. Traud, Peter J. Mucha, and Mason A. Porter, Social Structure of Facebook Networks, arXiv:1102.2166
2. NetKit-srl: Sofus A. Macskassy , Foster Provost "Classification in Networked Data: A toolkit and a univariate case study," Journal of Machine Learning, 8(May):935-983, 2007.

