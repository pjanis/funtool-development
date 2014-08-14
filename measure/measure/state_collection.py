# Defines a State Collection, which is a collection of states along with their associated groups

import collections

StateCollection = collections.namedtuple('StateCollection',['states','groups_dict'])

# A StateCollection is the default collection for a measure. It consists of a list of states (from state.py)
# along with a groups_dict, which has selector names as keys ( see selector.py ) and a list of groups (from group.py)  

def join_state_collections( collection_a, collection_b):
    """
    Warning: This is a very naive join. Only use it when measures and groups will remain entirely within each subcollection.

    For example: if each collection has states grouped by date and both include the same date, then the new collection 
        would have both of those groups, likely causing problems for group measures and potentially breaking many things.

    """
    
    return StateCollection(
            (collection_a.states + collection_b.states), 
            { group_selector_method:(collection_a.groups_dict.get(group_selector_method,[]) + collection_b.groups_dict.get(group_selector_method,[]))
                for group_selector_method in set( list(collection_a.groups_dict.keys()) + list(collection_b.groups_dict.keys()) ) })
