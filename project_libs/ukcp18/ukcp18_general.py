"""
ukcp18_general.py
=================

General functions/data for the UKCP18 project.

"""

def map_ensemble_member(**facets):
    """
    Returns ensemble member facet value.
    
    :param facets: dictionary of current facets.
    :return: ensemble member value.
    """
    return facets['ensemble_member']
