"""Module containing the generic tests for the default scenario.

These tests can be reused across scenarios.
"""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    if distribution in ["debian", "kali", "ubuntu"]:
        pkgs = ["apache2", "libapache2-mod-auth-gssapi", "libapache2-mod-authnz-pam"]
    elif distribution in ["amzn", "fedora", "redhat"]:
        pkgs = [
            "httpd",
            "mod_auth_gssapi",
            "mod_authnz_pam",
            "mod_proxy_html",
            "mod_session",
            "mod_ssl",
        ]
    else:
        raise ValueError(f"Unknown distribution {distribution}")

    for pkg in pkgs:
        assert host.package(pkg).is_installed, f"System package {pkg} not installed"


@pytest.mark.parametrize("f", ["/usr/local/sbin/01_setup_http_service.sh"])
def test_files(host, f):
    """Test that the expected files were installed."""
    assert host.file(f).exists, f"File {f} does not exist"
    assert host.file(f).is_file, f"{f} is not a file"
    assert host.file(f).user == "root", f"File {f} does not have user root"
    assert host.file(f).group == "root", f"File {f} does not have group root"
    assert host.file(f).mode == 0o500, f"File {f} does not have mode 0o500"
