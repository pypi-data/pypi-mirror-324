import subprocess
import pytest
import urllib3
# Desactivar solo el warning de solicitudes HTTPS no verificadas
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
# flake8: noqa

from opencapif_sdk import capif_invoker_connector, capif_provider_connector, service_discoverer, capif_logging_feature, capif_invoker_event_feature, capif_provider_event_feature,api_schema_translator


capif_sdk_config_path = "./capif_sdk_config_sample_test.json"

# Fixture para configurar el proveedor
@pytest.fixture
def provider_setup():
    provider = capif_provider_connector(capif_sdk_config_path)
    provider.onboard_provider()
    yield provider
    provider.offboard_provider()

# Fixture para configurar el proveedor
@pytest.fixture
def invoker_setup():
    invoker = capif_invoker_connector(capif_sdk_config_path)
    invoker.onboard_invoker()
    yield invoker
    invoker.offboard_invoker()

@pytest.fixture
def test_provider_update(invoker_setup):
    invoker = capif_invoker_connector(capif_sdk_config_path)
    invoker.update_invoker()

@pytest.fixture
def test_provider_publish(provider_setup):
    provider=capif_provider_connector(capif_sdk_config_path)
    APF1 = provider.provider_capif_ids['APF-1']
    APF2 = provider.provider_capif_ids['APF-2']
    AEF1 = provider.provider_capif_ids['AEF-1']
    AEF2 = provider.provider_capif_ids['AEF-2']
    AEF3 = provider.provider_capif_ids['AEF-3']
    
    translator = api_schema_translator("./test1.yaml")
    translator.build("test1",ip="0.0.0.0",port=9090)
    provider.api_description_path="test1.json"
    # Update configuration file
    provider.publish_req['publisher_apf_id'] = APF1
    provider.publish_req['publisher_aefs_ids'] = [AEF1]
    
    provider.publish_services()

def test_invoker_discover(invoker_setup):
    discoverer = service_discoverer(config_file=capif_sdk_config_path)
    discoverer.discover()
    discoverer.get_tokens()

def test_provider_unpublish_1(test_provider_publish):
    provider=capif_provider_connector(capif_sdk_config_path)
    APF1 = provider.provider_capif_ids['APF-1']
    provider.publish_req['publisher_apf_id'] = APF1
    service_api_id = provider.provider_service_ids["API of dummy Network-App to test"]
    provider.publish_req['service_api_id'] = service_api_id
    provider.unpublish_service()


def preparation_for_update(APFs, AEFs, second_network_app_api,capif_provider_connector):
    
    capif_provider_connector.apfs = APFs
    capif_provider_connector.aefs = AEFs
    if second_network_app_api:
        capif_provider_connector.api_description_path = "./network_app_provider_api_spec_2.json"
    else:
        capif_provider_connector.api_description_path = "./network_app_provider_api_spec_3.json"         
    
    return capif_provider_connector


    
