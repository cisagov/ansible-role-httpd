"""Module containing tests specific to the service_disabled scenario.

These tests cannot be used across scenarios.
"""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_services(host):
    """Test that the expected services were disabled."""
    distribution = host.system_info.distribution
    service = None
    if distribution in ["debian", "kali", "ubuntu"]:
        service = "apache2"
    elif distribution in ["amzn", "fedora", "redhat"]:
        service = "httpd"
    else:
        raise ValueError(f"Unknown distribution {distribution}")

    assert not host.service(service).is_enabled, f"Service {service} is enabled"
