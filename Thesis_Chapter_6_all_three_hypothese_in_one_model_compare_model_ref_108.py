class Node (object) :
    import networkx as nx
    def __init__ (self,number):
        self.number = number
        self.state = "S"
        self.primary_state = None
        self.time = 0

    def get_neighbor (self,all_node,adjacency):
        self.neighbor = []
        for number in adjacency[self.number] :
            self.neighbor.append(all_node[number])


    def STOI1 (self,t):
        self.state = "I1"
        self.time = t

    def STOI2 (self,t):
        self.state = "I2"
        self.time = t

    def STOB1 (self,t):
        self.state = "B1"
        self.time = t

    def STOB2 (self,t):
        self.state = "B2"
        self.time = t

    def B1TOI1 (self,t):
        self.state = "I1"
        self.time = t

    def B1TOS (self,t):
        self.state = "S"
        self.time = t

    def B2TOI2 (self,t):
        self.state = "I2"
        self.time = t

    def B2TOS (self,t):
        self.state = "S"
        self.time = t

    def I1TOI12 (self,t):
        self.state = "I12"
        self.time = t

    def I1TOR1 (self,t):
        self.state = "R1"
        self.time = t

    def I2TOI12 (self,t):
        self.state = "I12"
        self.time = t

    def I2TOR2 (self,t):
        self.state = "R2"
        self.time = t

    def I12TOR1 (self,t):
        self.state = "R1"
        self.time = t
    
    def I12TOR2 (self,t):
        self.state = "R2"
        self.time = t
    
