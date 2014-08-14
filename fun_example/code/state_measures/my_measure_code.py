
import measure.state_measures.default
import numbers

def all_ratios(state_measure, analysis_collection, state_collection, overriding_parameters=None):
    measure_parameters = measure.state_measures.default._get_measure_parameters(state_measure, overriding_parameters)
    all_measures= list(analysis_collection.state.measures.keys())
    for idx,first_measure in enumerate(all_measures):
        if isinstance(analysis_collection.state.measures[first_measure],numbers.Number):
            for second_measure in all_measures[(idx+1):-1]:
                if isinstance(analysis_collection.state.measures[second_measure],numbers.Number):
                    a_value= analysis_collection.state.measures[first_measure]
                    b_value= analysis_collection.state.measures[second_measure]
                    analysis_collection.state.measures[first_measure+"_to_"+second_measure]= measure.state_measures.default._compute_ratio(a_value,b_value)
    return analysis_collection
            
