[![Build Status](https://travis-ci.org/marvel-nccr/ansible-role-aiidalab-server.svg?branch=master)](https://travis-ci.org/marvel-nccr/ansible-role-aiidalab-server)

# Ansible Role: marvel-nccr.aiidalab_server

An Ansible role that deploys a multi-user [AiiDAlab](aiidalab.materialscloud.org) server on Ubuntu.

## Installation

`ansible-galaxy install marvel-nccr.aiidalab_server`

## Role Variables

See `defaults/main.yml`.

Configure which docker image to use, resource limits, and more.
## Example Playbook

```yaml
- hosts: servers
  roles:
  - role: marvel-nccr.aiidalab_server
```

## Tests

This role uses [Molecule](https://molecule.readthedocs.io/en/latest/#) and
Docker for tests. Once Docker is installed, run tests using

```bash
pip install -r requirements.txt
molecule test
```

## License

MIT

## Contact

Please direct inquiries regarding Quantum Mobile and associated ansible roles to the [AiiDA mailinglist](http://www.aiida.net/mailing-list/).
