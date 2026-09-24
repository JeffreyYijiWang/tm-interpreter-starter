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
       #TODO: What should the initial configuration be?
    #the intial configuration should be the q0 to the left 
    if not validate_TM(M): return (None, Result.REJECT)
    if not isinstance(x, str): return (None, Result.REJECT)
    if any(s not in M.Sigma for s in x): return (None, Result.REJECT)
    if k is not None and type(k) != int: return (None, Result.REJECT)

    # the initial configuration has q0 to the left of the input
    u = ""
    q = M.q0
    v = x
    config = Configuration(u, q, v)
    config_list = [config]
    index = 0
    while True:
        # Check for halting before checking the limit, including at step k.
        if(config.q == M.q_acc):
            return (config_list, Result.ACCEPT)
        elif(config.q == M.q_rej):
            return (config_list, Result.REJECT)
        elif(k is not None and k >= 0 and index == k):
            return (config_list, Result.UNDETERMINED)

        config = simulate_step(M, config)
        config_list.append(config)
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
    if not isinstance(M, TuringMachine):
        return False
    if not all(isinstance(s, set) for s in (M.Q, M.Sigma, M.Gamma)):
        return False
    if not isinstance(M.delta, dict):
        return False
    if not all(isinstance(q, State) for q in M.Q):
        return False
    if not all(isinstance(q, State) for q in (M.q0, M.q_acc, M.q_rej)):
        return False
    if not all(isinstance(s, str) and len(s) == 1 for s in M.Gamma | M.Sigma):
        return False
    if ((M.q0 not in M.Q) or (M.q_acc not in M.Q) or (M.q_rej not in M.Q)):
        return False
    if(M.q_acc == M.q_rej):
        return False
    if not M.Sigma or not M.Sigma <= M.Gamma:
        return False
    if('_' not in M.Gamma or '_' in M.Sigma):
        return False

    if len(M.delta) != (len(M.Q) - 2) * len(M.Gamma):
        return False

    q_running = M.Q - {M.q_acc, M.q_rej}

    # delta uses tape symbols, and has no transitions from halting states.
    for config, transition in M.delta.items():
        if not isinstance(config, tuple) or len(config) != 2:
            return False
        if not isinstance(transition, tuple) or len(transition) != 3:
            return False
        q, tape_s = config
        new_state, new_tape_s, dir = transition
        if not isinstance(q, State) or not isinstance(new_state, State):
            return False
        if not isinstance(tape_s, str) or not isinstance(new_tape_s, str):
            return False
        if(q not in q_running):
            return False
        if(tape_s not in M.Gamma or new_tape_s not in M.Gamma):
            return False
        if(new_state not in M.Q or dir not in ('L', 'R')):
            return False
    return True
          
def simulate_step(M, config):
    """TODO this is a helper function used by interpret to simulate one step of the TM.

    This is optional, but will be helpful in writing the TM interpreter.

    Given the current configuration, we want to compute and return the next configuration.


    """
    u, q, v = config.u, config.q, config.v

    if(q == M.q_acc or q == M.q_rej):
        return Configuration(u, q, v)

    s = v[0] if v != "" else '_'
    q_new, new_s, dir = M.delta[(q, s)]

    if(dir == 'L'):
        v = v[1:]

        if(new_s != '_' or v != ""):
            v = new_s + v

        if(u != ""):
            v = u[-1] + v
            u = u[:-1]
        elif(v != ""):
            v = "_" + v
    else:
        if(new_s != '_' or u != ""):
            u = u + new_s
        v = v[1:]

    return Configuration(u, q_new, v)
