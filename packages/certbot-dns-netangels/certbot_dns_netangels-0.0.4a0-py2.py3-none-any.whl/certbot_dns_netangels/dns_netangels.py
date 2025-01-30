"""DNS Authenticator for Netangels."""
import json
import logging
import requests
import time
from urllib.parse import urlencode
import tldextract

import requests
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

LIMIT_GET_RECORDS = 50
DEFAULT_TTL = 300

# Структуры данных
class TXTDnsRecord:
    def __init__(self, name, value, ttl=DEFAULT_TTL):
        self.type = "TXT"
        self.name = name
        self.value = value
        self.ttl = ttl

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "value": self.value,
            "ttl": self.ttl
        }

class CreateDnsResponse:
    def __init__(self, data):
        self.id = data.get('id')
        self.zone_id = data.get('zone_id')
        self.name = data.get('name')
        self.type = data.get('type')
        self.value = data.get('value')
        self.ttl = data.get('ttl')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.details = data.get('details')

class ZoneEntities:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')

class SecondaryDNS:
    def __init__(self, data):
        self.entities = [ZoneEntities(entity) for entity in data.get('entities', [])]

class Zone:
    def __init__(self, data):
        self.comment = data.get('comment')
        self.created_at = data.get('created_at')
        self.editable = data.get('editable')
        self.id = data.get('id')
        self.is_in_transfer = data.get('is_in_transfer')
        self.is_technical_zone = data.get('is_technical_zone')
        self.name = data.get('name')
        self.records_count = data.get('records_count')
        self.secondary_dns = SecondaryDNS(data.get('secondary_dns', {}))
        self.soa_email = data.get('soa_email')
        self.ttl = data.get('ttl')
        self.updated_at = data.get('updated_at')

class Zones:
    def __init__(self, data):
        self.count = data.get('count')
        self.entities = [Zone(zone) for zone in data.get('entities', [])]

class GetRecordsDetails:
    def __init__(self, data):
        self.has_mailserver = data.get('has_mailserver')
        self.is_shared = data.get('is_shared')
        self.is_www = data.get('is_www')
        self.value = data.get('value')
        self.priority = data.get('priority')
        self.ip = data.get('ip')
        self.hostname = data.get('hostname')
        self.port = data.get('port')
        self.protocol = data.get('protocol')
        self.service = data.get('service')
        self.weight = data.get('weight')
        self.domain = data.get('domain')
        self.nameserver = data.get('nameserver')
        self.flag = data.get('flag')
        self.tag = data.get('tag')

class Record:
    def __init__(self, data):
        self.created_at = data.get('created_at')
        self.details = GetRecordsDetails(data.get('details', {}))
        self.id = data.get('id')
        self.ttl = data.get('ttl')
        self.name = data.get('name')
        self.type = data.get('type')
        self.updated_at = data.get('updated_at')

