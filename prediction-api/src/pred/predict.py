""" Module to design inference workflows"""

def infer_prediction(features: dict):
    """ Makes inference using predefined model to give a prediction
    based on input features.

    Parameters
    ----------
        features (dict): dict of features

    Returns
    -------
        result (int): predicted price for rent 
    """

    result = 1
    for v in features.values():
        result *= v

    return result
