# Ansible Role: aiidalab.aiidalab_server

An Ansible role that deploys a multi-user [AiiDAlab](aiidalab.materialscloud.org) server on Ubuntu.

## Installation

`ansible-galaxy install git+https://github.com/aiidalab/ansible-role-aiidalab-server.git,v0.4.0`

## Role Variables

See `defaults/main.yml`.

Configure which docker image to use, resource limits, and more.
## Example Playbook

```yaml
- hosts: servers
  roles:
  - role: aiidalab.aiidalab_server
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
