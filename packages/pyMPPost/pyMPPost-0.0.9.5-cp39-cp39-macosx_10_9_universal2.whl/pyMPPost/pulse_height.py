# -*- coding: utf-8 -*-
"""
file: pulse_height.py 
discription: 
"""
import logging

import numpy as np

from .cython_functs import calc_pulses


def pulse_height(plm_ddf, info, client):
    # Calculate Light
    meta = plm_ddf._meta.assign(light=[])
    plm_ddf = plm_ddf.map_partitions(lambda df: df.assign(light=_light_helper(df,info["mats"])),meta=meta)

    # Generate Pulses
    pgt_arr = []
    dt_arr = []
    
    for mat in info["mats"]:
        pgt_arr.append(mat["pulse_creation"]["pgt"]/ 10.0) 
        dt_arr.append(mat["pulse_creation"]["dt"]/ 10.0) 
        
    pgt_arr = np.array(pgt_arr)
    dt_arr = np.array(dt_arr)
    tol = info["pulse_height"]["pulse_tol"]
    
    meta = meta.assign(pulse=[])
    pulses_q = plm_ddf.map_partitions(lambda df: df.assign(pulse=_pulse_helper(df, pgt_arr, dt_arr, tol)), meta=meta)
    
    # Sum Light by Pulse
    pulses_q = pulses_q.groupby(by=["history","cell","pulse"]).agg({'particle_type':'first', 'mat_num':'first', 'time': 'first', 'light': 'sum'})
    
    # Check and Run resolution sub-modules
    pulse_meta = pulses_q._meta
    if info["seed"] == 0:
        gen = np.random.default_rng()
    else:
        gen = np.random.default_rng(info["seed"])
            
    if info["pulse_height"]["time_res_on"]:      
        # time resolution
        pulses_q = pulses_q.map_partitions(lambda df: df.assign(time=_time_res(df,info["mats"],gen)), meta=pulse_meta)
    
    if info["pulse_height"]["energy_res_on"]:
        # energy resolution
        pulses_q = pulses_q.map_partitions(lambda df: df.assign(light=_energy_res(df,info["mats"], gen)), meta=pulse_meta)
    
    logging.info("Beginning Pulse Height Computation") 
    PH_df = client.compute(pulses_q).result().reset_index(["cell", "pulse"])
    PH_df = PH_df[PH_df["pulse"] >= 0]
    PH_df = PH_df[(PH_df["light"] >= info["pulse_height"]["threshold"]["lower"]) & (PH_df["light"] <= info["pulse_height"]["threshold"]["upper"])]
    logging.info("Pulse Height Computation Complete")  
    
    if info["pulse_height"]["all_pulses"] == "tsv":
        PH_df.to_csv(f"{info['i/o']['output_root']}_All_Pulses", header=info['i/o']['output_headers'], sep="\t")
    elif info["pulse_height"]["all_pulses"] == "parquet":
        PH_df.to_parquet(f"{info['i/o']['output_root']}_All_Pulses")
    
    logging.info("Pulse Height Export Complete") 
    
    total, edges = np.histogram(a=PH_df["light"], bins=info["pulse_height"]["hist_bins"])
    neutrons, __ = np.histogram(a=PH_df[PH_df.particle_type == 1]["light"], bins=edges)
    photons, __ = np.histogram(a=PH_df[PH_df.particle_type == 2]["light"], bins=edges)
    np.savetxt(fname=f"{info['i/o']['output_root']}_Pulse_Hist", X=np.column_stack((edges[:-1],total,neutrons,photons)))
    
    return PH_df, (len(PH_df), len(PH_df[PH_df["particle_type"] == 1]))

def _light_helper(df, mats):
    """ helper function to calculate the light value from the respective material's Birk's table

    Args:
        df: Pandas dataframe
        mats: materials
    """
    conditions = []
    choices = []
    
    for i, mat in enumerate(mats):
        cal = mat["calibration"]
        mat_type = mat["mat_type"]
        
        if mat_type == 1:
            conditions.extend([
                (df["mat_num"] == i) & (df["particle_type"] != 1),
                (df["mat_num"] == i) & (df["particle_type"] == 1) & ((df["target_nucleus"] == 6000) | (df["target_nucleus"] == 6012) | (df["target_nucleus"] == 6013)),
                (df["mat_num"] == i) & (df["particle_type"] == 1) & (df["target_nucleus"] == 1001),
            ])
            choices.extend([
                df["energy_deposited"]*cal["photon"][0]+cal["photon"][1],
                df["energy_deposited"]*cal["carbon"],
                np.interp(df["energy_deposited"],cal["birks_energy"],cal["birks_light"]),
            ])
        else:
            conditions.extend([
                (df["mat_num"] == i),
            ])
            choices.extend([
                df["energy_deposited"]*cal["photon"][0]+cal["photon"][1],
            ])

    return np.select(conditions,choices)

def _pulse_helper(df, pgt_arr, dt_arr, tol):
    return calc_pulses(df.index.values,df.cell.values, df.time.values, df.mat_num.values, pgt_arr, dt_arr, tol)

def _time_res(df,mats,gen):
    """ Computes random time broadening

    Args:
        df: Pandas dataframe
        mats: materials
        gen: Numpy Random Generator
    """
    conditions = []
    choices = []
    for i, mat in enumerate(mats):
        conditions.append((df["mat_num"] == i))
        choices.append(mat["resolution"]["time"] / 10.0)
    time_res = np.select(conditions, choices)
    return gen.normal(loc=df["time"],scale=time_res)

def _energy_res(df, mats, gen):
    """ Computes random energy broadening

    Args:
        df: Pandas dataframe
        mats: materials
        gen: Numpy Random Generator
    """
    conditions = []
    choices = []
    for i, mat in enumerate(mats):
        mat_type = mat["mat_type"]
        en_res_p = mat["resolution"]["energy"]["photon"]
        if mat_type == 1:
            en_res_n = mat["resolution"]["energy"]["neutron"]
            conditions.append((df["mat_num"] == i) & (df["particle_type"] != 1))
            choices.append(df["light"] * np.sqrt((en_res_p[0]**2) + ((en_res_p[1]**2)/df["light"]) + ((en_res_p[2]**2)/(df["light"]**2))))
            conditions.append((df["mat_num"] == i) & (df["particle_type"] == 1))
            choices.append(df["light"] * np.sqrt((en_res_n[0]**2) + ((en_res_n[1]**2)/df["light"]) + ((en_res_n[2]**2)/(df["light"]**2))))
        else:
            conditions.append((df["mat_num"] == i))
            choices.append(df["light"] * np.sqrt((en_res_p[0]**2) + ((en_res_p[1]**2)/df["light"]) + ((en_res_p[2]**2)/(df["light"]**2))))
            
    en_half_max = np.select(conditions, choices)
    en_sd = en_half_max / (2 * np.sqrt(2.0 * np.log(2)))        
    return gen.normal(loc=df["light"], scale= en_sd)