# ***** Script Service *****

# Librairies
import bentoml
import numpy as np 
import pandas as pd 
from .validation import building_formula

@bentoml.service
class EnergyPrediction :
    def __init__(self):
        # Charge le pipeline du modèle pour la prediction
        self.pipeline = bentoml.sklearn.load_model('model_nr_seattle_v1:latest')

        # charge le model stocké dans le magasin bentoml
        bento_model = bentoml.models.get('model_nr_seattle_v1:latest')

        self.features_names = bento_model.custom_objects['features_names']

    @bentoml.api
    def predict(self, input_data: building_formula):
        data = input_data.model_dump()

        building_age = 2016 - data["YearBuilt"]
        total_ty_gfa = data["PrimaryPropertyUseTypeGFA"] + data["SecondLargestPropertyUseTypeGFA"] + data["ThirdLargestPropertyUseTypeGFA"]
        floor_surface = total_ty_gfa / data["NumberofFloors"]
        ratio_build = data["NumberofBuildings"] / data["NumberofFloors"]

        features = {
                "building_age": building_age,
                "BuildingType": data["BuildingType"],
                "floor_surface": floor_surface,
                "has_third_use": data["has_third_use"],
                "Neighborhood": data["Neighborhood"],
                "NumberofBuildings": data["NumberofBuildings"],
                "NumberofFloors": data["NumberofFloors"],
                "PrimaryPropertyType": data["PrimaryPropertyType"],
                "ratio_build": ratio_build,
                "SecondLargestPropertyUseTypeGFA": data["SecondLargestPropertyUseTypeGFA"],
                "sum_energy_use": data["sum_energy_use"],
                "sum_types_use": data["sum_types_use"],
                "ThirdLargestPropertyUseTypeGFA": data["ThirdLargestPropertyUseTypeGFA"],
                "total_ty_gfa": total_ty_gfa,
                "use_steam": data["use_steam"],
            }
        
        df = pd.DataFrame([features], columns = self.features_names)

        prediction_log = self.pipeline.predict(df)

        prediction_kBtu = np.expm1(prediction_log[0])

        return {"consommation_estimee_kbtu": round(float(prediction_kBtu), 2)}
