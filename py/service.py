# ***** Script Service *****

# Librairies
import bentoml
import numpy as np 
import pandas as pd 
from validation import building_formula

@bentoml.service
class EnergyPrediction :
    def __init__(Self):
        self.pipeline = bentoml.sklearn.load_model('model_nr_seattle_v1:latest')
        self.features_names = bento_model.custom_objects['features_names']

@bentoml.api
def predict(self, input_data:'building_formula'):
    data = input_data.load_dump()


df_s2['building_age'] = 2016 - df_s2['YearBuilt']    
df_s2['use_steam'] = (df_s2['SteamUse(kBtu)'] > 0).astype(int)
df_s2['sum_energy_use'] = df_s2['use_electricity'] + df_s2['use_gaz'] + df_s2['use_steam']
df_s2['total_ty_gfa'] = (df_s2['LargestPropertyUseTypeGFA'].fillna(0) + df_s2['SecondLargestPropertyUseTypeGFA'].fillna(0) + df_s2['ThirdLargestPropertyUseTypeGFA'].fillna(0))
df_s2['has_second_use'] = df_s2['SecondLargestPropertyUseTypeGFA'].notna().astype(int)
df_s2['has_third_use'] = df_s2['ThirdLargestPropertyUseTypeGFA'].notna().astype(int)
df_s2['sum_types_use'] = df_s2['has_second_use'] + df_s2['has_third_use'] + 1 # +1 car toujours un usage principal
df_s2['floor_surface'] = df_s2['PropertyGFATotal'] / df_s2['NumberofFloors']
df_s2['building_surface'] = df_s2['PropertyGFATotal'] / df_s2['NumberofBuildings']

















# feature du groupe des surfaces des structures
df_s2['ratio_parking'] =  df_s2['PropertyGFAParking'] / df_s2['PropertyGFATotal']
df_s2['ratio_build'] =  df_s2['PropertyGFABuilding(s)'] / df_s2['PropertyGFATotal']

# features pour le type d'energie utilisée
df_s2['use_electricity'] = (df_s2['Electricity(kWh)'] > 0).astype(int)
df_s2['use_gaz'] = (df_s2['NaturalGas(therms)'] > 0).astype(int)


# feature pour les ratios de surface des usages
df_s2['ratio_prime_ty_gfa'] =  df_s2['LargestPropertyUseTypeGFA'].fillna(0) / df_s2['total_ty_gfa']
df_s2['ratio_second_ty_gfa'] =  df_s2['SecondLargestPropertyUseTypeGFA'].fillna(0) / df_s2['total_ty_gfa']
df_s2['ratio_third_ty_gfa'] =  df_s2['ThirdLargestPropertyUseTypeGFA'].fillna(0) / df_s2['total_ty_gfa']
