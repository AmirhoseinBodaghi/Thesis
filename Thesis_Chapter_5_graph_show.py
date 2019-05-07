def graph_generator ():
    import networkx as nx
##    s = nx.utils.powerlaw_sequence(1000, 2.5) ########## 
##    G = nx.expected_degree_graph(s, selfloops=False)  #########
    G = nx.scale_free_graph(1000,alpha=0.32, beta=0.45, gamma=0.23) ######## here we make a scale free network which is directed :) please notice : here adjaceny matris is a hetrogounos matrix and for example adjaceny[12] = [1, 3, 179 ,570] means that node 12 followes nodes 1 , 3 , 179 , 570 , in other words nodes 1 , 3 , 179 and 570 have influence on node 12 and can cause a change in state of node 12  
    pos=nx.spring_layout(G) #this command makes a layout of position of all nodes (instead of spring_layout you can use fruchterman_reingold_layout or other layouts so you will have different figures for graph) ,since we want to have different color for different states of nodes so we have to first make a layout then in graph draw function we make node by different colores,in fact ( I seperated this command and also above command (G=nx.Graph()) from the function of graph draw for two reasons : 1- seperating pos command causes we have a fixed layout for all graph draw (for example if initial node is located in south west of picture of graph(in graph draw plot)then for any time we plot graph again (for example for different timesteps) then the initial infected node is still in south west of graph plot, so we can see spread of rumor and its expand from south west of graph during different timesteps  2- by seperating graph generator function (G = nx.Graph command) we save time because we perform this command only one time and for any times that we plot graph we would not use this command again, so plots will be made fastly  
    return G,pos
#-------------------------------------
def main():
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import networkx as nx
    import numpy as np
    total_degree_list = []
    total_betweenness_list = []
    total_closeness_list = []
    
    i = 0
    while i < 20 :
        G,pos = graph_generator ()
        nx.draw(G,pos)
        degree_list = []
        betweenness_list = []
        closeness_list = []
        for node , degree in (nx.degree_centrality(G)).items() :  #The in degree centrality for a node v is the fraction of nodes, that are connected to node v
            degree_list.append(degree)
        for node , betweenness in nx.betweenness_centrality(G).items() :
            betweenness_list.append(betweenness)
        for node , closeness in nx.closeness_centrality(G).items() :
            closeness_list.append(closeness)

        total_degree_list.append(np.mean(degree_list))
        total_betweenness_list.append(np.mean(betweenness_list))    
        total_closeness_list.append(np.mean(closeness_list))

        i+=1

    print("degree :" , np.mean(total_degree_list))
    print("betweenness :" , np.mean(total_betweenness_list))
    print("closeness :" , np.mean(total_closeness_list))
    
#------------------
main()
input ("press enter to exit.")
