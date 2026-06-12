# ***** Script validation *****
from pydantic import BaseModel, Field, field_validator

# **** Creation de la classe building_formula par heritage de la classe BaseModel(pydantic) ****
class building_formula(BaseModel):

    # *** Verrouillage des types de données ***

    # --- Types des categories ---
    BuildingType: str = Field(alias = 'Type de bâtiments')
    PrimaryPropertyType: str = Field(alis = 'Bâtiment principal')
    Neighborhood: str = Field(alias = 'Quartier')

    # --- Types entiers ---
    NumberofBuildings: int = Field(ge=1, alias = 'Nombre de bâtiments' )
    NumberofFloors: int = Field(ge = 1, alias = 'Nombre d\'étage')
    YearBuilt: int = Field(ge = 1000, le = 2016, alias = 'Année de construction')
    sum_energy_use: int = Field(ge = 1, le = 3, alias = 'Nombre de source d\'energie utilisée')
    sum_types_use: int = Field(ge = 1, le = 3, alias = 'Nombre d\'usage des bâtiments')

    # --- Types floats ---
    PrimaryPropertyUseTypeGFA: float = Field(ge = 0, alias = 'Surface de l\'usage principal')
    SecondLargestPropertyUseTypeGFA: float = Field(ge = 0,alias = 'Surface de l\'usage secondaire')
    ThirdLargestPropertyUseTypeGFA: float = Field(ge = 0, alias = 'Surface de l\'usage tertiaire')

    # --- Binaires 0 ou 1 ---
    use_steam: int = Field(ge = 0, le = 1, alias = 'Usage de la vapeur comme source d\'énergie')
    has_third_use: int = Field(ge = 0, le= 1,'Bâtiments ayant plus de 3 usages' )

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