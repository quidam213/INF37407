import requests;
from typing import Any;
import json;
from pprint import pprint;
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    URL_NAME_LAYERS = 'layers';
    COL_NAME_LAYERS = 'layers';
    URL_NAME_QUERY = 'query';
    COL_NAME_FEATURES = 'features';

    services : list[str] = list(set([
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/coastal_environmental_baseline_program/MapServer",
        #!! ajouter ici les autres services compatibles (arcgis + opengouv canada) et 1 seul layer
    ]));

    def get_request_pjson(self : BaseCommand, url : str, params : dict = {}) -> Any:
        params['f'] = 'pjson';
        response : requests.Response = requests.get(url=url, params=params);
        response.raise_for_status();
        data : Any = json.loads(response.text);
        return data;

    def manage_service(self : BaseCommand, service : Any) -> None:
        print(f"=== SERVICE: {service.get('mapName', 'N/A')} ===")
        print(f"Description: {service.get('description', 'N/A')[:100]}...")
        print(f"Copyright: {service.get('copyrightText', 'N/A')}")
        print(f"SRID: {service.get('spatialReference', {}).get('wkid', 'N/A')}")
        print(f"Unités: {service.get('units', 'N/A')}")
        print(f"Emprise: xmin={service.get('fullExtent', {}).get('xmin', 'N/A')}, ymin={service.get('fullExtent', {}).get('ymin', 'N/A')}, xmax={service.get('fullExtent', {}).get('xmax', 'N/A')}, ymax={service.get('fullExtent', {}).get('ymax', 'N/A')}")
        print(f"Nombre de layers: {len(service.get('layers', []))}")
        print()

    def manage_layer(self : BaseCommand, layer : Any) -> None:
        print(f"=== LAYER {layer.get('id', 'N/A')}: {layer.get('name', 'N/A')} ===")
        print(f"Type: {layer.get('geometryType', 'N/A')} | Display: {layer.get('displayField', 'N/A')}")
        print(f"Champs: {[f['name'] for f in layer.get('fields', [])]}")
        print(f"SRID: {layer.get('extent', {}).get('spatialReference', {}).get('wkid', 'N/A')}")
        print()

    def manage_feature(self : BaseCommand, feature: Any) -> None:
        attributes = feature.get('attributes', {})
        geometry = feature.get('geometry', {})

        feature_id = attributes.get('OBJECTID', 'N/A')
        lat = attributes.get('decimalLatitude', attributes.get('Latitude', 'N/A'))
        lon = attributes.get('decimalLongitude', attributes.get('Longitude', 'N/A'))

        print(f"   FEATURE ID: {feature_id}")
        print(f"   Latitude: {lat}")
        print(f"   Longitude: {lon}")
        print(f"   Géométrie: {len(geometry.get('points', []))} point(s)")

        if geometry.get('points'):
            print(f"   Coordonnées techniques: {geometry['points'][0]}")

        other_attrs = {k: v for k, v in attributes.items()
                    if k not in ['OBJECTID', 'decimalLatitude', 'decimalLongitude', 'Latitude', 'Longitude']}
        if other_attrs:
            print(f"   Autres attributs: {other_attrs}")

        print()

    def handle(self : BaseCommand, *args, **options) -> None:
        for s in self.services:
            try:
                service : Any = self.get_request_pjson(s);
                self.manage_service(service);
                sl : str = '';
                if s[-1] != '/':
                    sl = s + '/' + self.URL_NAME_LAYERS;
                else:
                    sl = s + self.URL_NAME_LAYERS;
                try:
                    layers : Any = self.get_request_pjson(sl);
                    print(f"Layers Ok for the service : {s}.");
                    for l in layers[self.COL_NAME_LAYERS]:
                        self.manage_layer(l);
                        try:
                            sf : str = '';
                            l_id : str = str(l.get('id'));
                            if s[-1] != '/':
                                sf = s + '/' + l_id + '/' + self.URL_NAME_QUERY;
                            else:
                                sf = s + l_id + '/' + self.URL_NAME_QUERY;
                            f_params : dict = {
                                'where': '1=1',
                                'outFields': '*',
                                'returnGeometry': 'true',
                            }
                            features : Any = self.get_request_pjson(sf, params=f_params);
                            print(f"Features Ok for the layer : {l_id}.");
                            for f in features[self.COL_NAME_FEATURES]:
                                self.manage_feature(f);
                        except Exception as e:
                            print(f"Exception : {e} occured for the service : {s} while getting features of the layer {l.get('id', 'N/A')} : {l.get('name', 'N/A')}.");
                            pass
                except Exception as e:
                    print(f"Exception : {e} occured for the service : {s} while getting layers.");
                    pass
            except Exception as e:
                print(f"Exception : {e} occured for the service : {s}.");
                pass
