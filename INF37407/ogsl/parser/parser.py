import requests;
from typing import Any;
import json;
from pprint import pprint;

COL_NAME_LAYERS = 'layers';

def get_layers(url : str) -> Any:
    params : dict = {'f' : 'pjson'};
    response : requests.Response = requests.get(url=url, params=params);
    response.raise_for_status();
    data : Any = json.loads(response.text);
    return data;

def manage_layers(layers : Any) -> None:
    for l in layers[COL_NAME_LAYERS]:
        print(f"=== LAYER {l.get('id', 'N/A')}: {l.get('name', 'N/A')} ===")
        print(f"Type: {l.get('geometryType', 'N/A')} | Display: {l.get('displayField', 'N/A')}")
        print(f"Champs: {[f['name'] for f in l.get('fields', [])]}")
        print(f"SRID: {l.get('extent', {}).get('spatialReference', {}).get('wkid', 'N/A')}")
        print()

def main() -> int:
    services : list[str] = list(set([
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/coastal_environmental_baseline_program/MapServer/layers",
        # "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/underwater_vehicle_survey_musquash_mpa/MapServer/layers",
        # "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/biodiversity_of_the_whelk_buccinum_dredge_survey_in_the_st_lawrence_estuary_fr/MapServer/layers",
        # "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/characterization_of_the_batture_aux_alouettes_kelp_bed_in_2018_2019_fr/MapServer/layers",
        # "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/inventory_macroalgae_benthic_macroinvertebrates_nshore_stlawrence_2019_fr/MapServer/layers",
        # "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/coastal_biodiversity_benthic_epifauna_st_lawrence_estuary_2018_2019_fr/MapServer/layers",
        # "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/saint_john_intertidal_water_level_temp_sites/MapServer/layers",
    ]));

    for s in services:
        try:
            layers : Any = get_layers(s);
            print(f"Layers Ok for the service : {s}.");
            manage_layers(layers);
        except Exception as e:
            print(f"Exception : {e} occured for the service : {s}.");
            pass
    return 0;

if __name__ == "__main__":
    ret_val : int = main();
    exit(ret_val);
