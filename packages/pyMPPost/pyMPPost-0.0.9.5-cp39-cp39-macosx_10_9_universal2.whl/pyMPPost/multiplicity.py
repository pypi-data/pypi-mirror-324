# -*- coding: utf-8 -*-
# NOT COMPLETED 
"""
file: multiplicity.py
discription:
"""
import logging

import numpy as np
import pandas as pd
import math
from .cython_functs import shift_register_counting 


def multiplicity(ph_df, info):
    """ Multiplicity Cout
    """
    logging.info("Beginning Scintilator Multiplicity")
    ph_df["particle_label"] = ph_df.particle_type.map({1:"n",2:"g", 3:"g"})
    ph_df["window"] = shift_register_counting(ph_df.index.values, 
                                              ph_df.time.values, 
                                              info["multiplicity"]["window_width"], 
                                              info["multiplicity"]["mult_tol"])
    ph_df.sort_values(["window","particle_label"])
    window_df = ph_df.groupby("window").agg({"particle_label":"sum"}).reset_index()
    total_counts = window_df["particle_label"].count()
    counts = window_df.groupby("particle_label")["window"].count()
    
    
    logging.info("Multiplicity Complete")
    return (counts, total_counts)
