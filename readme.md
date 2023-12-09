The code will not give prompt for taking inputs, you have to give it manually. The input should be like the following: 

dc_line_flow(n_bus, P_g, P_d, connections, line_impedance, Base_MVA = 100)

    n_bus = number of bus
    P_g = list of generator real powers; if Pg_1 = unknown, give 0 as input
    P_d = list of generator demands
    connections = list of strings to show how the buses are connected (first element = starting bus, second_element = ending bus)
    line_impedance = list of line impedances in p.u. corresponding to connections list

    if line impedance is  infinite, give np.inf as input

    Example of input (3 bus, 3 line system):

    n_bus = 3 ; 3 bus system
    P_g = [0, 630, 0] ; P_g2 = 63 MW, P_g3 = 0 MW
    P_d = [0, 100, 90] ; P_d1 = 0 MW, P_g2 = 63 MW, P_g3 = 0 MW
    connections = ['12', '23', '13']
    line_impedance = [0.0576, 0.092, 0.17]
    Base_MVA = 100 ; base apparant power

    dc_line_flow(3, P_g, P_d, [0, 630, 0], line_impedance, Base_MVA = 100)
