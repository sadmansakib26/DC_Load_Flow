import numpy as np
import math

def bus_matrix(n_bus, connections, line_impedance):

    # Function to calculate the reciprocal
    x = lambda a: 1 / a if a != 0 else 0

    ordered_connections = [''.join(sorted(i)) for i in connections]
    line_data = dict(zip(ordered_connections, line_impedance))

    # Calculating Equivalent line impedances
    duplicates = {}
    for i, key in enumerate(ordered_connections):
        if key in duplicates:
            duplicates[key].append(i)
        else:
            duplicates[key] = [i]

    line_data = {key: x(sum(x(line_impedance[i]) for i in indexes)) for key, indexes in duplicates.items()}

    line_data = {key: 1 / value for key, value in line_data.items()} #convert impedance values to admittance values
    
    for key, value in list(line_data.items()):
        
        reversed_substring = ''.join(reversed(key))
        
        # Update the original dictionary
        line_data[key] = line_data[reversed_substring] = value # this creates y_12 = y_21; y_13 = y_31 and so on
        


    Y = np.zeros((n_bus, n_bus)) #size of Y_Bus matrix
    
    for i in range(n_bus):
        for j in range(n_bus):
            if i != j:
                Y[i, j] = line_data.get(f'{i+1}{j+1}') #Filling the non-diagonal values
                
    np.fill_diagonal(Y, -Y.sum(0)) #Filling the diagonal values

    return Y*1j #Y_bus is complex

def get_theta(Y_bus, P_g, P_d, Base_MVA = 100):
    
    B_prime = 1j*Y_bus[1:, 1:] #removing the first row and column of B matrix 
    Theta = (np.linalg.inv(B_prime) @ (np.array(P_g[1:]) - np.array(P_d[1:])))/Base_MVA 

    return Theta

def get_line_power(n_bus, Theta, connections, line_impedance, Base_MVA=100):
    
    line_admittance = [1/x for x in line_impedance] #converting impedance to admittance
    b = np.diag(line_admittance, 0) 
    #connections = ['12', '12', '13', '23']
    
    #Calculating Matrix A

    node_from = [int(connection[0]) for connection in connections]
    node_to = [int(connection[1]) for connection in connections]
    A = np.zeros((len(connections), n_bus))
    for i, (start, end) in enumerate(zip(node_from, node_to)):
        A[i, start-1] = 1
        A[i, end-1] = -1

    #Calculating P_line & P_slack
    P_line = Base_MVA * (b @ A @ (np.insert(Theta, 0, 0)))

    pos_idx_slack = [idx for idx, connection in enumerate(connections) if '1' in connection[0]]
    neg_idx_slack = [idx for idx, connection in enumerate(connections) if '1' in connection[1]]
    P_slack = np.sum(P_line[pos_idx_slack]) - np.sum(P_line[neg_idx_slack]) 

    return P_line, P_slack

def dc_line_flow(n_bus, P_g, P_d, connections, line_impedance, Base_MVA = 100):
    
    """
    n_bus = number of bus
    P_g = list of generator real powers, give P_g1 = 0
    P_d = list of generator demands
    connections = list of strings to show how the buses are connected (first element = starting bus, second_element = ending bus)
    line_impedance = list of line impedances in p.u. 
    

    if line impedance is  infinite, give np.inf as input

    Example of input:

    n_bus = 3 ; 3 bus system
    P_g = [0, 630, 0] ; P_g2 = 63 MW, P_g3 = 0 MW
    P_d = [0, 100, 90] ; P_d1 = 0 MW, P_g2 = 63 MW, P_g3 = 0 MW
    connections = ['12', '23', '13']
    line_impedance = [0.0576, 0.092, 0.17]
    Base_MVA = 100 ; base apparant power

    dc_line_flow(n_bus, P_g, P_d, connections, line_impedance, Base_MVA = 100)

    """
    
    Y_bus = bus_matrix(n_bus, connections, line_impedance)
    print(f'\nThe Y_bus matrix is:\n{"-"*100}\n{Y_bus}\n{"-"*100}\n')
    Theta = get_theta(Y_bus, P_g, P_d, Base_MVA)
    print(f'The Theta matrix is:\n{"-"*100}\n{Theta}\n{"-"*100}\n')
    P_line, P_slack = get_line_power(n_bus, Theta, connections, line_impedance, Base_MVA)
    print(f'The Line powers are:\n{"-"*100}\n{P_line}\n{"-"*100}\n')
    print(f'Power Generation at swing bus:\n{"-"*100}\n{P_slack}\n{"-"*100}\n')

#Modify and uncomment the following lines to run this

# n_bus = 3
# P_g = [230, 20, 0] 
# P_d = [0, 200, 50] 
# connections = ['21', '21', '23', '13']
# line_impedance = [0.2, 0.2, 0.2, 0.2]
# Base_MVA = 100 
# dc_line_flow(n_bus, P_g, P_d, connections, line_impedance, Base_MVA = 100)