#-------------
class Network_New_Model (object):
    def __init__ (self,BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2,adjacency):
        number = 0
        self.network_all_node = []
        self.timestep = 0
        self.number_of_nodes_in_S_state_per_timestep = []
        self.number_of_nodes_in_I1_state_per_timestep = []
        self.number_of_nodes_in_I2_state_per_timestep = []
        self.number_of_nodes_in_B1_state_per_timestep = []
        self.number_of_nodes_in_B2_state_per_timestep = []
        
        
        while number < 1000 :
            self.network_all_node.append (Node(number))
            number += 1
        for node in self.network_all_node :
            node.get_neighbor (self.network_all_node,adjacency)


    def __str__(self):
        S_number = 0
        I1_number = 0
        I2_number = 0
        B1_number = 0
        B2_number = 0
        for node in self.network_all_node :
            if node.state == "S" :
                S_number += 1
            if node.state == "I1" :
                I1_number += 1
            if node.state == "I2" :
                I2_number += 1
            if node.state == "B1" :
                B1_number += 1
            if node.state == "B2" :
                B2_number += 1
                
        rep = "Timestep number : " + str(self.timestep) + "\n\n" + "number of S nodes : " + str(S_number) + "\n\n" + "number of I1 nodes : " + str(I1_number) + "\n\n" + "number of I2 nodes : " + str(I2_number) +  "\n\n" + "number of B1 nodes : " + str(B1_number) + "\n\n" + "number of B2 nodes : " + str(B2_number) + "\n ----------------------"
        return rep

    def number_of_nodes_in_each_state_per_timestep (self) : 
        S_number = 0
        I1_number = 0
        I2_number = 0
        B1_number = 0
        B2_number = 0

        for node in self.network_all_node :
            if node.state == "S" :
                S_number += 1
            if node.state == "I1" :
                I1_number += 1
            if node.state == "I2" :
                I2_number += 1
            if node.state == "B1" :
                B1_number += 1
            if node.state == "B2" :
                B2_number += 1
                

        self.number_of_nodes_in_S_state_per_timestep.append(S_number)
        self.number_of_nodes_in_I1_state_per_timestep.append(I1_number)
        self.number_of_nodes_in_I2_state_per_timestep.append(I2_number)


    def initial_infection (self,g,f):
        self.network_all_node[g].state = "I1"
        self.network_all_node[f].state = "I2"
        




    
    def change (self,BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2, t) :

        import random
        import math ######## for the following line we need math module, please notice the number 10 in the following line can be any number from 1 to infinity , when it goes to infinity the influence of  number of neighbors decreses ,for this run we set it 10
         
        for node in self.network_all_node :
            number_I1_state_neighbor = 0
            number_I2_state_neighbor = 0

            #----.-----.-----.-----.-----.----.-----.-----.-----.-----.----.-----.-----.-----.-----
            
            if node.state == "S" :
                number_of_neighbors = len (node.neighbor) ######## we need to know number of neighbors to implement hypothesis of this model (more neighbores less the influence of one message !)
                impact_of_all_I1_neighbors = []
                impact_of_all_I2_neighbors = []
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        delta_time = t - (neighbor.time + 1) 
                        impact_of_spreader_I1 = math.exp(-delta_time) #the impact of spreader in one step after getting spreader is 1 and then it exponetialy decreses
                        impact_of_all_I1_neighbors.append (impact_of_spreader_I1)
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        delta_time = t - (neighbor.time + 1) 
                        impact_of_spreader_I2 = math.exp(-delta_time) #the impact of spreader in one step after getting spreader is 1 and then it exponetialy decreses
                        impact_of_all_I2_neighbors.append (impact_of_spreader_I2)
                        number_I2_state_neighbor += 1
                        
                #computing non_spontaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_SI1 - GAMMA_SB1 - GAMMA_SI2 - GAMMA_SB2         
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state                   

                    # Computing  T_SI1B1 and T_SI2B2 
                    T_SI1B1 = 1 - T_SI1I1
                    T_SI2B2 = 1 - T_SI2I2
                                           
                    message_coefficient = math.exp((1- number_of_neighbors)/20) ######## (the first hypothesis) this message_coefficient decreses by increasing the number of neighbors (the maximum is 1 when just one neighbor exists. please notice number of neighbors can't be zero because the upper condition  "if number_I1_state_neighbor + number_I2_state_neighbor != 0" doesn't allow that. 
                    BETA_SI1 = BETA_SI1*message_coefficient ####### by this line we make a connection between number of neighbors and the messages's power of influence 
                    BETA_SI2 = BETA_SI2*message_coefficient ####### by this line we make a connection between number of neighbors and the messages's power of influence
                    
                    # Computing of required parameters : {{{                        

                    real_number_I1_state_neighbor = sum (impact_of_all_I1_neighbors) #this is were we implement the second hypotheis
                    real_number_I2_state_neighbor = sum (impact_of_all_I2_neighbors) #this is were we implement the second hypotheis
                    #computing F_SI1 and F_SI2
                    a = (BETA_SI1*real_number_I1_state_neighbor)/(1-0.5*BETA_SI1)
                    b = (BETA_SI2*real_number_I2_state_neighbor )/(1-0.5*BETA_SI2)
                    c = 1-((1-BETA_SI1)**real_number_I1_state_neighbor)*((1-BETA_SI2)**real_number_I2_state_neighbor )
                    d = a + b 
                    if d == 0 :
                        d = 1.0e-323 #since numbers less than this, will be set as 0 by python and this causes us to have division by zero, we set this small number for them
                    F_SI1 = (a*c)/d
                    F_SI2 = (b*c)/d 
                    #computing G functions
                    G_SI1 = F_SI1*T_SI1I1
                    G_SI2 = F_SI2*T_SI2I2
                    G_SB1 = F_SI1*T_SI1B1
                    G_SB2 = F_SI2*T_SI2B2

                    #computing G_S0 ie: no success connected transition
                    G_S0 = 1 - c  #look at the c above
                    #   }}}

                else :
                    G_SI1 = 0
                    G_SI2 = 0
                    G_SB1 = 0
                    G_SB2 = 0
                    G_S0  = 1
                
                #Total Transitions (mass function rule is achieved because :  P_S_TO_I1 + P_S_TO_I2 + P_Remain_S = 1   )
                P_S_TO_I1 = GAMMA_SI1 + non_simultaneous_transition_probability * G_SI1
                P_S_TO_B1 = GAMMA_SB1 + non_simultaneous_transition_probability * G_SB1
                P_S_TO_I2 = GAMMA_SI2 + non_simultaneous_transition_probability * G_SI2
                P_S_TO_B2 = GAMMA_SB2 + non_simultaneous_transition_probability * G_SB2
                P_Remain_S = non_simultaneous_transition_probability * G_S0

                #change
                x = random.uniform(0,1)
                if x <= P_S_TO_I1 :
                    node.primary_state = "I1"
                elif x <= (P_S_TO_I1 + P_S_TO_B1) :
                    node.primary_state = "B1"    
                elif x <= (P_S_TO_I1 + P_S_TO_B1 + P_S_TO_I2)  :
                    node.primary_state = "I2"
                elif x <= (P_S_TO_I1 + P_S_TO_B1 + P_S_TO_I2 + P_S_TO_B2)  :
                    node.primary_state = "B2"
                else :
                    node.primary_state = "S" #means  (P_S_TO_I1_C + P_S_TO_B1 + P_S_TO_I2 + P_S_TO_B2) < x <= 1    ie: P_Remain_S was succesful
                
            #----.-----.-----.-----.-----
            #----.-----.-----.-----.-----
            #----.-----.-----.-----.-----
            elif node.state == "B1" :
                number_of_neighbors = len (node.neighbor) ######## we need to know number of neighbors to implement hypothesis of this model (more neighbores less the influence of one message !)
                impact_of_all_I1_neighbors = []
                impact_of_all_I2_neighbors = []
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        delta_time = t - (neighbor.time + 1) 
                        impact_of_spreader_I1 = math.exp(-delta_time) #the impact of spreader in one step after getting spreader is 1 and then it exponetialy decreses
                        impact_of_all_I1_neighbors.append (impact_of_spreader_I1)
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        delta_time = t - (neighbor.time + 1) 
                        impact_of_spreader_I2 = math.exp(-delta_time) #the impact of spreader in one step after getting spreader is 1 and then it exponetialy decreses
                        impact_of_all_I2_neighbors.append (impact_of_spreader_I2)
                        number_I2_state_neighbor += 1


                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_B1I1 - GAMMA_B1S 
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state

                                           
                    message_coefficient = math.exp((1- number_of_neighbors)/20) ######## (the first hypothesis) this message_coefficient decreses by increasing the number of neighbors (the maximum is 1 when just one neighbor exists. please notice number of neighbors can't be zero because the upper condition  "if number_I1_state_neighbor + number_I2_state_neighbor != 0" doesn't allow that. 
                    BETA_B1I1 = BETA_B1I1*message_coefficient ####### by this line we make a connection between number of neighbors and the messages's power of influence 
                    BETA_B1I2 = BETA_B1I2*message_coefficient ####### by this line we make a connection between number of neighbors and the messages's power of influence
                    
                    # Computing of required parameters : {{{                        

                    real_number_I1_state_neighbor = sum (impact_of_all_I1_neighbors) #this is were we implement the second hypotheis
                    real_number_I2_state_neighbor = sum (impact_of_all_I2_neighbors) #this is were we implement the second hypotheis
                    
                    # Computing of required parameters : {{{                         
                    #computing F_B1I1 and F_B1I2
                    a = (BETA_B1I1*number_I1_state_neighbor)/(1-0.5*BETA_B1I1)
                    b = (BETA_B1I2*number_I2_state_neighbor)/(1-0.5*BETA_B1I2)
                    c = 1-((1-BETA_B1I1)**number_I1_state_neighbor)*((1-BETA_B1I2)**number_I2_state_neighbor)
                    d = a + b
                    if d == 0 :
                        d = 1.0e-323 #since numbers less than this, will be set as 0 by python and this causes us to have division by zero, we set this small number for them

                    F_B1I1 = (a*c)/d
                    F_B1I2 = (b*c)/d
                    #computing G functions
                    G_B1I1 = F_B1I1 + F_B1I2
                    #computing G_S0 ie: no succesful connected transition
                    G_B10 = 1 - c  #look at the c above
                    #   }}}

                else :
                    G_B1I1 = 0
                    G_B10  = 1

                #Total Transitions  (mass function rule is achieved because :  P_B1_TO_I1 + P_B1_TO_S + P_Remain_B1  = 1   )
                P_B1_TO_I1 = GAMMA_B1I1 + non_simultaneous_transition_probability * G_B1I1
                P_B1_TO_S = GAMMA_B1S
                P_Remain_B1 = non_simultaneous_transition_probability * G_B10

                #change
                x = random.uniform(0,1)
                if x <= P_B1_TO_I1 :
                    node.primary_state = "I1"
                elif x <= (P_B1_TO_I1 + P_B1_TO_S) :
                    node.primary_state = "S"
                else :
                    node.primary_state = "B1" #means  (P_B1_TO_I1 + P_B1_TO_S ) < x <= 1    ie: P_Remain_B1 was succesful
                    
                
            #----.-----.-----.-----.-----
            #----.-----.-----.-----.-----
            #----.-----.-----.-----.-----


            elif node.state == "B2" :
                number_of_neighbors = len (node.neighbor) ######## we need to know number of neighbors to implement hypothesis of this model (more neighbores less the influence of one message !)
                impact_of_all_I1_neighbors = []
                impact_of_all_I2_neighbors = []
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        delta_time = t - (neighbor.time + 1) 
                        impact_of_spreader_I1 = math.exp(-delta_time) #the impact of spreader in one step after getting spreader is 1 and then it exponetialy decreses
                        impact_of_all_I1_neighbors.append (impact_of_spreader_I1)
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        delta_time = t - (neighbor.time + 1) 
                        impact_of_spreader_I2 = math.exp(-delta_time) #the impact of spreader in one step after getting spreader is 1 and then it exponetialy decreses
                        impact_of_all_I2_neighbors.append (impact_of_spreader_I2)
                        number_I2_state_neighbor += 1

                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_B2I2 - GAMMA_B2S
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state

                    message_coefficient = math.exp((1- number_of_neighbors)/20) ######## (the first hypothesis) this message_coefficient decreses by increasing the number of neighbors (the maximum is 1 when just one neighbor exists. please notice number of neighbors can't be zero because the upper condition  "if number_I1_state_neighbor + number_I2_state_neighbor != 0" doesn't allow that. 
                    BETA_B2I1 = BETA_B2I1*message_coefficient ####### by this line we make a connection between number of neighbors and the messages's power of influence 
                    BETA_B2I2 = BETA_B2I2*message_coefficient ####### by this line we make a connection between number of neighbors and the messages's power of influence
                    
                    # Computing of required parameters : {{{                        

                    real_number_I1_state_neighbor = sum (impact_of_all_I1_neighbors) #this is were we implement the second hypotheis
                    real_number_I2_state_neighbor = sum (impact_of_all_I2_neighbors) #this is were we implement the second hypotheis
                    
                    # Computing of required parameters : {{{                        
                    #computing F_B2I1 and F_B2I2
                    a = (BETA_B2I1*number_I1_state_neighbor)/(1-0.5*BETA_B2I1)
                    b = (BETA_B2I2*number_I2_state_neighbor)/(1-0.5*BETA_B2I2)
                    c = 1-((1-BETA_B2I1)**number_I1_state_neighbor)*((1-BETA_B2I2)**number_I2_state_neighbor)
                    d = a + b
                    if d == 0 :
                        d = 1.0e-323 #since numbers less than this, will be set as 0 by python and this causes us to have division by zero, we set this small number for them
                    F_B2I1 = (a*c)/d
                    F_B2I2 = (b*c)/d
                    #computing G functions
                    G_B2I2 = F_B2I1 + F_B2I2
                    #computing G_S0 ie: no success connected transition
                    G_B20 = 1 - c  #look at the c above
                    #   }}}
                    
                else :
                    G_B2I2 = 0
                    G_B20  = 1
                        
                #Total Transitions  (mass function rule is achieved because :  P_B2_TO_I2 + P_B2_TO_S + P_Remain_B2  = 1   )
                P_B2_TO_I2 = GAMMA_B2I2 + non_simultaneous_transition_probability * G_B2I2
                P_B2_TO_S = GAMMA_B2S
                P_Remain_B2 = non_simultaneous_transition_probability * G_B20


                #change
                x = random.uniform(0,1)
                if x <= P_B2_TO_I2 :
                    node.primary_state = "I2"
                elif x <= (P_B2_TO_I2 + P_B2_TO_S) :
                    node.primary_state = "S"
                else :
                    node.primary_state = "B2" #means  (P_B2_TO_I2 + P_B2_TO_S ) < x <= 1    ie: P_Remain_B2 was succesful


            #----.-----.-----.-----.-----
            #----.-----.-----.-----.-----
            #----.-----.-----.-----.-----


            else :
                None # means node was in I1 or I2 state and these nodes never participate in any change process fro themselves and forever will be in their state (even though this can be a subject for second paper in which these states will change to other states)
                    
        #----.-----.-----.-----.-----.----.-----.-----.-----.-----.----.-----.-----.-----.-----
                    
        #----.-----.-----.-----.-----.----.-----.-----.-----.-----.----.-----.-----.-----.-----


        for node in self.network_all_node :
            if node.state == "S" and node.primary_state == "I1" :
                node.STOI1(t)
                
            elif node.state == "S" and node.primary_state == "I2" :
                node.STOI2(t)

            elif node.state == "S" and node.primary_state == "B1" :
                node.STOB1(t)

            elif node.state == "S" and node.primary_state == "B2" :
                node.STOB2(t)

            elif node.state == "B1" and node.primary_state == "I1" :
                node.B1TOI1(t)

            elif node.state == "B2" and node.primary_state == "I2" :
                node.B2TOI2(t)

            elif node.state == "B1" and node.primary_state == "S" :
                node.B1TOS(t)

            elif node.state == "B2" and node.primary_state == "S" :
                node.B2TOS(t)
                
            else :
                None

    def time (self,t):
        self.timestep = t

