import requests;
from typing import Any;
import json;
from django.core.management.base import BaseCommand;
from rest_api.models import Service, Layer, Feature;

class Command(BaseCommand):
    URL_NAME_LAYERS = 'layers';
    COL_NAME_LAYERS = 'layers';
    URL_NAME_QUERY = 'query';
    COL_NAME_FEATURES = 'features';

    services : list[str] = list(set([
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/coastal_environmental_baseline_program/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/coastal_biodiversity_benthic_epifauna_st_lawrence_estuary_2018_2019_en/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/inventory_macroalgae_benthic_macroinvertebrates_nshore_stlawrence_2019_en/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/characterization_of_the_batture_aux_alouettes_kelp_bed_in_2018_2019_en/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/development_coastal_species_charaterization_edna_12s/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/development_coastal_species_characterization_edna_coi/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/biodiversity_of_the_whelk_buccinum_dredge_survey_in_the_st_lawrence_estuary_en/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/biodiversity_snow_crab_trawl_survey_st_lawrence_estuary_2019_en/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/saint_john_intertidal_water_level_temp_sites/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/coastal_baseline_program_placentia_bay_biological_and_water/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/placentia_bay_ctd_moorings/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/atlantic_salmon_smolt_marine_migration_nw_placentia_bay/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/atlantic_salmon_smolt_marine_migration_nw_placentia_bay/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/seasonal_bar_haven_atlantic_cod_spawning_grounds_placentia_bay/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/fish_invertebrate_assemblages_coastal_st_lawrence_estuary_north/MapServer",
        "https://egisp.dfo-mpo.gc.ca/arcgis/rest/services/open_data_donnees_ouvertes/epifauna_diversity_burrard_inlet_fraser_river_delta_bc/MapServer",
    ]));

    def get_request_pjson(self : BaseCommand, url : str, params : dict = {}) -> Any:
        params['f'] = 'pjson';
        response : requests.Response = requests.get(url=url, params=params);
        response.raise_for_status();
        data : Any = json.loads(response.text);
        return data;

    def manage_service(self : BaseCommand, service_data : Any, service_url : str) -> Service:
        service, created = Service.objects.update_or_create(
            url=service_url,
            defaults={
                'name': service_data.get('mapName', ''),
                'description': service_data.get('description', ''),
                'short_description': service_data.get('documentInfo', {}).get('Title', ''),
                'copyright_text': service_data.get('copyrightText', ''),
                'spatial_reference': service_data.get('spatialReference', {}).get('wkid'),
                'full_extent': service_data.get('fullExtent', {}),
            }
        );

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Service créé: {service.name}")
            );
        else:
            self.stdout.write(
                self.style.WARNING(f"🔁 Service mis à jour: {service.name}")
            );

        return service;

    def manage_layer(self : BaseCommand, layer_data : Any, service : Service) -> Layer:
        layer, created = Layer.objects.update_or_create(
            service=service,
            layer_id=layer_data['id'],
            defaults={
                'name': layer_data.get('name', ''),
                'display_name': layer_data.get('name', ''),
                'description': layer_data.get('description', ''),
                'geometry_type': layer_data.get('geometryType', ''),
                'display_field': layer_data.get('displayField', ''),
                'spatial_reference': layer_data.get('extent', {}).get('spatialReference', {}).get('wkid'),
                'extent': layer_data.get('extent', {}),
                'fields_definition': layer_data.get('fields', []),
            }
        );

        action = "créé" if created else "mis à jour";
        self.stdout.write(f"\t📁 Layer {layer.layer_id} {action}: {layer.name}");

        return layer;

    def manage_feature(self : BaseCommand, feature_data : Any, layer : Layer, features_data : Any) -> None:
        attributes : Any = feature_data.get('attributes', {});
        geometry : Any = feature_data.get('geometry', {});

        Feature.objects.update_or_create(
            layer=layer,
            object_id=attributes.get('OBJECTID'),
            defaults={
                'site_name': attributes.get('site_name', ''),
                'geometry_type': features_data.get('geometryType', ''),
                'geometry_data': geometry,
                'attributes': attributes,
            }
        );

    def handle(self : BaseCommand, *args, **options) -> None:
        self.stdout.write("🚀 Début de l'import ArcGIS...");

        total_services : int = len(self.services);
        services_processed : int = 0;
        layers_processed : int = 0;
        features_processed : int = 0;

        for i, s in enumerate(self.services, 1):
            self.stdout.write(f"\n📡 [{i}/{total_services}] Traitement: {s}");

            try:
                service_data : Any = self.get_request_pjson(s);
                service : Service = self.manage_service(service_data, s);
                services_processed += 1;

                sl : str = '';
                if s[-1] != '/':
                    sl = s + '/' + self.URL_NAME_LAYERS;
                else:
                    sl = s + self.URL_NAME_LAYERS;

                try:
                    layers : Any = self.get_request_pjson(sl);
                    layers_count = len(layers[self.COL_NAME_LAYERS]);
                    self.stdout.write(f"\t📂 {layers_count} layer(s) trouvé(s)");

                    for l in layers[self.COL_NAME_LAYERS]:
                        layer : Layer = self.manage_layer(l, service);
                        layers_processed += 1;

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
                            };
                            features : Any = self.get_request_pjson(sf, params=f_params);
                            features_count = len(features[self.COL_NAME_FEATURES]);

                            for f in features[self.COL_NAME_FEATURES]:
                                self.manage_feature(f, layer, features);
                                features_processed += 1;

                            self.stdout.write(f"\t\t📊 {features_count} feature(s) importée(s)");

                        except Exception as e:
                            self.stderr.write(
                                self.style.ERROR(f"\t\t❌ Erreur features layer {l_id}: {e}")
                            );

                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Service {service.name} TERMINÉ")
                    );

                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"\t❌ Erreur layers: {e}")
                    );

            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"❌ Erreur service: {e}")
                );

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Import terminé! "
                f"{services_processed}/{total_services} service(s), "
                f"{layers_processed} layer(s), "
                f"{features_processed} feature(s)"
            )
        );
