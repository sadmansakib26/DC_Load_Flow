The code will not give prompt for taking inputs, you have to give it manually. The input should be like the following: 

dc_line_flow(n_bus, P_g, P_d, connections, line_impedance, Base_MVA = 100, **line_data)

    n_bus = number of bus
    P_g = list of generator real powers, give P_g1 = 0
    P_d = list of generator demands
    connections = list of strings to show how the buses are connected (first element = starting bus, second_element = ending bus)
    line_impedance = list of line impedances in p.u. corresponding to connections list
    line_data = equivalent line impedances in p.u.

    if line impedance is  infinite, give np.inf as input

    Example of input (3 bus, 3 line system):

    n_bus = 3 ; 3 bus system
    P_g = [0, 630, 0] ; P_g2 = 63 MW, P_g3 = 0 MW
    P_d = [0, 100, 90] ; P_d1 = 0 MW, P_g2 = 63 MW, P_g3 = 0 MW
    connections = ['12', '23', '13']
    line_impedance = [0.0576, 0.092, 0.17]
    Base_MVA = 100 ; base apparant power
    **line_data = equivalent impedance in p.u. for the keywords, first letter must be a character (any), next two letters are connected buses

    dc_line_flow(3, P_g, P_d, [0, 630, 0], line_impedance, Base_MVA = 100, z12=0.0576, z23=0.092, z13=0.17)


