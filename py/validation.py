# ***** Script validation *****
from pydantic import BaseModel, Field, field_validator

# **** Creation de la classe building_formula par heritage de la classe BaseModel(pydantic) ****
class building_formula(BaseModel):

    # *** Verrouillage des types de données ***

    # --- Types des categories ---
    BuildingType: str
    PrimaryPropertyType: str
    Neighborhood: str

    # --- Types entiers ---
    NumberofBuildings: int = Field(ge=1)
    NumberofFloors: int = Field(ge = 1)
    YearBuilt: int = Field(ge = 1000, le = 2026)
    sum_energy_use: int = Field(ge = 1, le = 3)
    sum_types_use: int = Field(ge = 1, le = 3)

    # --- Types floats ---
    PrimaryPropertyUseTypeGFA: float = Field(ge = 0)
    SecondLargestPropertyUseTypeGFA: float = Field(ge = 0)
    ThirdLargestPropertyUseTypeGFA: float = Field(ge = 0)

    # --- Binaires 0 ou 1 ---
    use_steam: int = Field(ge = 0, le = 1)
    has_third_use: int = Field(ge = 0, le= 1)

    # *** Validateurs (garde-fou) ***

    # --- Correspondance des infrastructures ---
    @field_validator('BuildingType')
    @classmethod
    def check_BuildiingType(cls, v):
        allowed = ['NonResidential', 'Nonresidential COS', 'SPS-District K-12', 'Campus', 'Nonresidential WA']  
        if v not in allowed:
            raise ValueError(f"{v} Infrastructure non repertoriée")
        return v

    # --- Correspondance des structures de bâtiments ---
    @field_validator('PrimaryPropertyType')
    @classmethod
    def check_PrimaryPropertyType(cls, v):
        allowed = ['Hotel', 'Other', 'Mixed Use Property', 'K-12 School', 'University', 'Small- and Mid-Sized Office', 'Self-Storage Facility', 'Warehouse', 'Large Office', 'Senior Care Community', 'Medical Office', 'Retail Store', 'Hospital', 'Residence Hall', 'Distribution Center', 'Worship Facility', 'Supermarket / Grocery Store', 'Laboratory', 'Refrigerated Warehouse', 'Restaurant', 'Low-Rise Multifamily', 'Office']  
        if v not in allowed:
            raise ValueError(f"Bâtiments {v} non repertorié")
        return v

    # --- Correspondance des quartiers ---
    @field_validator('Neighborhood')
    @classmethod
    def check_Neighborhood(cls, v):
        allowed = ['DOWNTOWN', 'SOUTHEAST', 'NORTHEAST', 'EAST', 'Central', 'NORTH', 'MAGNOLIA / QUEEN ANNE', 'LAKE UNION', 'GREATER DUWAMISH', 'BALLARD', 'NORTHWEST', 'CENTRAL', 'SOUTHWEST', 'DELRIDGE', 'Ballard', 'North', 'Delridge', 'Northwest', 'DELRIDGE NEIGHBORHOODS']  
        if v not in allowed:
            raise ValueError(f"Quartier {v} non repertorié")
        return v

    # --- Cohérence de l'âge du bâtiment ---
    @field_validator('YearBuilt')
    @classmethod
    def check_years(cls, v):
        from datetime import datetime
        if v > datetime.now().year :
            raise ValueError(f"Année {v} incohérente")
        return v

if __name__ == "__main__":
    # test
        # Test valide
    test_ok = building_formula(
        BuildingType="Campus",
        PrimaryPropertyType="Hotel",
        Neighborhood="DOWNTOWN",
        NumberofBuildings=1,
        NumberofFloors=3,
        YearBuilt=2005,
        sum_energy_use=2,
        sum_types_use=1,
        PrimaryPropertyUseTypeGFA=5000.0,
        SecondLargestPropertyUseTypeGFA=0.0,
        ThirdLargestPropertyUseTypeGFA=0.0,
        use_steam=0,
        has_third_use=0
    )
    print("Valide:", test_ok)

    # Test invalide
    try:
        test_ko = building_formula(
            BuildingType="Maison",
            PrimaryPropertyType="Hotel",
            Neighborhood="DOWNTOWN",
            NumberofBuildings=1,
            NumberofFloors=3,
            YearBuilt=2005,
            sum_energy_use=2,
            sum_types_use=1,
            PrimaryPropertyUseTypeGFA=5000.0,
            SecondLargestPropertyUseTypeGFA=0.0,
            ThirdLargestPropertyUseTypeGFA=0.0,
            use_steam=0,
            has_third_use=0
        )
    except Exception as e:
        print("Rejete:", e)