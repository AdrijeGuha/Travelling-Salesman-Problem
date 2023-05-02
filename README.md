# Optimizing the travel distance for Covid personal
This project is built for an academic project exhibition with the community in mind.  
The project is built based on the concept of the [_Travelling Salesman Problem_](https://en.wikipedia.org/wiki/Travelling_salesman_problem). We are making our project to optimize the travel path taken by Covid personnel for visiting various houses in a locality. We have implemented [_Genetic Algorithm_](https://en.wikipedia.org/wiki/Genetic_algorithm) to find the optimum path solution and then have displayed the output as an HTML file which displays the map of the locality and traces the path to be taken for visiting the houses. The visiting sequence is also altered based on the rank given to the houses as per the comfortable visit time.  

#### Genetic Algorithm(GA)
For implementing the GA a population of 500 _house visit order_ is considered and a __fitness score__ is assigned to all the members of the population as per their travel distance for that particular order. A new generation is then created, with the fitness score in consideration, at random with the population members' having better fitness sore to have higher chances at being in the mating pool for creating a new population. A __mutations__ of a certain rate is also caused to happen while making new generation to aid our aim of finding an optimum solution of our problem. This process is continued for 100 generations. Then for another 100 generations, the program is executed to check if any change occurs in the _all time best solution_ obtained from the past 100 generations. If there is no change in the _all time best solution_, then considering this all-time best solution to be _the truly most optimum solution_ for our considered dataset, else we repeat the process for the next 100 generations till our goal of _no change in optimum route over 100 generations_ is obtained.  

## Bibliography
We were able to make this project only because of the guidance provided by Dr. Rakesh R., a professor of VIT, Bhopal(at present).  
Sources used for this project are the video tutorial series of 
- [_Travelling salesman_ in youtube](https://youtube.com/playlist?list=PLaBkvsv2Y7rJzlA2TYTMSHBvhTvaa6F_o), and 
- [Genetic Algorithm](https://thecodingtrain.com/more/archive/nature-of-code/9-genetic-algorithms/)  

both from [The coding train](https://thecodingtrain.com/).
