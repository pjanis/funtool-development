# A measure performed and recorded on an individual state

import collections
import yaml
import importlib
import functools

import measure.analysis

StateMeasure = collections.namedtuple('StateMeasure',['measure_module','measure_function','state_selectors','group_selectors','parameters'])

# A StateMeasure is used with an AnalysisCollection and a StateCollection to measure each State in the StateCollection
#   Each State will have a new key added to it's measures (or updated if the key already exists)
#   After measuring the state, an AnalysisCollection is returned
#
# measure_module        a string indicating where the measure_function is defined
# measure_function      a string with the name of the function which measures the state
# state_selectors       a list of selectors which are run sequentially to update the AnalysisCollection
# group_selectors       a list of group_selectors which are used to create groups in the StateCollection before any analysis is run
# parameters            a dict of parameters passed to the measure 

def import_config(config_file_location):
    new_state_measures={}
    with open(config_file_location) as f:
        yaml_config= yaml.load(f)
    for state_measure_name,state_measure_parameters in yaml_config.items():
        new_state_measure= StateMeasure(**state_measure_parameters)
        new_state_measures[state_measure_name]= ( new_state_measure, state_measure_process(new_state_measure)) 
            # for ** explination https://docs.python.org/2/tutorial/controlflow.html#tut-unpacking-arguments

    return new_state_measures


def state_measure_process(state_measure): #returns a function, that accepts a state_collection, to be used as a process
    return _wrap_measure(individual_state_measure_process(state_measure))

def individual_state_measure_process(state_measure):
    state_measure_module = importlib.import_module(state_measure.measure_module)
    return functools.partial( getattr(state_measure_module,state_measure.measure_function), state_measure )

def _wrap_measure(individual_measure_process): 
    """
    Should be moved to MeasureSet when it's complete runs a measure over a statecollection instead of an analysis collection
    """
    def wrapped_measure(state_collection):
        for state in state_collection.states:
            analysis_collection = measure.analysis.AnalysisCollection(state,None,[])
            individual_measure_process(analysis_collection,state_collection)
        return state_collection
    return wrapped_measure
        


def _state_and_parameter_measure(state_measure_function):
    def wrapped_function(state_measure, analysis_collection, state_collection, overriding_parameters=None):
        measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
        measure_value= state_measure_function(analysis_collection.state,measure_parameters)
        analysis_collection.state.measures[measure_parameters.get('measure_name',state_measure_function.__name__)] = measure_value
        return analysis_collection
    return wrapped_function



def _get_measure_parameters(state_measure, overriding_parameters):
    measure_parameters= state_measure.parameters
    if overriding_parameters != None:
        for param, val in overriding_parameters.items():
            measure_parameters[param] = val
    return measure_parameters

