This project aims to present concepts seen in the intelligent systems class, subject of the Computer Engineering course, UTFPR, Campus Curitiba. In the next topics I will be discussing a little about its implementation and its functioning, in general.

Implementation:
The implementation of this project is based on some pseudo-codes and pieces of code found on the internet, in addition to adjustments made by the students in the logical and functional part, to adapt the modeling done previously.

Behavior:
The program receives an image, like the example below, transforms the image to a gray scale and then discretizes the image into a matrix. The algorithm The star runs through this matrix looking for the optimal path, using the distance of the Pythagorean theorem as a heuristic function. After finding the final point, the program "recapitulates" the steps it took until it forms the shortest path between the two points on the map. 

