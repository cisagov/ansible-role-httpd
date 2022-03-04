#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

# This script is intended to set up the HTTP FreeIPA service on this
# host.  It creates the service if it does not already exist, then
# retrieves and saves the keytab.
#
# These variables must be set before client installation:
#
# hostname: The hostname of this IPA client (e.g. client.example.com).

USAGE=$(
  cat << END_OF_LINE
Set up the HTTP FreeIPA service on this host.

Usage:
  ${0##*/} [IPA-GROUP-ALLOWED-TO-CREATE-KEYTAB]
  ${0##*/} (-h | --help)

END_OF_LINE
)

# Parse command line arguments
if [ $# -eq 1 ]; then
  if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo "${USAGE}"
    exit 0
  else
    group_allowed_to_create_keytab=$1
  fi
elif [ $# -gt 1 ]; then
  echo "${USAGE}"
  exit 1
fi

# The file installed by cloud-init that contains the value for the
# above variables.
freeipa_vars_file=/var/lib/cloud/instance/freeipa-vars.sh

# Load above variable from a file installed by cloud-init:
if [[ -f "$freeipa_vars_file" ]]; then
  # Disable this warning since the file is only available at runtime
  # on the server.
  #
  # shellcheck disable=SC1090
  source "$freeipa_vars_file"
else
  echo "FreeIPA variables file does not exist: $freeipa_vars_file"
  echo "It should have been created by cloud-init at boot."
  exit 254
fi

# Get the default Ethernet interface
function get_interface {
  ip route | grep default | sed "s/^.* dev \([^ ]*\).*$/\1/"
}

# Get the IP address corresponding to an interface
function get_ip {
  ip --family inet address show dev "$1" \
    | grep --perl-regexp --only-matching 'inet \K[\d.]+'
}

# Create the HTTP/$hostname service if it does not already exist.
#
# Since the service may not be found, which returns an error code, we
# need to temporarily turn off errexit for this.
set +o errexit
# hostname is defined in the FreeIPA variables file that is sourced
# toward the top of this file.  Hence we can ignore the "undefined
# variable" warning from shellcheck.
#
# shellcheck disable=SC2154
ipa service-find --canonical-principal="HTTP/$hostname"
rc=$?
set -o errexit
if [[ $rc -ne 0 ]]; then
  ipa service-add "HTTP/$hostname"
  # Grab our IP address
  interface=$(get_interface)
  ip_address=$(get_ip "$interface")
  ip_address_dashes=${ip_address//./-}
  # Add an alias that is the PTR record as determined from the
  # Shared Services VPC.
  ipa service-add-principal "HTTP/$hostname" "HTTP/ip-${ip_address_dashes}.ec2.internal"
fi

# If an IPA-GROUP-ALLOWED-TO-CREATE-KEYTAB argument was provided,
# add that group to the service.
if [ $# -eq 1 ]; then
  ipa service-allow-create-keytab "HTTP/$hostname" --groups="$group_allowed_to_create_keytab"
fi

# Grab the keytab for the HTTP service and change its permissions so
# that the httpd process can read it.
ipa-getkeytab --quiet --keytab=/etc/krb5_http.keytab --principal="HTTP/$hostname"
chgrp www-data /etc/krb5_http.keytab
chmod g+r /etc/krb5_http.keytab

# Restart the httpd systemd service
systemctl restart apache2.service