class Records:
    def __init__(self, data):
        self.count = data.get('count')
        self.entities = [Record(record) for record in data.get('entities', [])]

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Netangels

    This Authenticator uses the Netangels Remote REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using Netangels for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=120
        )
        add("credentials", help="Netangels credentials INI file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the Netangels Remote REST API."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Netangels credentials INI file",
            {
                "panelurl": "URL of Panel.",
                "apiurl": "URL of API.",
                "apikey": "API Key of user in panel.",
            },
        )

    def _perform(self, domain, validation_name, validation):
        self._get_netangels_client().present_record(
            domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_netangels_client().webhook_cleanup(
            domain, validation_name, validation, self.ttl
        )

    def _get_netangels_client(self):
        return _NetangelsClient(
            self.credentials.conf("panelurl"),
            self.credentials.conf("apiurl"),
            self.credentials.conf("apikey"),
            None,
        )


class _NetangelsClient(object):
    """
    Encapsulates all communication with the Netangels Remote REST API.
    """

    def __init__(self, panelurl, apiurl, apikey, token):
        logger.debug("creating netangelsclient")
        self.panelurl = panelurl
        self.apiurl = apiurl
        self.apikey = apikey
        self.token = None

    def get_token(self):
        logger.info("GetToken...")
        response = requests.post(self.panelurl, data={"api_key": self.apikey})
        if response.status_code != 200:
            logger.error(f"GetToken. Error status code {response.status_code}")
            raise Exception(f"GetToken. Error status code {response.status_code}")
        token_response = response.json()
        self.token = token_response.get('token')
        logger.info("Token received and stored.")
        return self.token

    def fetch_zones(self, offset):
        url = f"{self.apiurl}/dns/zones/?{urlencode({'limit': LIMIT_GET_RECORDS, 'offset': offset})}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Get zones error response code: {response.status_code}")
            raise Exception(f"get zones error. status {response.status_code}")
        zones_info = response.json()
        return Zones(zones_info)

    def get_zone_id(self, fqdn_name):
        fqdn_name = cut_trailing_dot_if_exist(fqdn_name)
        z_name = get_domain(fqdn_name)
        offset = 0
        while True:
            zones_data = self.fetch_zones(offset)
            if not zones_data.entities:
                break
            for zone in zones_data.entities:
                if zone.name == z_name:
                    logger.info(f"Zone Id {z_name} found: {zone.id}")
                    return zone.id, zones_data.count
            offset += LIMIT_GET_RECORDS
            if offset > zones_data.count:
                break
        logger.error(f"Zone Id {fqdn_name} not found")
        raise Exception(f"Zone Id {fqdn_name} not found")

    def add_txt_record(self, fqdn_name, value):
        fqdn_name = cut_trailing_dot_if_exist(fqdn_name)
        logger.info(f"Create new TXT record for: {fqdn_name} ...")
        txt_record_body = TXTDnsRecord(name=fqdn_name, value=value).to_dict()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        response = requests.post(f"{self.apiurl}/dns/records/", json=txt_record_body, headers=headers)
        if response.status_code == 201:
            create_response = CreateDnsResponse(response.json())
            logger.info(f"The record {fqdn_name} was successfully created")
            return create_response.id
        elif response.status_code == 400:
            logger.error("AddRecord. Incorrect data format or missing mandatory parameters")
            raise Exception("incorrect data format or missing mandatory parameters")
        else:
            logger.error(f"AddRecord error. Unexpected response code: {response.status_code}")
            raise Exception(f"add record error. Unexpected response code: {response.status_code}")

    def remove_record(self, record_id):
        if record_id == 0:
            logger.error("Function RemoveRecord input id=0. Not valid value.")
            return None
        url = f"{self.apiurl}/dns/records/{record_id}/"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            logger.info(f"Record ID {record_id} successfully deleted.")
            return None
        elif response.status_code == 404:
            logger.error(f"Error delete record: DNS-record with ID {record_id} not found")
            raise Exception(f"error delete record: DNS-record with ID {record_id} not found")
        else:
            logger.error(f"Error delete record. Status: {response.status_code}")
            raise Exception(f"error delete record. status: {response.status_code}")

    def fetch_records(self, zone_id, offset):
        url = f"{self.apiurl}/dns/zones/{zone_id}/records/?{urlencode({'limit': LIMIT_GET_RECORDS, 'offset': offset})}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Get records error response code: {response.status_code}")
            raise Exception(f"get records error. status {response.status_code}")
        recors_info = response.json()
        return Records(recors_info)

    def get_txt_record(self, fqdn_name, value_data=""):
        fqdn_name = cut_trailing_dot_if_exist(fqdn_name)
        if not fqdn_name:
            logger.error("function GetTXTRecord get to input FQDNName = ``. Not valid value")
            raise Exception("function GetTXTRecord get to input FQDNName = ``. Not valid value")
        zone_id, _ = self.get_zone_id(fqdn_name)
        offset = 0
        while True:
            records_data = self.fetch_records(zone_id, offset)
            if not records_data.entities:
                break
            for item in records_data.entities:
                if item.type == "TXT" and item.name == fqdn_name:
                    if not value_data:
                        logger.info("Found first in list TXT Record.")
                        return item.id, item.details.value
                    elif item.details.value == value_data:
                        logger.info("A record with a complete data match was found")
                        return item.id, item.details.value
            offset += LIMIT_GET_RECORDS
            if offset > records_data.count:
                break
        logger.info(f"Record {fqdn_name} not found")
        return 0, ""

    def present_record(self, domain, fqdn_name, value_data, ttl):
        self.get_token()
        fqdn_name = cut_trailing_dot_if_exist(fqdn_name)
        logger.info(f"Start function PresentRecord for: {fqdn_name}")
        record_id, _ = self.get_txt_record(fqdn_name, value_data)
        if record_id:
            logger.info(f"PresentRecord. The record {fqdn_name} exists. The data is up to date.")
            return
        record_id, _ = self.get_txt_record(fqdn_name, "")
        if record_id:
            updated, _ = self.update_txt_value_record(record_id, fqdn_name, value_data)
            if updated:
                logger.info(f"PresentRecord. Updated value in a TXT Record {fqdn_name}.")
                return
            else:
                logger.error(f"PresentRecord. Error update value in a TXT Record {fqdn_name}.")
                raise Exception("no error, but not updated record")
        logger.info("PresentRecord. Domain record not found. Will be created")
        self.add_txt_record(fqdn_name, value_data)

    def update_txt_value_record(self, record_id, fqdn_name, value):
        if record_id == 0:
            logger.error("Function UpdateTXTValueRecord get to input ID=0. Not valid value")
            raise Exception("function UpdateTXTValueRecord get to input ID=0. Not valid value")
        txt_record_body = TXTDnsRecord(name=fqdn_name, value=value).to_dict()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.apiurl}/dns/records/{record_id}/", json=txt_record_body, headers=headers)
        if response.status_code == 200:
            logger.info(f"DNS record {fqdn_name} successfully updated")
            return True, None
        else:
            logger.error(f"Error when updating DNS record {fqdn_name}")
            logger.error(f"Failed request, response code: {response.status_code}")
            return False, response.status_code

    def webhook_cleanup(self, domain, fqdn_name, value, ttl):
        self.get_token()
        fqdn_name = cut_trailing_dot_if_exist(fqdn_name)
        logger.info(f"CleanUP for {fqdn_name}")
        record_id, _ = self.get_txt_record(fqdn_name, value)
        if not record_id:
            raise Exception("record for delete not found")
        logger.info(f"Start delete record with ID: {record_id}")
        self.remove_record(record_id)
        logger.info(f"Record {fqdn_name} is deleted")


def get_domain(fqdn_name):
    """
    Функция для получения домена верхнего уровня из строки fqdn_name.
    :param fqdn_name: Полное доменное имя (FQDN)
    :return: Домен верхнего уровня или пустая строка, если домен не найден
    """
    if not fqdn_name:
        return ""
    # Используем tldextract для разбора доменного имени
    extracted = tldextract.extract(fqdn_name)

    # Проверяем, что домен верхнего уровня существует
    if extracted.domain and extracted.suffix:
        domain = f"{extracted.domain}.{extracted.suffix}"
        return domain
    else:
        return ""

def cut_trailing_dot_if_exist(fqdn_name):
    if fqdn_name.endswith('.'):
        return fqdn_name[:-1]
    return fqdn_name
