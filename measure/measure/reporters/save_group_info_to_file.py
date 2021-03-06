# This reporter will save all meta and measures for all states in a state_collection to a file
# Reporter should include the following parameters
# save_directory    location of the save file
# filename          basename of the file
# filetype          file type which is added as an extension, either csv or tsv
# overwrite         boolean to overwrite existing file if it exists


import csv
import json

import os.path



def save(reporter,state_collection):  #This is all quick and dirty for a demo. Should be cleaned up.
    if not _can_write(reporter):
        raise ReporterError("Can't write to %s at %s" % (reporter.parameters['filename'], reporter.parameters['save_directory'] ) )
    grouping_value= reporter.parameters['grouping_value']
    grouping_value_type= reporter.parameters['grouping_value_type']
    reporting_value= reporter.parameters['reporting_value']
    path_and_filename= os.path.join(reporter.parameters['save_directory'],".".join([reporter.parameters['filename'], reporter.parameters['file_type']]))
    
    with open( path_and_filename, 'w', newline='' ) as f:
        writer = _get_writer(reporter,f)
        groups = {}
        for state in sorted(state_collection.states, key= lambda state: state.meta.get('filename','')):
            group_key= getattr(state,grouping_value_type).get(grouping_value,'None')
            current_values= groups.get(group_key, [])
            groups[group_key]= current_values + [state.measures.get(reporting_value)]
        number_of_rows= max( [ len(vals) for k,vals in groups.items() ])
        
        group_names= list(groups.keys())
        _write_line(reporter,writer, ( ["save_number"] + group_names ) )
        for idx in range(number_of_rows):
            write_values = [idx]
            for name in group_names:
                if len(groups[name]) > idx:
                    write_values.append(groups[name][idx])
                else:
                    write_values.append(None)
            _write_line(reporter,writer, write_values ) 
    return state_collection


# Internal functions

def _can_write(reporter):
    path_and_filename=  os.path.join(reporter.parameters['save_directory'],".".join([reporter.parameters['filename'], reporter.parameters['file_type']]))
    return os.path.exists(reporter.parameters['save_directory']) and ( not os.path.exists(path_and_filename) or reporter.parameters['overwrite'] )
    

def _get_writer(reporter, file_handler):
    if reporter.parameters['file_type'].lower() == 'csv' :
        return csv.writer(file_handler)
    elif reporter.parameters['file_type'].lower() == 'tsv' :
        return file_handler
    else :
        return None

def _write_line(reporter, writer, state_values):
    if reporter.parameters['file_type'].lower() == 'csv' :
        writer.writerow(state_values) 
    elif reporter.parameters['file_type'].lower() == 'tsv' :
        writer.write( "\t".join([ _write_value(v) for v in state_values ]))
        writer.write( "\n" )
    return True

def _write_value(value): #converts value in json encoded string if possible and a regular string if not
    try:
        write_value= json.dumps(value)
    except:
        write_value= str(value)
    return write_value
        
   