#----------------
def graph_generator ():
    import networkx as nx
    s = nx.utils.powerlaw_sequence(1000, 2.5)
    G = nx.expected_degree_graph(s, selfloops=False)
    pos=nx.spring_layout(G) #this command makes a layout of position of all nodes (instead of spring_layout you can use fruchterman_reingold_layout or other layouts so you will have different figures for graph) ,since we want to have different color for different states of nodes so we have to first make a layout then in graph draw function we make node by different colores,in fact ( I seperated this command and also above command (G=nx.Graph()) from the function of graph draw for two reasons : 1- seperating pos command causes we have a fixed layout for all graph draw (for example if initial node is located in south west of picture of graph(in graph draw plot)then for any time we plot graph again (for example for different timesteps) then the initial infected node is still in south west of graph plot, so we can see spread of rumor and its expand from south west of graph during different timesteps  2- by seperating graph generator function (G = nx.Graph command) we save time because we perform this command only one time and for any times that we plot graph we would not use this command again, so plots will be made fastly
    adjacency = G.adjacency_list()
    return G,pos,adjacency

#----------------
class Network_Baseline_Model (object):
    def __init__ (self,BETA_SI1,BETA_SI2,BETA_I1I12,BETA_I1R1,BETA_I2I12,BETA_I2R2,BETA_I12R1,BETA_I12R2,adjacency):
        number = 0
        self.network_all_node = []
        self.timestep = 0
        self.number_of_nodes_in_S_state_per_timestep = []
        self.number_of_nodes_in_I1_state_per_timestep = []
        self.number_of_nodes_in_I2_state_per_timestep = []
        self.number_of_nodes_in_I12_state_per_timestep = []
        self.number_of_nodes_in_R1_state_per_timestep = []
        self.number_of_nodes_in_R2_state_per_timestep = []
        
        while number < 1000 :
            self.network_all_node.append (Node(number))
            number += 1
        for node in self.network_all_node :
            node.get_neighbor (self.network_all_node,adjacency)

