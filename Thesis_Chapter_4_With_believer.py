class Node (object) :
    def __init__ (self,number):
        self.number = number
        self.state = "S"
        self.primary_state = None

    def get_neighbor (self,all_node,adjacency):
        self.neighbor = []
        for number in adjacency[self.number] :
            self.neighbor.append(all_node[number])


    def STOI1 (self):
        self.state = "I1"

    def STOI2 (self):
        self.state = "I2"        

    def STOB1 (self):
        self.state = "B1"

    def STOB2 (self):
        self.state = "B2"

    def B1TOI1 (self):
        self.state = "I1"

    def B1TOS (self):
        self.state = "S"

    def B2TOI2 (self):
        self.state = "I2"

    def B2TOS (self):
        self.state = "S"


        

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
##        self.number_of_nodes_in_S_state_per_timestep.append(S_number)
        self.number_of_nodes_in_I1_state_per_timestep.append(I1_number)
        self.number_of_nodes_in_I2_state_per_timestep.append(I2_number)
##        self.number_of_nodes_in_B1_state_per_timestep.append(B1_number)
##        self.number_of_nodes_in_B2_state_per_timestep.append(B2_number)

    def initial_infection (self,g,f):
        self.network_all_node[g].state = "I1"
        self.network_all_node[f].state = "I2"
        




    
    def change (self,BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2) :
        import random
        
        for node in self.network_all_node :
            number_I1_state_neighbor = 0
            number_I2_state_neighbor = 0

            #----.-----.-----.-----.-----.----.-----.-----.-----.-----.----.-----.-----.-----.-----
            
            if node.state == "S" :
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1
                        
                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_SI1 - GAMMA_SB1 - GAMMA_SI2 - GAMMA_SB2        
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    # Computing  T_SI1B1 and T_SI2B2 
                    T_SI1B1 = 1 - T_SI1I1
                    T_SI2B2 = 1 - T_SI2I2
                    #computing F_SI1 and F_SI2
                    a = (BETA_SI1*number_I1_state_neighbor)/(1-0.5*BETA_SI1)
                    b = (BETA_SI2*number_I2_state_neighbor)/(1-0.5*BETA_SI2)
                    c = 1-((1-BETA_SI1)**number_I1_state_neighbor)*((1-BETA_SI2)**number_I2_state_neighbor)
                    d = a + b
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
                
                #Total Transitions (mass function rule is achieved because :  P_S_TO_I1 + P_S_TO_B1 + P_S_TO_I2 + P_S_TO_B2 + P_Remain_S = 1   )
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
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1


                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_B1I1 - GAMMA_B1S 
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                         
                    #computing F_B1I1 and F_B1I2
                    a = (BETA_B1I1*number_I1_state_neighbor)/(1-0.5*BETA_B1I1)
                    b = (BETA_B1I2*number_I2_state_neighbor)/(1-0.5*BETA_B1I2)
                    c = 1-((1-BETA_B1I1)**number_I1_state_neighbor)*((1-BETA_B1I2)**number_I2_state_neighbor)
                    d = a + b
                    F_B1I1 = (a*c)/d
                    F_B1I2 = (b*c)/d
                    #computing G functions
                    G_B1I1 = F_B1I1 + F_B1I2
                    #computing G_S0 ie: no success connected transition
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
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1

                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_B2I2 - GAMMA_B2S
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    #computing F_B2I1 and F_B2I2
                    a = (BETA_B2I1*number_I1_state_neighbor)/(1-0.5*BETA_B2I1)
                    b = (BETA_B2I2*number_I2_state_neighbor)/(1-0.5*BETA_B2I2)
                    c = 1-((1-BETA_B2I1)**number_I1_state_neighbor)*((1-BETA_B2I2)**number_I2_state_neighbor)
                    d = a + b
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


        for node in self.network_all_node :
            if node.state == "S" and node.primary_state == "I1" :
                node.STOI1()
                
            elif node.state == "S" and node.primary_state == "I2" :
                node.STOI2()

            elif node.state == "S" and node.primary_state == "B1" :
                node.STOB1()

            elif node.state == "S" and node.primary_state == "B2" :
                node.STOB2()

            elif node.state == "B1" and node.primary_state == "I1" :
                node.B1TOI1()

            elif node.state == "B2" and node.primary_state == "I2" :
                node.B2TOI2()

            elif node.state == "B1" and node.primary_state == "S" :
                node.B1TOS()

            elif node.state == "B2" and node.primary_state == "S" :
                node.B2TOS()
                
            else :
                None

    def time (self,t):
        self.timestep = t

