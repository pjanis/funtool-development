# Defines an analysis and provides methods to run it

# An analysis should be an ordered list of group_selectors, measures, reporters, and other analyses (i.e. analyses can be nested).

import collections 
import yaml
import functools

import measure.state_collection


Analysis = collections.namedtuple('Analysis',['name','process_identifiers','processes'])

# ProcessIdentifiers are defined in the analysis config, Processes are created internally

ProcessIdentifier = collections.namedtuple('ProcessIdentifier', ['process_type','process_name'])

Process= collections.namedtuple('Process',['collection','process_function'])


AnalysisCollection = collections.namedtuple('AnalysisCollection',['state','group','state_list'])

# An AnalysisCollection is a collection generated from a StateCollection used during part of the analysis
#
# In this collection are:
# state         a privileged state used by a process ( often the current state )
# group         a privileged group
# state_list    a privileged list of states, often from previous processes


def import_config(config_file_location):
    new_analyses=[]
    with open(config_file_location) as f:
        yaml_config= yaml.load(f)
    for individual_analysis in yaml_config:
        analysis_name, analysis_parameters = next(iter(individual_analysis.items()))
        new_analyses.append( Analysis(analysis_name, load_process_identifiers(analysis_parameters), []) )
    return new_analyses

def load_process_identifiers(analysis_parameters):
    return [ ProcessIdentifier(**process_parameters) for process_parameters in analysis_parameters ]        

def load_processes(analysis,known_processes, known_analyses):
    check_process_existence(analysis,known_processes,known_analyses)
    for process_id in analysis.process_identifiers:    
        if process_id.process_type == 'analysis':
            sub_analysis= load_processes(known_analyses[process_id.process_name], known_processes, known_analyses)
            analysis.processes.append(analysis_process(sub_analysis) )              
        else:
            analysis.processes.append(known_processes[process_id.process_type][process_id.process_name])
    return analysis 

def analysis_process(analysis): # returns a function which takes and returns a StateCollection and runs an analysis
    return functools.partial(run_analysis, analysis)

def run_analysis(analysis,state_collection=None):
    print("Running Analysis : " + analysis.name )
    if state_collection == None :
        state_collection = measure.state_collection.StateCollection([],{})        
    for idx,process in enumerate(analysis.processes):
        print("Running step "+ str(idx+1) + " : " + analysis.process_identifiers[idx].process_name )
        new_state_collection= process.process_function(state_collection)
        if isinstance(new_state_collection, measure.state_collection.StateCollection):
            state_collection = new_state_collection
        else:
            print("Error in process : StateCollection not returned")
            print("Continuing with previous StateCollection")
    return state_collection


# TODO needs to be made recursive for measures, etc...
def check_process_existence(analysis,known_processes, known_analyses):
    missing_processes= False
    for process_id in analysis.process_identifiers:    
        try:
            if process_id.process_type == 'analysis':
                check_process_existence(known_analyses[process_id.process_name], known_processes, known_analyses)
            else:
                known_processes[process_id.process_type][process_id.process_name]
        except KeyError:
            print("Process " + process_id.process_type + " "+ process_id.process_name + " is unknown.")
            missing_processes= True
    if missing_processes :
        raise Exception("Missing Processes")
    return True