##    def __str__(self):
##        S_number = 0
##        I1_number = 0
##        I2_number = 0
##
##        for node in self.network_all_node :
##            if node.state == "S" :
##                S_number += 1
##            if node.state == "I1" :
##                I1_number += 1
##            if node.state == "I2" :
##                I2_number += 1
##
##                
##        rep = "Timestep number : " + str(self.timestep) + "\n\n" + "number of S nodes : " + str(S_number) + "\n\n" + "number of I1 nodes : " + str(I1_number) + "\n\n" + "number of I2 nodes : " + str(I2_number) +  "\n\n" + "number of B1 nodes : " + str(B1_number) + "\n\n" + "number of B2 nodes : " + str(B2_number) + "\n ----------------------"
##        return rep

    def number_of_nodes_in_each_state_per_timestep (self) : 
        S_number = 0
        I1_number = 0
        I2_number = 0
        I12_number = 0
        R1_number = 0
        R2_number = 0
        
        for node in self.network_all_node :
            if node.state == "S" :
                S_number += 1
            if node.state == "I1" :
                I1_number += 1
            if node.state == "I2" :
                I2_number += 1
            if node.state == "I12" :
                I12_number += 1
            if node.state == "R1" :
                R1_number += 1
            if node.state == "R2" :
                R2_number += 1

        self.number_of_nodes_in_S_state_per_timestep.append(S_number)
        self.number_of_nodes_in_I1_state_per_timestep.append(I1_number)
        self.number_of_nodes_in_I2_state_per_timestep.append(I2_number)
        self.number_of_nodes_in_I12_state_per_timestep.append(I12_number)
        self.number_of_nodes_in_R1_state_per_timestep.append(R1_number)
        self.number_of_nodes_in_R2_state_per_timestep.append(R2_number)

    def initial_infection (self,g,f):
        self.network_all_node[g].state = "I1"
        self.network_all_node[f].state = "I2"
        




    
    def change (self,BETA_SI1,BETA_SI2,BETA_I1I12,BETA_I1R1,BETA_I2I12,BETA_I2R2,BETA_I12R1,BETA_I12R2,t) : #These parameters corrospond to their corrospondants in the origin model respectively as Beta1, Beta2, Beta2, Mu1, Beta1, Mu2, Mu1, Mu2
        import random
        
        for node in self.network_all_node :
            number_I1_state_neighbor = 0
            number_I2_state_neighbor = 0
            number_I12_state_neighbor = 0
            number_R1_state_neighbor = 0
            number_R2_state_neighbor = 0
            #----.-----.-----.-----.-----.----.-----.-----.-----.-----.----.-----.-----.-----.-----
            
            if node.state == "S" :
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1
                    if neighbor.state == "I12" :
                        number_I12_state_neighbor += 1
                        
##                #computing non_spontaneous_transition_probability
##                non_spontaneous_transition_probability = 1         
                if number_I1_state_neighbor + number_I2_state_neighbor + number_I12_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    #computing F_SI1 and F_SI2
                    a = (BETA_SI1*(number_I1_state_neighbor+number_I12_state_neighbor))/(1-0.5*BETA_SI1)
                    b = (BETA_SI2*(number_I2_state_neighbor+number_I12_state_neighbor))/(1-0.5*BETA_SI2)
                    c = 1-((1-BETA_SI1)**number_I1_state_neighbor)*((1-BETA_SI2)**number_I2_state_neighbor)
                    d = a + b #we used float to stop machine from rounding small numbers to zero and cause us to have division by zero
                    if d == 0 :
                        d = 1.0e-323 #since numbers less than this, will be set as 0 by python and this causes us to have division by zero, we set this small number for them                
                    F_SI1 = (a*c)/d
                    F_SI2 = (b*c)/d 
                    #computing G functions
                    G_SI1 = F_SI1
                    G_SI2 = F_SI2
                    #computing G_S0 ie: no success connected transition
                    G_S = 1 - c  #look at the c above
                    #   }}}

                else :
                    G_SI1 = 0
                    G_SI2 = 0
                    G_S  = 1
                
                #Total Transitions (mass function rule is achieved because :  P_S_TO_I1 + P_S_TO_B1 + P_S_TO_I2 + P_S_TO_B2 + P_Remain_S = 1   )
                P_S_TO_I1 = G_SI1
                P_S_TO_I2 = G_SI2
                P_Remain_S = G_S

                #change
                x = random.uniform(0,1)
                if x <= P_S_TO_I1 :
                    node.primary_state = "I1"   
                elif x <= (P_S_TO_I1 +  P_S_TO_I2)  :
                    node.primary_state = "I2"
                else :
                    node.primary_state = "S" #means  (P_S_TO_I1_C + P_S_TO_B1 + P_S_TO_I2 + P_S_TO_B2) < x <= 1    ie: P_Remain_S was succesful
                

            elif node.state == "I1" :                
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1
                    if neighbor.state == "I12" :
                        number_I12_state_neighbor += 1
                    if neighbor.state == "R1" :
                        number_R1_state_neighbor += 1
                        
