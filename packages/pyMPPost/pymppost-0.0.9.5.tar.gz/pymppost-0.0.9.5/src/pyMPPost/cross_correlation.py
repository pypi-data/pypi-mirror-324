# -*- coding: utf-8 -*-
"""
file: cross_correlation.py
discription:
"""
import logging

import numpy as np
import pandas as pd


def cross_correlation(ph_df, info):
    """ Calculates the cross correlation between different detectors
    """
    logging.info("Beginning Cross Correlation")
    ph_df["particle_label"] = ph_df.particle_type.map({1:"n",2:"g", 3:"g"})
    start_detectors = info["cross_correlation"]["start_detectors"]

    for start_detect in start_detectors:
        logging.info("Computing Cross Correlation for start detector %s", start_detect)
        filtered_df = ph_df[ph_df["cell"].eq(start_detect).groupby("history").transform("any")
                            & ph_df["cell"].ne(start_detect).groupby("history").transform("any")]
        start_df = filtered_df[filtered_df["cell"] == start_detect]
        oth_df = filtered_df[~(filtered_df["cell"] == start_detect)]

        computed1 = np.split(start_df[["time","particle_label"]].values,
                             np.unique(start_df.index.values, return_index=True)[1][1:])
        computed2 = np.split(oth_df[["time","particle_label"]].values,
                             np.unique(oth_df.index.values, return_index=True)[1][1:])

        time_data = [np.subtract.outer(oth[:,0],start[:,0]).flatten()
                     for start, oth in zip(computed1,computed2)]
        label_data = [np.add.outer(start[:,1], (oth[:,1])).flatten()
                     for start, oth in zip(computed1,computed2)]

        cc_df = pd.DataFrame({"time_diff":np.concatenate(time_data),
                              "labels":np.concatenate(label_data)})

        if info["cross_correlation"]["all_cc"] == "tsv":
            cc_df.to_csv(f"{info['i/o']['output_root']}_detector_{start_detect}_All_CC",
                         index=False, sep="\t")

        tot, edges = np.histogram(a=cc_df["time_diff"], bins=info["cross_correlation"]["hist_bins"])
        hist = np.column_stack((edges[:-1], tot,
                                np.histogram(cc_df[cc_df.labels == "nn"]["time_diff"], edges)[0],
                                np.histogram(cc_df[cc_df.labels == "gn"]["time_diff"], edges)[0],
                                np.histogram(cc_df[cc_df.labels == "nn"]["time_diff"], edges)[0],
                                np.histogram(cc_df[cc_df.labels == "gg"]["time_diff"], edges)[0]))

        np.savetxt(fname=f"{info['i/o']['output_root']}_detector_{start_detect}_CC_Hist",
                   X=hist)

    logging.info("Cross Correlation Complete")
