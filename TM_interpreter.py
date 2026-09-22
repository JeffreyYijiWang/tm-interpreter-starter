# Carnegie Mellon University 15-251 Great Ideas in Theoretical Computer Science
# Homework 3 Programming Assignment
# Starter code for TM_interpreter 
# TODO Implement the Turing Machine Interpreter

from TM_classes import State, Configuration, TuringMachine, Result
    
def TM_interpret(M, x, k = None):
    """TODO implement function that simulates TM M on input x. A Universal TM!

    Inputs: 
        - M: TuringMachine
        - x: str is the string representing the input to the TM
        - k: int is an optional parameter used if we want to simulate the TM for maximum of k steps (inclusive)
    Returns: tuple containing two elements
        - list of Configuration corresponding to the configuration of the TM at each timestep (including the initial configuration)
        - Result of ACCEPT, REJECT, or UNDETERMINED based on the behavior of the TM on input x
    Note:
        - If M is not a valid encoding of a TM, then we reject, with `None` as our list of configurations
        - If k is not set and TM loops forever, this function should loop forever as well
    """
    if not validate_TM(M): return (None, Result.REJECT) # First, check that the input TM is a correct encoding.

    #TODO: What should the initial configuration be?
    #the intial configuration should be the q0 to the left 
    u = ""
    q = M.q0
    v = x
    config = Configuration(u,q, v) 
    config_list = [config]
    index = 0
    while True:
        if (isinstance(k, set)):
            return (config_list, Result.UNDETERMINED)
        elif(index == k):
            return (config, Result.REJECT)


        config = simulate_step(M, config)
        config_list.append(config)
            
        if(config.q == M.q_acc):
            return (config, Result.ACCEPT)
        elif(config.q == M.q_rej):
            return (config, Result.REJECT)

        index = index + 1 
        

        
        
        # TODO fill in the rest of this loop
        # When do we know to Accept or Reject?
        # If k is set, when do we return "Undetermined after k steps"?
        # Remember to keep track of the configuration at each time step!

        # Finally, remember that each step corresponds to an application of
        # the transition function. If k = 3, we allow three applications of
        # the transition function. See the provided test cases for exact
        # details.

def validate_TM(M):
    """TODO Determine if the TM is correctly defined.
    
    Assume that the types of given parameters are correct (ex. Q is a set containing State objects, etc).
    Here are some things that you should check:
        - does Q contain q0, q_acc, and q_rej
        - is the input alphabet a subset of the tape alphabet?
        - etc (determine the other things you should check)
    Return True if the input TM is a valid encoding, False otherwise.
    """

    if ((M.q0 not in M.Q )or( M.q_acc not in M.Q ) or (M.q_rej not in M.Q)):
        return False
    if(M.Gamma == {}):
        return False
    if(M.Sigma & M.Gamma) != M.Sigma:
        return False
    if(M.Sigma)== {}:
        return False

    """
    check all delta to have valid states, in Q, and s that is in teh input alphebte
    """
    for config in M.delta:
        new_state, new_tape_s, dir = config
        if((new_state not in M.Q ) or (dir != 'L' ) or(dir != 'R')
            or new_tape_s not in M.Sigma):
           return False

    for q in M.Q:
        for tape_s in M.Sigma:
            if((q,tape_s) not in M.delta):
                return False
            new_state, new_tape_s, dir = M.delta(q,tape_s)
            if((new_state not in M.Q ) or (dir != 'L' ) or(dir != 'R')
                or new_tape_s not in M.Sigma):
                return False
            if(dir == 'L' and q == M.q0):
                return False
            """ thknk about how going left on a q0 is false """
         
    return True
          
def simulate_step(M, config):
    """TODO this is a helper function used by interpret to simulate one step of the TM.

    This is optional, but will be helpful in writing the TM interpreter.

    Given the current configuration, we want to compute and return the next configuration.


    """
    u, q, v = config.u, config.q, config.v # current configuration
    s = v[0]
    # TODO compute the next configuration!
    q_new,new_s, dir = M.delta(q, s)
    ## we need to consider the empy case where you are at the end
    if(dir == 'L'):
        v = new_s+ v 
        if(u != ""):
            u = u[:-1]
    else:
        u = u + new_s
        if(v != ""):
            v = v[1:]
        
    

     

    return Configuration(u, q_new, v) # return next configuration