##                #computing non_spontaneous_transition_probability
##                non_spontaneous_transition_probability = 1 - GAMMA_SI1 - GAMMA_SI2         
                if number_I1_state_neighbor + number_I2_state_neighbor + number_I12_state_neighbor + number_R1_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    #computing F_I1I12 and F_I1R1
                    a = (BETA_I1I12*(number_I2_state_neighbor+number_I12_state_neighbor))/(1-0.5*BETA_I1I12)
                    b = (BETA_I1R1*(number_I1_state_neighbor+number_R1_state_neighbor))/(1-0.5*BETA_I1R1)
                    c = 1-(BETA_I1I12*(number_I2_state_neighbor+number_I12_state_neighbor))*((1-BETA_I1R1)**(number_I1_state_neighbor+number_R1_state_neighbor))
                    d = a + b #we used float to stop machine from rounding small numbers to zero and cause us to have division by zero
                    if d == 0 :
                        d = 1.0e-323 #since numbers less than this, will be set as 0 by python and this causes us to have division by zero, we set this small number for them                
                    F_I1I12 = (a*c)/d
                    F_I1R1 = (b*c)/d 
                    #computing G functions
                    G_I1I12 = F_I1I12
                    G_I1R1 = F_I1R1
                    #computing G_S0 ie: no success connected transition
                    G_I1 = 1 - c  #look at the c above
                    #   }}}

                else :
                    G_I1I12 = 0
                    G_I1R1 = 0
                    G_I1  = 1
                
                #Total Transitions (mass function rule is achieved because :  P_S_TO_I1 + P_S_TO_B1 + P_S_TO_I2 + P_S_TO_B2 + P_Remain_S = 1   )
                P_I1_TO_I12 = G_I1I12
                P_I1_TO_R1 = G_I1R1
                P_Remain_I1 = G_I1

                #change
                x = random.uniform(0,1)
                if x <= P_I1_TO_I12 :
                    node.primary_state = "I12"   
                elif x <= (P_I1_TO_I12 +  P_I1_TO_R1)  :
                    node.primary_state = "R1"
                else :
                    node.primary_state = "I1" 
                
            elif node.state == "I2" :
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1
                    if neighbor.state == "I12" :
                        number_I12_state_neighbor += 1
                    if neighbor.state == "R2" :
                        number_R2_state_neighbor += 1
                        
##                #computing non_spontaneous_transition_probability
##                non_spontaneous_transition_probability = 1 - GAMMA_SI1 - GAMMA_SI2         
                if number_I1_state_neighbor + number_I2_state_neighbor + number_I12_state_neighbor + number_R2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    #computing F_I1I12 and F_I1R1
                    a = (BETA_I2I12*(number_I1_state_neighbor+number_I12_state_neighbor))/(1-0.5*BETA_I2I12)
                    b = (BETA_I2R2*(number_I2_state_neighbor+number_R2_state_neighbor))/(1-0.5*BETA_I2R2)
                    c = 1-(BETA_I2I12*(number_I1_state_neighbor+number_I12_state_neighbor))*((1-BETA_I2R2)**(number_I2_state_neighbor+number_R2_state_neighbor))
                    d = a + b #we used float to stop machine from rounding small numbers to zero and cause us to have division by zero
                    if d == 0 :
                        d = 1.0e-323 #since numbers less than this, will be set as 0 by python and this causes us to have division by zero, we set this small number for them                
                    F_I2I12 = (a*c)/d
                    F_I2R2 = (b*c)/d 
                    #computing G functions
                    G_I2I12 = F_I2I12
                    G_I2R2 = F_I2R2
                    #computing G_I2 ie: no success connected transition
                    G_I2 = 1 - c  #look at the c above
                    #   }}}

                else :
                    G_I2I12 = 0
                    G_I2R2 = 0
                    G_I2  = 1
                
                #Total Transitions 
                P_I2_TO_I12 = G_I2I12
                P_I2_TO_R2 = G_I2R2
                P_Remain_I2 = G_I2

                #change
                x = random.uniform(0,1)
                if x <= P_I2_TO_I12 :
                    node.primary_state = "I12"   
                elif x <= (P_I2_TO_I12 +  P_I2_TO_R2)  :
                    node.primary_state = "R2"
                else :
                    node.primary_state = "I2"    

            elif node.state == "I12" :                
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1
                    if neighbor.state == "R1" :
                        number_R1_state_neighbor += 1
                    if neighbor.state == "R2" :
                        number_R2_state_neighbor += 1
                        
