# Allows for a series of measures to be run sequentially

import collections

MeasureSet = collections.namedtuple('MeasureSet',['measures'])

MeasureSetItem = collections.namedtuple('MeasureSetItem',['measure_type','measure_name','parameters'])

# A MeasureSetItem defines one measure to be made on an AnalysisCollection in conjunction with a StateCollection
# measure_type      a string with the type of measure (i.e. group, state, or set )
# measure_name      a string with the name of the measure
# parameters        a dict of parameters that supercede the measure's parameters


