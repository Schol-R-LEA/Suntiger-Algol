# part of the Suntiger Algol project
# initiated 2008:05:25, by Joseph Osako, Jr. <josephosako@gmail.com>
# file last modified 2015:03:08

from typecheck import *


class State (object):
    """ Class representing the states of a Finite State Automata.
    
    Instance Variables:
        transitions: dictionary (string:integer)
        final: boolean
        toktype: Object
        pushback: integer
    
    State object consist of four properties: an a-list of accepted input
    strings and numeric identifiers for the succeeding states, a flag
    indicating if the state can lead to a final (accept or reject) state,
    the condition returned when accepted, and a number of characters which
    the recognizer should push back by. A State can take an input character
    and return an identifying number for the corresponding successor State. 
    
    The State class has five class constants. Four of these represent common
    states for all state machines (START, ACCEPT, ERROR, and DEFAULT). The
    last represents a default input.
    """
    START = 0
    ACCEPT = -1
    ERROR = -2
    DEFAULT = -3
    OTHER = "__OTHER__"

    def __init__(self, transitions, final = False, \
                toktype = ERROR, pushback = 0):
        """ Constructor - create a State object.
        
       @params:
        transitions - lookup table of inputs and states
        final - final/non-final state flag (default false)
        toktype - type of token recognized on accept (default None)
        pushback - number of chars to push back after accept (default 0)
        
        Initializes the instance variables for the new object.
       """
        self.__final, self.__toktype = final, toktype
        self.__transitions = transitions
        self.__pushback = pushback
    
#    @takes("State", str)
#    @returns(tuple)
    @typecheck
    def next(self, input: str):
        """ Return the successive state based on the input character.
        
         The next() method is the primary behavior of the State object.
        It returns a tuple containing the successor state, whether it 
        is a final state or not, the recognized result (if any) and the
        amount of pushback (if any).
        
        next() takes a single character input: it will reject any string not
        of size one, returning the number of extraneous characters in
        'pushback'. The method first tries to match the character to a
        state through a simple lookup, on the assumption that most transitions
        will be based on a single possible input. If this does not succeed,
        it will try to match the characters against keys with multiple
        characters; this allows a given state transition to give a set of
        possible matches (e.g., all alphanumeric characters) rather than
        requiring a separate key for each character. If this does not succeed,
        it then checks to see if there is a default state set. If none of these
        find a match, the method returns an error state.
        
        If a successor is found, the method then checks to see if the successor
        is either ACCEPT or ERROR. If it is ACCEPT, it returns the ACCEPT
        constant, a true final value, the type of the recongized token, and
        a pushback amount. If it is ERROR, it returns the ERROR constant, a
        true final value, ERROR as the token type, and the pushback amount.
        Otherwise, it returns the successor and false/None/0 for the remainder.
       """
        if len(input) != 1:         # check validity of the input
            return self.ERROR, False, self.ERROR, len(input) - 1
        
        # try to match the input to a transition
        successor = None
        if input in self.__transitions:     # check single-character key match
            successor = self.__transitions.get(input)
        else:
            for s in self.__transitions:    # check multi-char keys
                if input in s and s != self.OTHER:
                    successor = self.__transitions.get(s)
                    break
            if successor is None:           # use default transition, if any
                successor = self.__transitions.get(self.OTHER)
                if successor is None:
                    return self.ERROR, False, self.ERROR, 0
                
        # successor found, test if it is either an ACCEPT or ERROR state.
        if successor == self.ACCEPT:    # ACCEPT
            return self.ACCEPT, True, self.__toktype, self.__pushback
        elif successor == self.ERROR:   # ERROR
            return self.ERROR, True, self.ERROR, self.__pushback
        else:
            # not a final state, return the successor state 
            return successor, False, None, 0
        
        def __str__(self):
            """ Basic string representation of a State."""
            return str(self.__transitions)
            


class StateMachine(object):
    """ Generalized Finite State Automata class.
    
    Instance Variables:
        states: a lookup table of state numbers and states
        current_state: the current state of the FSM
        locked: flag whether all of the states are set.
    
    A FSM consists of a set of States, the current State, and a flag
    indicating if all States have been added to the set of states. Until
    the FSM is locked, new states may be added. The State machine begins
    in the Start state, and accepts input until it either accepts or rejects
    the input string. When it reaches one of these final states, it returns
    the type of the recognized string and resets itself to the Start state.
   """
    def __init__(self, start_state):
        """ Constructor - create a FSM object.        
        
        Adds the initial (Start) state, sets the current state to Start,
        and clears the locked flag.
       """
        self.__states = {State.START: start_state}
        self.__locked = False
        self.__current_state = self.__states[State.START]


    @typecheck
    def add(self, key: int, state: State):
        """ Add a new state to the state table.
        
        The add() method takes a state identifier key and a new State
        object. If the table is not locked, and there is no State
        by that number already, it adds state to the state table
        and returns true. Otherwise, it returns false.
       """
        if self.__locked:
            return False   # do not allow any states to be added
        elif key in self.__states:  # state with that ID already in table
            return False
        else:
            self.__states[key] = state
            return True
    
    def lock(self):
        """ Locks state table so no new states can be added."""
        self.__locked = True
        
#    @returns(tuple)
    def transition(self, input) -> tuple:
        """ Perform a state transition, and if it is a final
        state, return success or failure and the recognized token type. 
       """
        # get the successor state of the current state, if any
        successor, final, token, pb = self.__current_state.next(input)
        
        # see if the state has finalized, reset the current state and 
        # determine if it accepted or rejected the input string
        if final:
            self.__current_state = self.__states[State.START]
            
            if successor == State.ACCEPT:   # string accepted
                return True, token, pb
            else:                           # string rejected
                return True, State.ERROR, pb 
        # if the state has not finalized, see if it is a 'non-final' error
        # state and return an error value if it is. This will only occur if
        # the input is not valid.
        elif successor == State.ERROR:
            self.__current_state = self.__states[State.START]
            return True, State.ERROR, pb
        # if the state is not final and not an error, advance to the next state
        else:
            self.__current_state = self.__states[successor]
            return False, 0, 0
    
    def __str__(self):
        """Return a simple string representation of the FSM for debugging. """
        return str(self.__states)
    
################################
if __name__ == "__main__":
    pass