##                #computing non_spontaneous_transition_probability
##                non_spontaneous_transition_probability = 1 - GAMMA_SI1 - GAMMA_SI2         
                if number_I1_state_neighbor + number_I2_state_neighbor + number_R1_state_neighbor + number_R2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    #computing F_I1I12 and F_I1R1
                    a = (BETA_I12R1*(number_I1_state_neighbor+number_R1_state_neighbor))/(1-0.5*BETA_I12R1)
                    b = (BETA_I12R2*(number_I2_state_neighbor+number_R2_state_neighbor))/(1-0.5*BETA_I12R2)
                    c = 1-(BETA_I12R1*(number_I1_state_neighbor+number_R1_state_neighbor))*((1-BETA_I12R2)**(number_I2_state_neighbor+number_R2_state_neighbor))
                    d = a + b #we used float to stop machine from rounding small numbers to zero and cause us to have division by zero
                    if d == 0 :
                        d = 1.0e-323 #since numbers less than this, will be set as 0 by python and this causes us to have division by zero, we set this small number for them                
                    F_I12R1 = (a*c)/d
                    F_I12R2 = (b*c)/d 
                    #computing G functions
                    G_I12R1 = F_I12R1
                    G_I12R2 = F_I12R2
                    #computing G_I2 ie: no success connected transition
                    G_I12 = 1 - c  #look at the c above
                    #   }}}

                else :
                    G_I12R1 = 0
                    G_I12R2 = 0
                    G_I12  = 1
                
                #Total Transitions 
                P_I12_TO_R1 = G_I12R1
                P_I12_TO_R2 = G_I12R2
                P_Remain_I12 = G_I12

                #change
                x = random.uniform(0,1)
                if x <= P_I12_TO_R1 :
                    node.primary_state = "R1"   
                elif x <= (P_I12_TO_R1 +  P_I12_TO_R2)  :
                    node.primary_state = "R2"
                else :
                    node.primary_state = "I12"
                
            else :
                None # means node was in I1 or I2 state and these nodes never participate in any change process fro themselves and forever will be in their state (even though this can be a subject for second paper in which these states will change to other states)
                    
        #----.-----.-----.-----.-----.----.-----.-----.-----.-----.----.-----.-----.-----.-----


        for node in self.network_all_node :
            if node.state == "S" and node.primary_state == "I1" :
                node.STOI1(t)
                
            elif node.state == "S" and node.primary_state == "I2" :
                node.STOI2(t)

            elif node.state == "I1" and node.primary_state == "I12" :
                node.I1TOI12(t)

            elif node.state == "I1" and node.primary_state == "R1" :
                node.I1TOR1(t)

            elif node.state == "I2" and node.primary_state == "I12" :
                node.I2TOI12(t)

            elif node.state == "I2" and node.primary_state == "R2" :
                node.I2TOR2(t)

            elif node.state == "I12" and node.primary_state == "R1" :
                node.I12TOR1(t)

            elif node.state == "I12" and node.primary_state == "R2" :
                node.I12TOR2(t)

                
            else :
                None

    def time (self,t):
        self.timestep = t

#----------------
def error_computing (w,z,dataset_number) : #w is endorsers of simulation , z is deniers of simulation at the end of each 24 steps (equal to one day in real data set)
##    dataset_number = int (input("\n Which dataset you want to compare results to ?  <1> : ObamaDataset , <2> : PalinDataset (please enter the number of dataset)"))
  #  we want to just study influence of transmission parameters so we do not include other factors 
    if dataset_number == 1 : #Obamadataset is chosen
        x = [133, 275, 320, 374, 403, 436, 470, 503, 568, 641, 690, 708] #from obama dataset , the total number of endorsers at the end of each day (24 hours in dataset)
        y = [85, 183, 260, 286, 298, 308, 330, 352, 378, 388, 404, 408] #from obama dataset , the total number of deniers at the end of each day (24 hours in dataset)
        number_of_timesteps_in_dataset = 303
    elif dataset_number == 2 : #Palindataset is chosen
        x = [18, 100, 407, 987, 1069, 1133, 1158, 1179, 1221,1293, 1439] #from palin dataset , the total number of endorsers at the end of each day (24 hours in dataset) except for the first day that we put data of each 4 hours , because most of endorsers in the pailn dataset are made in the first day , so we have to spilit the first day to have resonable results
        y = [0, 2, 101, 804, 936, 999, 1047, 1075, 1126, 1527, 1634] #from palin dataset , the total number of deniers at the end of each day (24 hours in dataset) except for the first day that we put data of each 4 hours , because most of deniers in the pailn dataset are made in the first day , so we have to spilit the first day to have resonable results
        number_of_timesteps_in_dataset = 212
        
    cc = 1
    xx= len(w)
    zz= len(x)*24

    endorser_total_number_at_the_end_of_each_twentyfour_timesteps = []
    denier_total_number_at_the_end_of_each_twentyfour_timesteps = []
    while cc < xx + 1 and cc < zz + 1 : # because we want to have : length of k = length of x = length of y = length of p
        if cc % 24 == 0 :
            endorser_total_number_at_the_end_of_each_twentyfour_timesteps.append (w[cc])
            denier_total_number_at_the_end_of_each_twentyfour_timesteps.append (z[cc])
        cc += 1
    k = endorser_total_number_at_the_end_of_each_twentyfour_timesteps #the number of endorsers at the end of each 24 steps (equal to one day in real data set)
    p = denier_total_number_at_the_end_of_each_twentyfour_timesteps #the number of deniers at the end of each 24 steps (equal to one day in real data set)
    n = len (x)
    i = 0
    d_endorser = 0
    d_denier = 0
    d_endorser_add = 0
    d_denier_add = 0
    while i < n :
        d_endorser = x[i] - k[i]
        d_denier = y[i] - p[i]
        d_endorser_add += d_endorser**2
        d_denier_add += d_denier**2
        i+=1
    d_endorser_total = d_endorser_add**0.5
    d_denier_total = d_denier_add**0.5
    d_total = d_endorser_total + d_denier_total
##    if dataset_number == 1 : #Obamadataset is chosen
    return d_total
##    elif dataset_number == 2 : #Palindataset is chosen
##        print ("\n Total Error with Palindataset is  : ",d_total)
#------------------------
def infection (down_limit,up_limit):
	import random
	z = None
	x = None
	x = random.uniform(down_limit,up_limit)
	return x
#------------------
        
