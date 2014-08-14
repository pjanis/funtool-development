# Defines a group selector
import collections

GroupSelector = collections.namedtuple('GroupSelector',['name','selector_function','parameters'])

# A group selector is used to create a set of groups. This differs from a state selector which may create
#   a set of states. A group selector does not need to place each state in a collection into a group, but 
#   it often will (i.e. grouping saves by user_id ). 


# name                      a unique name for the selector
# selector_function         a function used to create the selection
# parameters                a dict of parameters for the selector function



