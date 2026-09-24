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
    q0 = State("q0")
    q_even = State("q_even")
    q_extra_1 = State("q_extra_1")
    q_extra_0 = State("q_extra_0")
    q_left_to_start = State("q_left_to_start")
    q_search_for_1 = State("q_search_for_1")
    q_search_for_0 = State("q_search_for_0")
    q_acc = State("q_acc")
    q_rej = State("q_rej")
    sigma = {'0', '1'}
    gamma = {'0', '1', 'X', 'A', '_'}
    q = {q0, q_even, q_extra_1, q_extra_0, q_left_to_start,
         q_search_for_1, q_search_for_0, q_acc, q_rej}

    # A is a crossed-out symbol that also marks the left edge.
    delta = {
        (q0, '0'): (q_search_for_1, 'A', 'R'),
        (q0, '1'): (q_search_for_0, 'A', 'R'),
        (q0, '_'): (q_acc, '_', 'R'),
        (q_even, 'X'): (q_even, 'X', 'R'),
        (q_even, '0'): (q_extra_0, 'X', 'L'),
        (q_even, '1'): (q_extra_1, 'X', 'L'),
        (q_even, '_'): (q_acc, '_', 'R'),
        (q_extra_0, 'A'): (q_search_for_1, 'A', 'R'),
        (q_extra_1, 'A'): (q_search_for_0, 'A', 'R'),
        (q_search_for_1, '1'): (q_left_to_start, 'X', 'L'),
        (q_search_for_0, '0'): (q_left_to_start, 'X', 'L'),
        (q_left_to_start, 'A'): (q_even, 'A', 'R')
    }
    for tape_s in {'0', '1', 'X'}:
        for state in {q_extra_0, q_extra_1, q_left_to_start}:
            delta[(state, tape_s)] = (state, tape_s, 'L')
    for tape_s in {'0', 'X'}:
        delta[(q_search_for_1, tape_s)] = (q_search_for_1, tape_s, 'R')
    for tape_s in {'1', 'X'}:
        delta[(q_search_for_0, tape_s)] = (q_search_for_0, tape_s, 'R')

    # transitions that cannot occur on valid input.
    for state in q - {q_acc, q_rej}:
        for tape_s in gamma:
            if((state, tape_s) not in delta):
                delta[(state, tape_s)] = (q_rej, '_', 'L')
    M = TuringMachine(q, sigma, gamma, delta, q0, q_acc, q_rej)
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
    q_zero = State("q_zero")
    q_carry = State("q_carry")
    q_overflow = State("q_overflow")
    q_left_to_start = State("q_left_to_start")
    q_finish = State("q_finish")
    q_error = State("q_error")
    q_acc = State("q_acc")
    q_rej = State("q_rej")
    sigma = {'0', '1'}
    gamma = {'0', '1', 'X', '_'}
    q = {q0, q1, q_zero, q_carry, q_overflow, q_left_to_start,q_finish,
         q_error, q_acc, q_rej}

    # X marks the first 1. Carry propagates from right to left.
    delta = {
        (q0, '_'): (q_rej, '_', 'R'),
        (q0, '0'): (q_zero, '1', 'R'),
        (q0, '1'): (q1, 'X', 'R'),
        (q_zero, '_'): (q_acc, '_', 'L'),
        (q_zero, '0'): (q_error, '0', 'R'),
        (q_zero, '1'): (q_error, '1', 'R'),
        (q1, '0'): (q1, '0', 'R'),
        (q1, '1'): (q1, '1', 'R'),
        (q1, '_'): (q_carry, '_', 'L'),
        (q_carry, '1'): (q_carry, '0', 'L'),
        (q_carry, '0'): (q_left_to_start, '1', 'L'),
        (q_carry, 'X'): (q_overflow, 'X', 'R'),
        (q_overflow, '0'): (q_overflow, '0', 'R'),
        (q_overflow, '_'): (q_left_to_start, '0', 'L'),
        (q_left_to_start, '0'): (q_left_to_start, '0', 'L'),
        (q_left_to_start, '1'): (q_left_to_start, '1', 'L'),
        (q_left_to_start, 'X'): (q_finish, '1', 'R'),
        (q_finish, '0'): (q_acc, '0', 'L'),
        (q_finish, '1'): (q_acc, '1', 'L'),
        (q_finish, 'X'): (q_acc, 'X', 'L'),
        (q_finish, '_'): (q_acc, '_', 'L'),
        (q_error, '0'): (q_error, '0', 'R'),
        (q_error, '1'): (q_error, '1', 'R'),
        (q_error, '_'): (q_rej, '_', 'R')
    }
    for state in q - {q_acc, q_rej}:
        for tape_s in gamma:
            if((state, tape_s) not in delta):
                delta[(state, tape_s)] = (q_error, tape_s, 'R')
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
    q0 = State("q0")
    q_x_zero = State("q_x_zero")
    q_x = State("q_x")
    q_y_start = State("q_y_start")
    q_y_zero = State("q_y_zero")
    q_y = State("q_y")
    q_left_to_start = State("q_left_to_start")
    q_check = State("q_check")
    q_to_dollar = State("q_to_dollar")
    q_borrow = State("q_borrow")
    q_to_end = State("q_to_end")
    q_carry = State("q_carry")
    q_overflow = State("q_overflow")
    q_output = State("q_output")
    q_finish = State("q_finish")
    q_error = State("q_error")
    q_acc = State("q_acc")
    q_rej = State("q_rej")
    sigma = {'0', '1', '$'}
    gamma = {'0', '1', '$', 'A', 'B', 'C', 'D', '_'}
    q = {q0, q_x_zero, q_x, q_y_start, q_y_zero, q_y, q_left_to_start,
         q_check, q_to_dollar, q_borrow, q_to_end, q_carry, q_overflow,
         q_output, q_finish, q_error, q_acc, q_rej}

    # A/B mark x's first 0/1, and C/D mark y's first 0/1.
    delta = {
        (q0, '0'): (q_x_zero, 'A', 'R'),
        (q0, '1'): (q_x, 'B', 'R'),
        (q_x_zero, '$'): (q_y_start, '$', 'R'),
        (q_x, '0'): (q_x, '0', 'R'),
        (q_x, '1'): (q_x, '1', 'R'),
        (q_x, '$'): (q_y_start, '$', 'R'),
        (q_y_start, '0'): (q_y_zero, 'C', 'R'),
        (q_y_start, '1'): (q_y, 'D', 'R'),
        (q_y_zero, '_'): (q_left_to_start, '_', 'L'),
        (q_y, '0'): (q_y, '0', 'R'),
        (q_y, '1'): (q_y, '1', 'R'),
        (q_y, '_'): (q_left_to_start, '_', 'L'),
        (q_left_to_start, 'A'): (q_check, 'A', 'R'),
        (q_left_to_start, 'B'): (q_to_dollar, 'B', 'R'),
        (q_check, '0'): (q_check, '0', 'R'),
        (q_check, '1'): (q_to_dollar, '1', 'R'),
        (q_check, '$'): (q_output, '_', 'R'),
        (q_to_dollar, '0'): (q_to_dollar, '0', 'R'),
        (q_to_dollar, '1'): (q_to_dollar, '1', 'R'),
        (q_to_dollar, '$'): (q_borrow, '$', 'L'),
        (q_borrow, '0'): (q_borrow, '1', 'L'),
        (q_borrow, '1'): (q_to_end, '0', 'R'),
        (q_borrow, 'B'): (q_to_end, 'A', 'R'),
        (q_to_end, '_'): (q_carry, '_', 'L'),
        (q_carry, '1'): (q_carry, '0', 'L'),
        (q_carry, '0'): (q_left_to_start, '1', 'L'),
        (q_carry, 'C'): (q_left_to_start, 'D', 'L'),
        (q_carry, 'D'): (q_overflow, 'D', 'R'),
        (q_overflow, '0'): (q_overflow, '0', 'R'),
        (q_overflow, '_'): (q_left_to_start, '0', 'L'),
        (q_output, 'C'): (q_finish, '0', 'L'),
        (q_output, 'D'): (q_finish, '1', 'L'),
        (q_finish, '_'): (q_acc, '_', 'R')
    }
    for tape_s in {'0', '1', '$', 'C', 'D'}:
        delta[(q_left_to_start, tape_s)] = (q_left_to_start, tape_s, 'L')
        delta[(q_to_end, tape_s)] = (q_to_end, tape_s, 'R')
    # Errors halt beyond the input, so the output prefix is empty.
    for tape_s in gamma:
        delta[(q_error, tape_s)] = (q_error, tape_s, 'R')
    delta[(q_error, '_')] = (q_rej, '_', 'R')
    for state in q - {q_acc, q_rej}:
        for tape_s in gamma:
            if((state, tape_s) not in delta):
                delta[(state, tape_s)] = (q_error, tape_s, 'R')
    M = TuringMachine(q, sigma, gamma, delta, q0, q_acc, q_rej)
    return M
      