def plot_results (number_of_nodes_in_I1_state_per_timestep_for_all_experiments,number_of_nodes_in_I2_state_per_timestep_for_all_experiments,number_of_nodes_in_S_state_per_timestep_for_all_experiments) : 
    import matplotlib.pyplot as plt
    import os #for giving adress to where we want to save output files
    import numpy as np
    i = 0
    j = 0
    
    n_ts = len (number_of_nodes_in_I1_state_per_timestep_for_all_experiments[0]) #number of time steps
    n_ex = len (number_of_nodes_in_I1_state_per_timestep_for_all_experiments) #number of experiments
    number_of_nodes_in_I1_in_a_single_time_step_for_all_experiments_for_all_time_steps = []
    number_of_nodes_in_I2_in_a_single_time_step_for_all_experiments_for_all_time_steps = []
    number_of_nodes_in_S_in_a_single_time_step_for_all_experiments_for_all_time_steps = []
    I1_mean = []
    I2_mean = []
    S_mean = []
    
    while i < n_ts:
        number_of_nodes_in_I1_in_a_single_time_step_for_all_experiments = []
        number_of_nodes_in_I2_in_a_single_time_step_for_all_experiments = []
        number_of_nodes_in_S_in_a_single_time_step_for_all_experiments = []
        j = 0
        while j < n_ex :
            number_of_nodes_in_I1_in_a_single_time_step_for_all_experiments.append (number_of_nodes_in_I1_state_per_timestep_for_all_experiments [j][i])
            number_of_nodes_in_I2_in_a_single_time_step_for_all_experiments.append (number_of_nodes_in_I2_state_per_timestep_for_all_experiments [j][i])
            number_of_nodes_in_S_in_a_single_time_step_for_all_experiments.append (number_of_nodes_in_S_state_per_timestep_for_all_experiments [j][i])
            j += 1
        number_of_nodes_in_I1_in_a_single_time_step_for_all_experiments_for_all_time_steps.append (number_of_nodes_in_I1_in_a_single_time_step_for_all_experiments)
        number_of_nodes_in_I2_in_a_single_time_step_for_all_experiments_for_all_time_steps.append (number_of_nodes_in_I2_in_a_single_time_step_for_all_experiments)
        number_of_nodes_in_S_in_a_single_time_step_for_all_experiments_for_all_time_steps.append (number_of_nodes_in_S_in_a_single_time_step_for_all_experiments)
        i+=1

    # please note that :
    # number_of_nodes_in_I1_in_a_single_time_step_for_all_experiments_for_all_time_steps is a list of lists like this :
    # [[x1,x2,...,x1000],[y1,y2,...,y1000],...,[z1,z2,...,z1000]]
    # that x1,x2,...x1000 are the number of rumor spreaders at the first time step for all the 1000 experiments
    # and y1,y2,...y1000 are the number of rumor spreaders at the second time step for all the 1000 experiments
    # and z1,z2,...z1000 are the number of rumor spreaders at the last time (for example 303th time step for obama) in all the 1000 experiments
    # the above explanations is same for all I2 and S list of lists
    # now we get the avarage value of 1000 experiments in each time step for each one of I1 , I2 , S
    k = 0
    while k < n_ts :
        I1_mean.append(np.mean (number_of_nodes_in_I1_in_a_single_time_step_for_all_experiments_for_all_time_steps [k]))
        I2_mean.append(np.mean (number_of_nodes_in_I2_in_a_single_time_step_for_all_experiments_for_all_time_steps [k]))
        S_mean.append(np.mean (number_of_nodes_in_S_in_a_single_time_step_for_all_experiments_for_all_time_steps [k]))
        k += 1
    
    h = 1
    z = n_ts
    f = []
    while h < z + 1: #making the horizental line of plot as the number of timesteps
        f.append(h)
        h+=1
    file_name = "The number of spreaders in each state per timestep"
    ax = plt.axes ()
    ax.axes.get_xaxis().set_visible(True)
    ax.axes.get_yaxis().set_visible(True)
    plt.plot(f,I1_mean,'r' , label = 'Rumor Spreaders')
    plt.plot(f,I2_mean,'b' , label = 'Anti-Rumor Spreaders')
    plt.plot(f,S_mean,'g'  , label = 'Susceptibles')  
    plt.xlabel('Timestep')
    plt.ylabel('Number of Nodes in States')
    plt.grid(True)
    plt.legend ()
    path_of_saving = str ("D:\\Papers\\Paper_3") #here we make the address of the folder we want pictures to be saved, BUT YOU HAVE TO douplicate each Backslash in the URL address (as you see I did ) , if you dont it wont work and give you error of UNICODESCAPE !
    plt.savefig(os.path.join(path_of_saving, file_name),dpi=600)
    plt.show () #since we save pics then there is no need to show them by processing the program, but if we delete this command (or comment out it) the text on plots get messed up! so let them be showed during the process
#-------------
def param_new_model (down_limit,up_limit):

    GAMMA_SB1 = infection (down_limit,up_limit)
    GAMMA_SI1 = infection (down_limit,up_limit)
    GAMMA_SB2 = infection (down_limit,up_limit)
    GAMMA_SI2 = infection (down_limit,up_limit)
    GAMMA_B1S = infection (down_limit,up_limit)
    GAMMA_B2S = infection (down_limit,up_limit)
    GAMMA_B1I1 = infection (down_limit,up_limit)
    GAMMA_B2I2 = infection (down_limit,up_limit)
    BETA_SI1 = infection (down_limit,up_limit)
    BETA_SI2 = infection (down_limit,up_limit)
    BETA_B1I1 = infection (down_limit,up_limit)
    BETA_B1I2 = infection (down_limit,up_limit)
    BETA_B2I2 = infection (down_limit,up_limit)
    BETA_B2I1 = infection (down_limit,up_limit)
    T_SI1I1 = infection (0,1)
    T_SI2I2 = infection (0,1)
    return BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2

#------------
def param_baseline (down_limit,up_limit): #here there is no diference between new_model params and baseline_model params
    BETA_SI1 = infection (down_limit,up_limit)
    BETA_SI2 = infection (down_limit,up_limit)
    BETA_I1I12 = BETA_SI2
    BETA_I1R1 = infection (down_limit,up_limit)
    BETA_I2I12 = BETA_SI1
    BETA_I2R2 = infection (down_limit,up_limit)
    BETA_I12R1 = BETA_I1R1
    BETA_I12R2 = BETA_I2R2
    return BETA_SI1,BETA_SI2,BETA_I1I12,BETA_I1R1,BETA_I2I12,BETA_I2R2,BETA_I12R1,BETA_I12R2
#--------------
def initial_infection ():
        import random
        x = random.randint(0,999)
        y = random.randint(0,999)
        while y==x :
            y = random.randint(0,999)
        return x , y