#----------------
class Network_Baseline_Model (object):
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
##        self.number_of_nodes_in_S_state_per_timestep.append(S_number)
        self.number_of_nodes_in_I1_state_per_timestep.append(I1_number)
        self.number_of_nodes_in_I2_state_per_timestep.append(I2_number)
##        self.number_of_nodes_in_B1_state_per_timestep.append(B1_number)
##        self.number_of_nodes_in_B2_state_per_timestep.append(B2_number)

    def initial_infection (self,g,f):
        self.network_all_node[g].state = "I1"
        self.network_all_node[f].state = "I2"
        




    
    def change (self,BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2) :
        import random
        
        for node in self.network_all_node :
            number_I1_state_neighbor = 0
            number_I2_state_neighbor = 0

            #----.-----.-----.-----.-----.----.-----.-----.-----.-----.----.-----.-----.-----.-----
            
            if node.state == "S" :
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1
                        
                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_SI1 - GAMMA_SB1 - GAMMA_SI2 - GAMMA_SB2        
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    # Computing  T_SI1B1 and T_SI2B2 
                    T_SI1B1 = 1 - T_SI1I1
                    T_SI2B2 = 1 - T_SI2I2
                    #computing F_SI1 and F_SI2
                    a = (BETA_SI1*number_I1_state_neighbor)/(1-0.5*BETA_SI1)
                    b = (BETA_SI2*number_I2_state_neighbor)/(1-0.5*BETA_SI2)
                    c = 1-((1-BETA_SI1)**number_I1_state_neighbor)*((1-BETA_SI2)**number_I2_state_neighbor)
                    d = a + b
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
                
                #Total Transitions (mass function rule is achieved because :  P_S_TO_I1 + P_S_TO_B1 + P_S_TO_I2 + P_S_TO_B2 + P_Remain_S = 1   )
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
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1


                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_B1I1 - GAMMA_B1S 
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                         
                    #computing F_B1I1 and F_B1I2
                    a = (BETA_B1I1*number_I1_state_neighbor)/(1-0.5*BETA_B1I1)
                    b = (BETA_B1I2*number_I2_state_neighbor)/(1-0.5*BETA_B1I2)
                    c = 1-((1-BETA_B1I1)**number_I1_state_neighbor)*((1-BETA_B1I2)**number_I2_state_neighbor)
                    d = a + b
##                    F_B1I1 = (a*c)/d ############### these two lines replace by the following lines
##                    F_B1I2 = (b*c)/d ###############

                    if d != 0 : ############### specificaly for this program (because by setting B1I2 = 0 in this program , it might that d=0 happens)
                        F_B1I1 = (a*c)/d
                        F_B1I2 = (b*c)/d
                    else :
                        F_B1I1 = 0
                        F_B1I2 = 0
                            
                    #computing G functions
                    G_B1I1 = F_B1I1 + F_B1I2
                    #computing G_S0 ie: no success connected transition
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
                for neighbor in node.neighbor :
                    if neighbor.state == "I1" :
                        number_I1_state_neighbor += 1
                    if neighbor.state == "I2" :
                        number_I2_state_neighbor += 1

                #computing non_simultaneous_transition_probability
                non_simultaneous_transition_probability = 1 - GAMMA_B2I2 - GAMMA_B2S
                if number_I1_state_neighbor + number_I2_state_neighbor != 0: #means at least there is one neighbour who is in I1 or I2 state
                    # Computing of required parameters : {{{                        
                    #computing F_B2I1 and F_B2I2
                    a = (BETA_B2I1*number_I1_state_neighbor)/(1-0.5*BETA_B2I1)
                    b = (BETA_B2I2*number_I2_state_neighbor)/(1-0.5*BETA_B2I2)
                    c = 1-((1-BETA_B2I1)**number_I1_state_neighbor)*((1-BETA_B2I2)**number_I2_state_neighbor)
                    d = a + b
