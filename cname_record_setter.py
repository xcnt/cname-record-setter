import click
import time
from datetime import timedelta
from typing import List
from google.cloud import dns
from dns import resolver as dns_resolver
from datetime import datetime
import logging

from google.cloud.dns import ResourceRecordSet

LOGGER = logging.getLogger('cname_record_setter')


def get_zone(client: dns.Client, record_candidate):
    candidates = list(get_zone_candidate(client, record_candidate))
    if len(candidates) == 0:
        return
    candidates = sorted(candidates, key=lambda entry: len(entry.dns_name), reverse=True)
    return candidates[0]


def get_zone_candidate(client: dns.Client, record_candidate):
    for zone in client.list_zones():
        target = zone.dns_name.strip('.')
        if record_candidate.endswith(target):
            yield zone


class Observer:
    observed_ips: List[str] = []
    last_observe_refresh: datetime = None
    current_record: ResourceRecordSet = None

    def __init__(self, zone: dns.ManagedZone, set_record: str, observed_record: str):
        self.zone = zone
        self.set_record = set_record
        self.observed_record = observed_record

    def observe_loop(self):
        while True:
            LOGGER.debug('Running check loop')
            self.observe()
            time.sleep(30)

    def observe(self):
        if self.observed_set_ips != self.current_target_ips:
            self.update_ips()

    def update_ips(self):
        target_ips = self.current_target_ips
        LOGGER.info('Changing ip addresses of target record from %s to %s' % (self.observed_set_ips, target_ips))
        changes = self.zone.changes()
        if self.current_record is not None:
            changes.delete_record_set(self.current_record)
            self.current_record = None
        record_set = self.zone.resource_record_set(self.set_record_for_dns, 'A', 300, target_ips)
        changes.add_record_set(record_set)
        changes.create()
        while changes.status != 'done':
            LOGGER.debug("Waiting for google cloud dns to be in sync")
            time.sleep(1)
            changes.reload()
        self.load_current_record()
        self.observed_ips = target_ips
        self.last_observe_refresh = datetime.now()

    @property
    def set_record_for_dns(self):
        return "%s." % (self.set_record.strip('.'))

    @property
    def observed_set_ips(self):
        """
        Returns the observed set ips. This function uses a time based cache refreshing it automatically
        after some time.
        """
        if self.last_observe_refresh is None or self.last_observe_refresh < datetime.now() - timedelta(minutes=10):
            self.fetch_observed_ips()
        return self.observed_ips

    def fetch_observed_ips(self):
        self.observed_ips = self.current_set_ips
        self.last_observe_refresh = datetime.now()

    @property
    def current_set_ips(self):
        """
        Queries the server for the current dns records
        """
        return sorted(getattr(self.load_current_record(), 'rrdatas', []))

    def load_current_record(self):
        records = self.zone.list_resource_record_sets()
        for record in records:
            if record.record_type == "A" and record.name.strip('.') == self.set_record.strip('.'):
                self.current_record = record
                return record
        self.current_record = None
        return []

    @property
    def current_target_ips(self):
        """
        Returns the current ips of the target
        """
        answers = dns_resolver.query(self.observed_record, 'A')
        return sorted([str(answer) for answer in answers])


@click.command('cname_record_etter')
@click.option('--set-record', help='The fqdn which should be observed')
@click.option('--observed-record', help='The record which should be observerd to be set')
@click.option('--project-id', help='The project id of the google project where the adjustable dns records are in')
@click.option('--log-level', help='The log level for the logger', default='INFO')
def cname_record_setter(set_record, observed_record, project_id, log_level):
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    client = dns.Client(project=project_id)
    zone = get_zone(client, set_record)
    Observer(zone, set_record, observed_record).observe_loop()


if __name__ == '__main__':
    cname_record_setter(auto_envvar_prefix='CNAME_RECORD_SETTER')
