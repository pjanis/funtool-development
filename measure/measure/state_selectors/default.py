# These are a default set of state_selector functions
# A state selector function should accept three parameters a StateSelector, an AnalysisCollection and a StateCollection
#  it should return an AnalysisCollection
# All functions that don't accept (StateSelector,AnalysisCollection,StateCollection) and return AnalysisCollection should
#  be internal functions

def trivial(state_selector, analysis_collection, state_collection):
    return analysis_collection

