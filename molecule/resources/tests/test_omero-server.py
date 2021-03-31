import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('omero-server')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'


def test_services_running_and_enabled(host):
    service = host.service('omero-server')
    assert service.is_running
    assert service.is_enabled


def test_postgres_not_installed(host):
    if host.system_info.distribution == 'ubuntu':
        service = host.service('postgresql@11-main')
    else:
        service = host.service('postgresql-11')
    assert not service.is_running
    assert not service.is_enabled


def test_omero_login(host, monkeypatch):
    # Ubuntu sudo doesn't set HOME so it tries to write to /root
    from time import time
    env = 'OMERO_USERDIR=/tmp/omero-{}'.format(time())
    with host.sudo('omero-server'):
        host.check_output(
            '%s %s login -C -s localhost -u root -w omero' % (env, OMERO))
