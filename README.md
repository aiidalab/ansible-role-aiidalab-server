[![Build Status](https://travis-ci.org/marvel-nccr/ansible-role-aiidalab-server.svg?branch=master)](https://travis-ci.org/marvel-nccr/ansible-role-aiidalab-server)

# Ansible Role: marvel-nccr.aiidalab_server

An Ansible role that deploys a multi-user [AiiDA lab](aiidalab.materialscloud.org) server on Ubuntu.

## Installation

`ansible-galaxy install marvel-nccr.aiidalab_server`

Note: By default, JupyterHub will use the `aiidalab-docker-stack:latest` image.
Don't forget to tag the image accordingly after pulling the latest version from Dockerhub:

```
docker pull aiidalab/aiidalab-docker-stack:latest
docker tag aiidalab/aiidalab-docker-stack:latest aiidalab-docker-stack:latest
```

## Role Variables

See `defaults/main.yml`

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