##                    F_B2I1 = (a*c)/d ############### these two lines replace by the following lines
##                    F_B2I2 = (b*c)/d ###############
                    
                    if d != 0 : ############### specificaly for this program (because by setting B2I1 = 0 in this program , it might that d=0 happens)
                        F_B2I1 = (a*c)/d
                        F_B2I2 = (b*c)/d
                    else :
                        F_B2I1 = 0
                        F_B2I2 = 0
                            
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


        for node in self.network_all_node :
            if node.state == "S" and node.primary_state == "I1" :
                node.STOI1()
                
            elif node.state == "S" and node.primary_state == "I2" :
                node.STOI2()

            elif node.state == "S" and node.primary_state == "B1" :
                node.STOB1()

            elif node.state == "S" and node.primary_state == "B2" :
                node.STOB2()

            elif node.state == "B1" and node.primary_state == "I1" :
                node.B1TOI1()

            elif node.state == "B2" and node.primary_state == "I2" :
                node.B2TOI2()

            elif node.state == "B1" and node.primary_state == "S" :
                node.B1TOS()

            elif node.state == "B2" and node.primary_state == "S" :
                node.B2TOS()
                
            else :
                None

    def time (self,t):
        self.timestep = t
#----------------
        
def graph_generator ():
    import networkx as nx
    s = nx.utils.powerlaw_sequence(1000, 2.5)
    G = nx.expected_degree_graph(s, selfloops=False)
    pos = nx.spring_layout(G) #this command makes a layout of position of all nodes (instead of spring_layout you can use fruchterman_reingold_layout or other layouts so you will have different figures for graph) ,since we want to have different color for different states of nodes so we have to first make a layout then in graph draw function we make node by different colores,in fact ( I seperated this command and also above command (G=nx.Graph()) from the function of graph draw for two reasons : 1- seperating pos command causes we have a fixed layout for all graph draw (for example if initial node is located in south west of picture of graph(in graph draw plot)then for any time we plot graph again (for example for different timesteps) then the initial infected node is still in south west of graph plot, so we can see spread of rumor and its expand from south west of graph during different timesteps  2- by seperating graph generator function (G = nx.Graph command) we save time because we perform this command only one time and for any times that we plot graph we would not use this command again, so plots will be made fastly
    adjacency = G.adjacency_list()
    return G,pos,adjacency

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
def param_baseline (down_limit,up_limit):
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
    BETA_B1I2 = 0 ############### specificaly for this program    - this caused that your model (for thesis) turns to a normal model
    BETA_B2I2 = infection (down_limit,up_limit)
    BETA_B2I1 = 0 ############### specificaly for this program    - this caused that your model (for thesis) turns to a normal model
    T_SI1I1 = infection (0,1)
    T_SI2I2 = infection (0,1)
    return BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2
#--------------
def initial_infection ():
        import random
        x = random.randint(0,999)
        y = random.randint(0,999)
        while y==x :
            y = random.randint(0,999)
        return x , y

