# Salt win_ossec Module

_A module to make managing OSSEC on windows minions less painful._

The main feature of this module is support for `ossec-authd` automatic enrollment for windows clients, something that is [not currently supported](https://github.com/ossec/ossec-hids/pull/181) by the standard OSSEC distribution. By the looks of it, this won't be supported in 2.9 either.

Using this module, combined with the ossec package installer in the [win_repo](), completely salt-managed installation and enrollment is possible. Whether you are automatically provisioning 10 or 1000 systems, this is a huge win.

# Usage Examples

## Module functions

Below are a few examples of how to use the module functions. Odds are, you won't want to use these directly and you'll want to use the state instead. See the Example SLS below.

```
# Will attempt to automatically enroll the minion to the server at 10.0.0.1
# and stores the resulting key line in C:\Program Files (x86)\ossec-agent\client.keys
salt <windows-minion> win_ossec.authd_enroll 10.0.1.1

# Returns the minion's ossec agent id
salt <windows-minion> win_ossec.get_agent_id
```

## Example sls

The example state below ensures ossec is installed, registered with the server, and running.

```
ossec-agent:
  pkg.installed:
    - version: '2.8'

'{{ salt['pillar.get']("ossec_server_ip") }}':
  win_ossec.autoenrolled:
    - name: '{{ salt['pillar.get']("ossec_server_ip") }}'
  require:
    - pkg: ossec-agent

'C:\\Program Files (x86)\\ossec-agent\ossec.conf':
  require:
    - pkg: ossec-agent
  file.managed:
    - source: salt://path-to-your-template-config/ossec.conf
    - template: jinja
    - context:
        ossec_server: {{ salt['pillar.get']("ossec_server_ip") }}

OssecSvc:
  require:
    - pkg: ossec-agent
    - win_ossec: '{{ salt['pillar.get']("ossec_server_ip") }}'
    - file: 'C:\\Program Files (x86)\\ossec-agent\ossec.conf'
  service.running:
    - enable: True
    - watch:
      - file: 'C:\\Program Files (x86)\\ossec-agent\ossec.conf'
      - win_ossec: '{{ salt['pillar.get']("ossec_server_ip") }}'
```

This example state assumes:

1. You have a template ossec.conf where at least the server ip is set in the template using the jinja `ossec_server` variable. That file must be in the path specified in the place holder `salt://path-to-your-template-config/ossec.conf`
2. The minion has the ossec server's IP in it's pillar data under `ossec_server_ip`.

> That's actually it. Just run the state and you're off to the races.

# How it works

## ossec-authd enrollment

This module provides a functional replacement for `agent_auth` via the `authd_enroll` function. Since ossec-authd's exchange requirements are dead simple, this was a very easy task.
