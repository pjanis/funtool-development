# Defines a state selector
import collections
import yaml
import importlib
import functools

StateSelector = collections.namedtuple('StateSelector',['selector_module','selector_function','parameters'])

# A state selector is one which selects one or more states based on a particular state
#    
# selector_module           the module where the selector function is defined 
# selector_function         a function used to create the selection
# parameters                a dict of parameters for the selector function
#
# For example: One state selector may find all the states with the same user id as a given state
#
# Another example: A state selector to find the next state based on on time stamp


def import_config(config_file_location):
    new_state_selectors={}
    with open(config_file_location) as f:
        yaml_config= yaml.load(f)
    for state_selector_name,state_selector_parameters in yaml_config.items():
        new_state_selector= StateSelector(**state_selector_parameters)
        new_state_selectors[state_selector_name]= (new_state_selector, state_selector_process(new_state_selector)) 
            # for ** explination https://docs.python.org/2/tutorial/controlflow.html#tut-unpacking-arguments

    return new_state_selectors


def state_selector_process(state_selector): #returns a function, that accepts a state_collection, to be used as a process
    state_selector_module = importlib.import_module(state_selector.selector_module)
    return functools.partial( getattr(state_selector_module,state_selector.selector_function), state_selector )
    

