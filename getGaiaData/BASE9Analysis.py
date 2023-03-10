import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as units

def readGaiaData(filepath: str) -> pd.DataFrame:
    data = pd.read_csv(filepath, sep='\s+', skiprows=180)
    data = data.rename(columns={'phot_g_mean_mag': 'G', 'phot_bp_mean_mag': 'G_BP', 'phot_rp_mean_mag': 'G_RP'})
    return data[['source_id', 'G', 'G_BP', 'G_RP', 'ra', 'dec']]

def findSeparation(dataframe: pd.DataFrame) -> pd.DataFrame:
    c1 = SkyCoord((dataframe['ra']),(dataframe['dec']),unit='deg')
    c2 = SkyCoord((295.3250),(40.19),unit='deg')
    distance = c1.separation(c2).value
    return distance 