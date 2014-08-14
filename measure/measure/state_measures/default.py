# These are default state_measure functions
# A state_measure function shoudl accept a StateMeasure, an AnalysisCollection, a StateCollection, and
#   an optional overriding_parameters
# It should return an AnalysisCollection and update Measure for the state in the AnalysisCollection


import math
import os.path
import datetime
import re

import measure.state_measure


# Function to record a fixed value to a state

def record_parameters(state_measure, analysis_collection, state_collection, overriding_parameters=None):
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    state= analysis_collection.state
    for measure_parameter in measure_parameters:
        state.measures[measure_parameter['parameter_name']]=measure_parameter['parameter_value']
    return analysis_collection

def block_counts(state_measure, analysis_collection, state_collection, overriding_parameters=None):
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    block_counts= _block_counts(_state_scripts(analysis_collection.state) )
    for block_type,block_count in block_counts.items():
        analysis_collection.state.measures[block_type+"_count"]=block_count
    return analysis_collection

def measure_ratio(state_measure, analysis_collection, state_collection, overriding_parameters=None):
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    a_measure = measure_parameters['first_measure']
    b_measure = measure_parameters['second_measure']
    measure_default = measure_parameters.get('measure_default',0)
    measure_name = measure_parameters.get('ratio_name', a_measure+"_to_"+b_measure )
    a_value= analysis_collection.state.measures.get(a_measure,measure_default)
    b_value= analysis_collection.state.measures.get(b_measure,measure_default)
    analysis_collection.state.measures[measure_name]=_compute_ratio(a_value,b_value)
    return analysis_collection

def creation_time_from_filename(state_measure, analysis_collection, state_collection, overriding_parameters=None):
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    filename_base = os.path.splitext(analysis_collection.state.meta.get('filename',''))[0]
    if filename_base.isnumeric():
        if len(filename_base)== 10:
            seconds_since_epoch= int(filename_base)
        else:
            seconds_since_epoch= int(filename_base)/1000.0
        analysis_collection.state.measures['creation_time']= datetime.datetime.fromtimestamp(seconds_since_epoch)
    return analysis_collection

def total_scripts(state_measure, analysis_collection, state_collection, overriding_parameters=None): #includes stage
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    analysis_collection.state.measures['total_scripts']= len(_state_scripts(analysis_collection.state))
    return analysis_collection

def scripts_with_block(state_measure, analysis_collection, state_collection, overriding_parameters=None): #includes stage
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    block_name = measure_parameters['block_name']
    count = 0
    for script in _state_scripts(analysis_collection.state):
        if block_name in str(script):
            count += 1
    analysis_collection.state.measures['scripts_with_'+block_name] = count
    return analysis_collection

def total_sprites(state_measure, analysis_collection, state_collection, overriding_parameters=None): #Does not include stage
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    analysis_collection.state.measures['total_sprites'] = len(_all_sprite_scripts(analysis_collection.state))
    return analysis_collection 

def number_of_scripted_sprites(state_measure, analysis_collection, state_collection, overriding_parameters=None): #Does not include stage
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    analysis_collection.state.measures['sprites'] = len([ sprite_scripts for sprite_scripts in _all_sprite_scripts(analysis_collection.state) 
                                                          if len(sprite_scripts) > 0 ] )
    return analysis_collection 

def number_of_sprites_with_block(state_measure, analysis_collection, state_collection, overriding_parameters=None): #includes stage
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    block_name = measure_parameters['block_name']
    count= 0
    for sprite_scripts in _all_sprite_scripts(analysis_collection.state):
        if block_name in str(sprite_scripts):
            count += 1
    analysis_collection.state.measures['sprites_with'+block_name] = count
    return analysis_collection
    
def scripted_stage(state_measure, analysis_collection, state_collection, overriding_parameters=None):
    measure_parameters = _get_measure_parameters(state_measure, overriding_parameters)
    analysis_collection.state.measures['scripted_stage'] = 1 if len(_stage_scripts) > 0 else 0
    return analysis_collection

@measure.state_measure._state_and_parameter_measure
def number_of_blocks_of_type(state,parameters):
    return sum([ str(_state_scripts(state)).count(block) for block in parameters.get('blocks',[]) ])


def _get_measure_parameters(state_measure, overriding_parameters):
    measure_parameters= state_measure.parameters
    if overriding_parameters != None:
        for param, val in overriding_parameters.items():
            measure_parameters[param] = val
    return measure_parameters

def _state_scripts(state): #returns all a list of all the scripts in a state
    json_data= state.data.get('json')
    scripts=[]
    if json_data != None:
        scripts.extend(json_data.get('scripts',[]))
        for child in json_data.get('children'):
            scripts.extend(child.get('scripts',[]))
    return scripts

def _block_counts(scripts): #counts blocks in a script
    block_counts={}
    for script in scripts:
        if isinstance(script, list):
            if isinstance(script[0],str):
                block_counts[script[0]] = block_counts.get(script[0],0) + 1
            for subvalue in script:
                if isinstance(subvalue, list):
                    for block_type, block_count in _block_counts(subvalue).items():
                        block_counts[block_type] = block_counts.get(block_type,0) + block_count
    return block_counts

def _compute_ratio(a_value,b_value):
    if b_value == 0:
        if a_value == 0:
            ratio= float('Nan')
        else:
            ratio= math.copysign(float('inf'),a_value)
    else:
        ratio= a_value/b_value
    return ratio

def _all_sprite_scripts(state): #returns a list of lists, each sublist is a list of scripts for each sprite  DOES NOT INCLUDE STAGE
    json_data= state.data.get('json')
    sprite_scripts
    if json_data != None:
        for child in json_data.get('children'):
            if 'scripts' in child:
                sprite_scripts.append(child.get('scripts',[]))
    return sprite_scripts

def _stage_scripts(state): #returns a list of scripts for the stage 
    return state.data.git('json').get('scripts',[])

