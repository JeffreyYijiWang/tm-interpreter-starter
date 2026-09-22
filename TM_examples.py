# Carnegie Mellon University 15-251 Great Ideas in Theoretical Computer Science
# Homework 3 Programming Assignment
# Starter code for TM_examples
# TODO Define a TuringMachine object that solves the given problems

from TM_classes import State, TuringMachine

def TM1():
    """Define and then return a Turing Machine with the following behavior:

    Input alphabet is {0, 1}. 
    The tape alphabet is a superset of {0, 1,X, _}, where _ is the blank symbol.
    (It is up to you if you want the tape alphabet to contain more symbols.)
    If the input has equal number of 0s and 1s, accept.
    Otherwise, reject.

    we want to have the accepted states be we have all input written to X, and then 
    then when we move to the left to the _ we accept
    we reject, when we hit _ of the left or right but we have not 

    we have to use the way we are collect the 1's and zero s
    """
    q_even = State("q_even")
    q_extra_1 = State("q_extra_1")
    q_extra_0 = State("q_extra_2")
    q_left_to_start = State("q_left_to_start")
    q_search_for_1 = State("q_search_for_1")
    q_search_for_0 = State("q_search_for_0")
    q_acc = State("q_acc")
    q_rej = State("q_rej")
    sigma = {'0','1'}
    gamma = {'0', '1', 'X' , '_'}

    q = {q_even,   q_extra_1,  q_extra_0,  q_left_to_start,  q_search_for_1,
          q_search_for_0,q_acc, q_rej}

    delta = {
             ( q_even, 'X'): (q_even, 'X' , 'R'), 
             ( q_even, '0'): (q_extra_0, 'X' , 'L'), 
             ( q_even, '1'): (q_extra_1, 'X' , 'L'), 
             ( q_even, '_'): (q_acc, '_' , 'L'), 
             ( q_extra_0, '_'): (q_search_for_1, '_' , 'R'), 
             ( q_extra_0, '0'): ( q_extra_0, '0' , 'L'), 
             ( q_extra_0, '1'): ( q_extra_0, '1' , 'L'), 
             ( q_extra_0, 'X'): ( q_extra_0, 'X' , 'L'),
             ( q_extra_1, '_'): (q_search_for_0, '_' , 'R'), 
             ( q_extra_1, '0'): (q_extra_1, '0' , 'L'), 
             ( q_extra_1, '1'): (q_extra_1, '1' , 'L'), 
             ( q_extra_1, 'X'): (q_extra_1, 'X' , 'L'),
             ( q_search_for_1, '_'): (q_rej, '_' , 'L'),
             ( q_search_for_1, '1'): (q_left_to_start, 'X' , 'L'),
             ( q_search_for_1, '0'): (q_search_for_1, '0' , 'R'),
             ( q_search_for_1, 'X'): ( q_search_for_1, 'X' , 'R'),
            ( q_search_for_0, '_'): (q_rej, '_' , 'L'),
            ( q_search_for_0, '1'): (q_left_to_start, '1' , 'R'),
            ( q_search_for_0, '0'): (q_search_for_0, 'X' , 'L'),
            ( q_search_for_0, 'X'): ( q_search_for_0, 'X' , 'R'),
            ( q_left_to_start, '0'): ( q_left_to_start, '0' , 'L'),
            ( q_left_to_start, '1'): ( q_left_to_start, '1' , 'L'),
            ( q_left_to_start, 'X'): ( q_left_to_start, 'X' , 'L'),
            ( q_left_to_start, '_'): ( q_even, '_' , 'R')
             }

    M = TuringMachine(q, sigma, gamma, delta, q_even, q_acc, q_rej)
    return M


def TM2():
    """Define and then return a Turing Machine with the following behavior:

    Input alphabet is {0, 1}.
    The tape alphabet is a superset of {0, 1, _}, where _ is the blank symbol.
    (It is up to you if you want the tape alphabet to contain more symbols.)
    If the input does not correspond to the usual binary encoding of a natural number,
    output the empty string.
    Otherwise, output x + 1 in binary, where x is the input number.
    """
        
    q0 = State("q0")
    q1 = State("q1")
    q_acc = State("q_acc")
    q_rej = State("q_rej")
    sigma = {'0','1'}
    gamma = {'0', '1', '_'}
    q = {q0, q1, q_acc, q_rej}

    delta = {(q0, '_'): (q_rej, '_' , 'R'), 
                (q0, '0'): (q_acc, '1' , 'R'), 
                (q0, '1'): (q1, '0' , 'R'), 
                (q1, '0'): (q_acc, '1' , 'R'), 
                (q1, '1'): (q1, '0' , 'R'),
                (q1, '_'): (q_acc, '1' , 'R')  
                }

    M = TuringMachine(q, sigma, gamma, delta, q0, q_acc, q_rej)
    
    return M
   

def Bonus():
    """Define and then return a Turing Machine with the following behavior: (BONUS)

    
    Input alphabet is {0, 1, $}.
    The tape alphabet is a superset of {0, 1, $, _}, where _ is the blank symbol.
    (It is up to you if you want the tape alphabet to contain more symbols.)
    If the input is not of form x$y where x and y are binary encodings of natural numbers,
    output the empty string.
    Otherwise, output the sum of x and y in binary.
    """
      