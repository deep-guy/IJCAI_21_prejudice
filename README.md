# IJCAI-21: Modelling Prejudice and Its Effect on Societal Prosperity

## Abstract
Prejudice is known to play an important role in multi-group dynamics in societies, but existing studies focus on the social-psychological knowledge behind the processes that lead to prejudice and its propagation. We create a framework that simulates the propagation of prejudice and measures its tangible impact on the prosperity of individuals as well as of larger social structures, which in our model include groups and factions within. Groups represent larger divisions in society and help us define prejudice, and factions represent smaller tight-knit circles that share similar opinions. We model social interactions based on the Continuous Prisoner's Dilemma (CPD) and introduce a novel type of agent called a prejudiced agent. Such agents’ cooperation is affected by a prejudice attribute, whose value updates over time, based both on the agent’s own experiences, and those of others in its faction. Our simulations show that while prejudiced agents have high relative prosperity, their presence degrades the overall prosperity levels of their societies. Prejudiced groups have higher levels of prosperity, even when they are the minority within society. As the relative size of unprejudiced groups increases over that of prejudiced groups, their prosperity level in the society increases, but still remains lower than their prejudiced counterparts.


## Code
This repository contains the code used for the modelling process as described in the paper, along with scripts to generate all plots and tables in the paper.

### Installation
Code must be run using Python 3 or higher. For a list of required modules, refer to requirements.txt, or simply run the following

    pip install -r requirements.txt

### Repo structure
All the classes for all the agent types that make up the base of our model may be found in the directories "twoGroups" and "nGroups", each of which contain the agent classes for two group and multi-group societies respectively. The remaining directories contain instantiations of the model class used for generating the corresponding result objects. The names of these directories are the same as the result object in the paper they correspond to. 

### Generating plots
Shell scripts have been written corresponding to each result object in the paper, and labelled accordingly. Therefore, to generate the plot in, say Fig 1(b), simply run

    bash 1b.sh

Each result is generated as an average of 10 runs of the model, which may take upto 5 minutes to finish execution. Note that some results are generated using the outputs from multiple experiments, and hence may take longer to generate. Fig 1(c) in particular shows the output of 20 experiments, and hence may take well over 1 hour to execute.

After execution, the pickle files for each model are saved in the respective directories. The final plot generated in saved as a png file in the root directory, and are labelled appropriately.