#---------------
def mean_best_params_new_model (error_list_new_model,param_list_new_model,number_expriment):
    i = 0
    j = 0
    n = number_expriment//50 # we use top 5% best min error to find mean of best parameters for : BETA_B1I1 , BETA_B1I2 , BETA_B2I2 , BETA_B2I1 , T_SI1I1 , T_SI2I2 
    min_error_new_model_list = []
    mean_best_params_new_model_list = []
    sum_BETA_B1I1 = 0
    sum_BETA_B1I2 = 0
    sum_BETA_B2I2 = 0
    sum_BETA_B2I1 = 0
    sum_T_SI1I1   = 0
    sum_T_SI2I2   = 0
    while i < n :
        min_index_new_model = error_list_new_model.index(min(error_list_new_model))
        min_error_new_model = error_list_new_model[min_index_new_model]
        min_error_new_model_list.append(min_error_new_model)
        mean_best_params_new_model_list.append(param_list_new_model[min_index_new_model])
        error_list_new_model.remove(min_error_new_model)
        i+=1

    for param_set in mean_best_params_new_model_list :
        sum_BETA_B1I1 += param_set[2]
        sum_BETA_B1I2 += param_set[3]
        sum_BETA_B2I2 += param_set[4]
        sum_BETA_B2I1 += param_set[5]
        sum_T_SI1I1   += param_set[14]
        sum_T_SI2I2   += param_set[15]

        
    mean_BETA_B1I1 = sum_BETA_B1I1 / n
    mean_BETA_B1I2 = sum_BETA_B1I2 / n
    mean_BETA_B2I2 = sum_BETA_B2I2 / n
    mean_BETA_B2I1 = sum_BETA_B2I1 / n
    mean_T_SI1I1   = sum_T_SI1I1 / n
    mean_T_SI2I2   = sum_T_SI2I2 / n
    print("mean_BETA_B1I1 : ",mean_BETA_B1I1)
    print("mean_BETA_B1I2 : ",mean_BETA_B1I2)
    print("mean_BETA_B2I2 : ",mean_BETA_B2I2)
    print("mean_BETA_B2I1 : ",mean_BETA_B2I1)
    print("mean_T_SI1I1 : ",mean_T_SI1I1)
    print("mean_T_SI2I2 : ",mean_T_SI2I2)
    
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
        NNM.number_of_nodes_in_each_state_per_timestep ()
        while t < number_timestep + 1 :
            NNM.change(BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2)
            NNM.time (t)
            NNM.number_of_nodes_in_each_state_per_timestep ()
            t+=1
        error_new_model = error_computing (NNM.number_of_nodes_in_I1_state_per_timestep,NNM.number_of_nodes_in_I2_state_per_timestep,dataset_number)
        error_list_new_model.append(error_new_model)
        param_set_new_model = [BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2]
        param_list_new_model.append(param_set_new_model)


        
        BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2 = param_baseline (down_limit,up_limit)
        NBM = Network_Baseline_Model(BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2,adjecency)
        NBM.initial_infection (g,f) # this function makes an initial infected node NOT randomly! but we choose TWO certain nodes as infected to I1 & as infected to I2 because we want to just study influence of transmission parameters so we do not include other factors 
        t = 0
        NBM.number_of_nodes_in_I1_state_per_timestep = []
        NBM.number_of_nodes_in_I2_state_per_timestep = []
        NBM.number_of_nodes_in_each_state_per_timestep ()
        while t < number_timestep + 1 :
            NBM.change(BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2)
            NBM.time (t)
            NBM.number_of_nodes_in_each_state_per_timestep ()
            t+=1
        error_baseline = error_computing (NBM.number_of_nodes_in_I1_state_per_timestep,NBM.number_of_nodes_in_I2_state_per_timestep,dataset_number)
        error_list_baseline.append(error_baseline)
        param_set_baseline=[BETA_SI1,BETA_SI2,BETA_B1I1,BETA_B1I2,BETA_B2I2,BETA_B2I1,GAMMA_B1I1,GAMMA_B2I2,GAMMA_SB1,GAMMA_SI1,GAMMA_SB2,GAMMA_SI2,GAMMA_B1S,GAMMA_B2S,T_SI1I1,T_SI2I2]
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
    mean_best_params_new_model (error_list_new_model,param_list_new_model,number_expriment)

##    plot_results (final_result_I1_Monte_carlo,final_result_I2_Monte_carlo,final_result_B1_Monte_carlo,final_result_B2_Monte_carlo,final_result_S_Monte_carlo,number_timestep) #to plot results (number of nodes in each state per timestep 
    
    print ("It's Done. \n")
#------------------
main()
input ("press enter to exit.")
        
    
            
