"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "pkg", ["apache2", "libapache2-mod-auth-gssapi", "libapache2-mod-authnz-pam"]
)
def test_debian_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    if (
        host.system_info.distribution == "debian"
        or host.system_info.distribution == "ubuntu"
        or host.system_info.distribution == "kali"
    ):
        assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["httpd", "mod_auth_gssapi", "mod_authnz_pam"])
def test_redhat_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    if (
        host.system_info.distribution == "redhat"
        or host.system_info.distribution == "fedora"
        or host.system_info.distribution == "amzn"
    ):
        assert host.package(pkg).is_installed


def test_services(host):
    """Test that the expected services were enabled."""
    service = None
    if (
        host.system_info.distribution == "debian"
        or host.system_info.distribution == "ubuntu"
        or host.system_info.distribution == "kali"
    ):
        service = "apache2"
    elif (
        host.system_info.distribution == "redhat"
        or host.system_info.distribution == "fedora"
        or host.system_info.distribution == "amzn"
    ):
        service = "httpd"

    assert host.service(service).is_enabled