#---------------
def main():
    dataset_number = int(input("Please enter the number of dataset you want to compare with  <1>ObamaDataset , <2>PalinDataset : "))
    number_expriment = int(input("Please enter the total number of expriments : "))
    down_limit = float(input("Please enter the down limit for the variebles :(0,1) "))
    up_limit = float(input("Please enter the up limit for the variebles :(0,1) "))    
    j=0
    v=0
    G,pos,adjecency = graph_generator()
    error_list_new_model = []
    param_list_new_model = []
    error_list_baseline = []
    param_list_baseline = []
    sum_error_new_model = 0
    sum_error_baseline = 0
    number_of_nodes_in_I1_state_per_timestep_for_all_experiments = []
    number_of_nodes_in_I2_state_per_timestep_for_all_experiments = []
    number_of_nodes_in_S_state_per_timestep_for_all_experiments = []
    

    if dataset_number == 1 :
        number_timestep = 289 #because more than 288 (12*24) timesteps we do not need in our simulation, since in obama dataset we have 12 day and in our simulation we takes 24 steps as a day
    elif dataset_number == 2 :
        number_timestep = 313 #because more than 312 (13*24) timesteps we do not need in our simulation, since in palin dataset we have 13 day and in our simulation we takes 24 steps as a day
        
        
    
    while j < number_expriment :
        g,f = initial_infection () #to make same initial infected nodes for both new_model and baseline model 
        BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2 = param_new_model (down_limit,up_limit)
        NNM = Network_New_Model(BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2,adjecency)
        NNM.initial_infection (g,f) # this function makes an initial infected node NOT randomly! but we choose TWO certain nodes as infected to I1 & as infected to I2 because we want to just study influence of transmission parameters so we do not include other factors 
        t = 0
        NNM.number_of_nodes_in_I1_state_per_timestep = []
        NNM.number_of_nodes_in_I2_state_per_timestep = []
        NNM.number_of_nodes_in_S_state_per_timestep = []
        NNM.number_of_nodes_in_each_state_per_timestep ()
        while t < number_timestep + 1 :
            NNM.change(BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2, t)
            NNM.time (t)
            NNM.number_of_nodes_in_each_state_per_timestep ()
            t+=1
        error_new_model = error_computing (NNM.number_of_nodes_in_I1_state_per_timestep,NNM.number_of_nodes_in_I2_state_per_timestep,dataset_number)
        error_list_new_model.append(error_new_model)
        param_set_new_model = [BETA_SI1,BETA_SI2,GAMMA_SI1,GAMMA_SI2]
        param_list_new_model.append(param_set_new_model)

        number_of_nodes_in_I1_state_per_timestep_for_all_experiments.append (NNM.number_of_nodes_in_I1_state_per_timestep)
        number_of_nodes_in_I2_state_per_timestep_for_all_experiments.append (NNM.number_of_nodes_in_I2_state_per_timestep)
        number_of_nodes_in_S_state_per_timestep_for_all_experiments.append (NNM.number_of_nodes_in_S_state_per_timestep)
       
        
        BETA_SI1,BETA_SI2,BETA_I1I12,BETA_I1R1,BETA_I2I12,BETA_I2R2,BETA_I12R1,BETA_I12R2 = param_baseline (down_limit,up_limit)
        NBM = Network_Baseline_Model(BETA_SI1,BETA_SI2,BETA_I1I12,BETA_I1R1,BETA_I2I12,BETA_I2R2,BETA_I12R1,BETA_I12R2,adjecency)
        NBM.initial_infection (g,f) # this function makes an initial infected node NOT randomly! but we choose TWO certain nodes as infected to I1 & as infected to I2 because we want to just study influence of transmission parameters so we do not include other factors 
        t = 0
        NBM.number_of_nodes_in_I1_state_per_timestep = []
        NBM.number_of_nodes_in_I2_state_per_timestep = []
        NBM.number_of_nodes_in_each_state_per_timestep ()
        while t < number_timestep + 1 :
            NBM.change(BETA_SI1,BETA_SI2,BETA_I1I12,BETA_I1R1,BETA_I2I12,BETA_I2R2,BETA_I12R1,BETA_I12R2,t)
            NBM.time (t)
            NBM.number_of_nodes_in_each_state_per_timestep ()
            t+=1
        error_baseline = error_computing (NBM.number_of_nodes_in_I1_state_per_timestep,NBM.number_of_nodes_in_I2_state_per_timestep,dataset_number)
        error_list_baseline.append(error_baseline)
        param_set_baseline=[BETA_SI1,BETA_SI2,GAMMA_SI1,GAMMA_SI2]
        param_list_baseline.append(param_set_baseline)
        

        j+=1

    
    for error in error_list_new_model :
        sum_error_new_model += error
    mean_error_new_model = sum_error_new_model/number_expriment
    for error in error_list_baseline :
        sum_error_baseline += error
    mean_error_baseline = sum_error_baseline/number_expriment

    
    min_index_new_model = error_list_new_model.index(min(error_list_new_model))
    min_error_new_model = error_list_new_model[min_index_new_model]
    best_param_new_model = param_list_new_model[min_index_new_model]
    min_index_baseline = error_list_baseline.index(min(error_list_baseline))
    min_error_baseline = error_list_baseline[min_index_baseline]
    best_param_baseline = param_list_baseline[min_index_baseline]

    
    print("-----------------------------------------\n")
    print("min_index_new_model : ",min_index_new_model)
    print("min_error_new_model : ",min_error_new_model)
    print("mean_error_new_model : ",mean_error_new_model)
    print("best_param_new_model : ",best_param_new_model)
    print("------------------------------------------")
    print("min_index_baseline : ",min_index_baseline)
    print("min_error_baseline : ",min_error_baseline)
    print("mean_error_baseline : ",mean_error_baseline)
    print("best_param_baseline : ",best_param_baseline)
    print("------------------------------------------")
    print("------------------------------------------")


    plot_results (number_of_nodes_in_I1_state_per_timestep_for_all_experiments,number_of_nodes_in_I2_state_per_timestep_for_all_experiments,number_of_nodes_in_S_state_per_timestep_for_all_experiments) #to plot results (number of nodes in each state per timestep 
    
    print ("It's Done. \n")
#------------------
main()
input ("press enter to exit.")
