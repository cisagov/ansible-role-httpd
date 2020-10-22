# ansible-role-httpd #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-httpd/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-httpd/actions)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/ansible-role-httpd.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-httpd/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/ansible-role-httpd.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-httpd/context:python)

This is an Ansible role that installs [Apache
httpd](https://httpd.apache.org/), along with the
[mod_auth_gssapi](https://github.com/gssapi/mod_auth_gssapi) and
[mod_authnz_pam](https://github.com/adelton/mod_authnz_pam) modules.
This lays the base for an Apache httpd server suitable for
authentication against
[Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol)) via
GSSAPI and authorization via
[PAM](https://en.wikipedia.org/wiki/Linux_PAM).

This is ideal for a web server in [the
COOL](https://github.com/cisagov/cool-system) that wishes to
authenticate users via Kerberos and authorize users via
[`pam_sss`](https://linux.die.net/man/8/pam_sss) against
[FreeIPA](https://www.freeipa.org/page/Main_Page)'s HBAC (host-based
access control) rules.

## Requirements ##

None.

## Role Variables ##

None.

## Dependencies ##

None.

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: web
  become: yes
  become_method: sudo
  roles:
    - httpd
```

## New Repositories from a Skeleton ##

Please see our [Project Setup guide](https://github.com/cisagov/development-guide/tree/develop/project_setup)
for step-by-step instructions on how to start a new repository from
a skeleton. This will save you time and effort when configuring a
new repository!

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Shane Frasier - <jeremy.frasier@trio.dhs.gov>
