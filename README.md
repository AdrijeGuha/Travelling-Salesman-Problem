# Optimizing the travel distance for Covid personal
--------------------------
This project is built for an academic project exhibition with the community in mind.  
The project is built using the concept of `Travelling Salesman Problem`. We are making our project to optimize the travel path taken by a Covid personal for visiting houses in a locality. We have implemented `Genetic Algorithm` to find the optimum path solution and then have displayed the output as an html file which has the map of teh locality and traces the path to be taken for visiting the houses. The visiting sequence is also alterde based on the rank given to the houses as per the comfortable visit time to the houses.  
## Genetic Algorithm(GA)
For implementing the Genetic Algorithm(GA) we are considering a population of 500 _house visit order_ and then are assigning __fitness score__ to various members of our population as per their travel distance for that perticular order. We then create a new generation, with the fitness score in consideration, at random with the population members havig better fitness sore to have higher chances at being in the mating pool for creating new population. We also cause a __mutations__ of certain rate to happen while making new generation to aid our cause of finding a optimum route. We continue this process for next 200 generations. Then check for another 100 generation to see if there has been any change in the all time best solution obtained till now. If there happens to be no change then considering this all time best to be truely the most optimum solution for our considered dataset, else we repeat the process for next 100 generation till our goal of _no change in optimum route over 100 generations_ is obtained.  
## Biblography
This project could have been made only because of the guidance provided by Mr. Rakesh R., a professor of VIT, Bhopal(at present).  
Sources used for this project are the video tutorial series of 
- [_Travelling salesman_ in youtube](https://youtube.com/playlist?list=PLaBkvsv2Y7rJzlA2TYTMSHBvhTvaa6F_o), and 
- [Genetic Algorithm](https://thecodingtrain.com/more/archive/nature-of-code/9-genetic-algorithms/)  

both from [The coding train](https://thecodingtrain.com/).
