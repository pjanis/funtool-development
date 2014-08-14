import importlib
import os
import inspect

import measure
import measure.analysis

# Configuration Locations
# processes defined in the last location take precedence

measure_path= os.path.dirname(inspect.getfile(measure))

default_locations= [
    measure_path,
    os.path.join('.','config')
]

primary_analyses_directory= os.path.join('.','analyses')


#supplemental analyses directories, intended for sub-analyses
analyses_directories= [
    'analysis',
    'analyses'
]

process_types= [
    'adaptor',
    'state_selector',
    'state_measure',
    'reporter'
]

# This could probably be replaced with inflect, but for one instance it's probably not worth it
def _process_type_default_directory(process_type):
    return {
        'adaptor':'adaptors',
        'state_selector':'state_selectors',
        'state_measure':'state_measures',
        'reporter':'reporters'
    }[process_type]


# API Functions

def load_config(locations=default_locations,process_types=process_types):
    known_processes={}
    for process_type in process_types:
        known_processes[process_type]=_load_from_locations(process_type,locations)
    return known_processes

def load_primary_analyses(primary_analyses_location= primary_analyses_directory):
    primary_analyses=[]
    for config_file in _available_config_files(primary_analyses_directory):
        primary_analyses.append( measure.analysis.import_config(config_file) )   
    return [ analysis for config_analyses in primary_analyses for analysis in config_analyses ]
     

def load_known_analyses(locations=default_locations, primary_analyses=None):
    if primary_analyses == None:
        primary_analyses = load_primary_analyses()
    known_analyses = {}
    for location in locations:
        for analyses_directory in analyses_directories:
            for possible_analyses_directory in _mangle(analyses_directory):
                dir_path = os.path.join(location, possible_analyses_directory )
                for config_file in _available_config_files(dir_path):
                    config_file_analyses= measure.analysis.import_config(config_file)
                    for config_file_analysis in config_file_analyses:
                       known_analyses[config_file_analysis.name] = config_file_analysis    
    for primary_analysis in primary_analyses:
       known_analyses[primary_analysis.name] = primary_analysis    
    return known_analyses     

def prepare_analyses(known_processes=None,known_analyses=None, primary_analyses=None):
    if primary_analyses == None:
        primary_analyses = load_primary_analyses()
    if known_analyses == None:
        known_analyses = load_known_analyses()
    if known_processes == None:
        known_processes = load_config()
    return [ measure.analysis.load_processes(analysis,known_processes,known_analyses) for analysis in primary_analyses ]
   

def run_analyses(prepared_analyses=None):
    """
        If all defaults are ok, this should be the only function needed to run the analyses.
    """
    if prepared_analyses == None:
        prepared_analyses = prepare_analyses()
    state_collection = measure.state_collection.StateCollection([],{})
    for analysis in prepared_analyses:
        state_collection= measure.analysis.run_analysis(analysis, state_collection)
    return state_collection
    
       

# Internal Functions

def _load_from_locations(process_type,locations):
    process_module = importlib.import_module("measure."+process_type)
    process_config_import = getattr(process_module,"import_config")
    process_type_alts = _mangle(process_type)
    loaded_processes = {}
    for location in locations:
        for process_type_alt in process_type_alts:
            process_directory= os.path.join(location,_process_type_default_directory(process_type_alt))
            for config_file in _available_config_files(process_directory): 
                for process_name,process in process_config_import(config_file).items():
                    loaded_processes[process_name]=measure.analysis.Process(*process)
    return loaded_processes

def _available_config_files(directory):
    available_files=[]
    for root, subdirectories, files in os.walk(directory):
        for f in files:
            if f.endswith(".yaml") or f.endswith(".yml"):
                available_files.append(os.path.join(root,f))
    return sorted(available_files)

# TODO mangles a particular directory_string to give other possible strings
def _mangle(directory_string):
    return [directory_string] 
        
