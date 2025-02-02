import hashlib
import pickle
import copy
import pandas as pd



def deep_copy(obj):
    '''
    Description
    --------------------
    Returns deep copy of a given object. For pandas DataFrames or Series,
    uses pandas' native copy method.

    Parameters
    --------------------
    obj : object
        object to be copied

    Returns
    --------------------
    out : object
        deep copy of object
    '''
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        return obj.copy(deep=True)
    else:
        return copy.deepcopy(obj)



def sha256(*args):
    '''
    Description
    --------------------
    Returns sha256 hash value for any arbitrary number of arguments.

    Parameters
    --------------------
    args : tuple
        arguments to hashed

    Returns
    --------------------
    out : str
        sha256 hash value
    '''
    return hashlib.sha256(pickle.dumps(args)).hexdigest()