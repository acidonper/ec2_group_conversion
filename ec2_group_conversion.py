#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import json

DOCUMENTATION = """
---
module: ec2_group_conversion
short_description: Transform ec2_group_facts output to ec2_group input
description:
  - Receive ec2_group_facts output from a security group
  - Transform this dictionary in an ec2_group rules input array
  - Export the array to inbound_rules variable
version_added: "0.1"
author: Asier Cidon Perianez
notes:
  - First version
options:
  security_group:
    description:
      - ec2_group_facts output
    required: true
    type: array
"""

EXAMPLES = """
# Compare current a correct file to find differences
- ec2_group_conversion:
    security_group: [{"description":"Connectivity rule for BSC-SG-D-EW1-ALL-T1-ZZ1","group_id":"sg-511d792c","group_name":"BSC-SG-D-EW1-ALL-T1-ZZ1","ip_permissions":[{"from_port":23,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[{"cidr_ipv6":"::/0"}],"prefix_list_ids":[],"to_port":23,"user_id_group_pairs":[]},{"from_port":222,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":222,"user_id_group_pairs":[]},{"from_port":53,"ip_protocol":"udp","ip_ranges":[],"ipv6_ranges":[{"cidr_ipv6":"::/0"}],"prefix_list_ids":[],"to_port":53,"user_id_group_pairs":[]},{"from_port":2242,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":2242,"user_id_group_pairs":[]},{"from_port":0,"ip_protocol":"tcp","ip_ranges":[],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":0,"user_id_group_pairs":[{"group_id":"sg-4b723f36","user_id":"266912643964"}]},{"from_port":123,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"10.219.0.0/32"}],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":123,"user_id_group_pairs":[]}],"ip_permissions_egress":[{"ip_protocol":"-1","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[],"prefix_list_ids":[],"user_id_group_pairs":[]}],"owner_id":"266912643964","tags":{"Name":"BSC-SG-D-EW1-ALL-T1-ZZ1"},"vpc_id":"vpc-dd60a2ba"}]
"""

def main():

    module = AnsibleModule(
        argument_spec = dict(
            security_group     = dict(required=True, type='list')
        ),
        supports_check_mode=True
    )


    security_group = module.params['security_group']
    security_groups = []

    if not security_group:
        module.fail_json(msg="security_group rules array is empty")

    for i in security_group[0]:

        if i == 'ip_permissions':

            for x in security_group[0][i]:

                if not x['user_id_group_pairs']:

                    if x['ip_ranges']:
                        rule = {'to_port': x['to_port'], 'from_port': x['from_port'], 'proto': x['ip_protocol'],  'cidr_ip': x['ip_ranges'][0]['cidr_ip']}
                        security_groups.append(rule)

                    if x['ipv6_ranges']:
                        rule = {'to_port': x['to_port'], 'from_port': x['from_port'], 'proto': x['ip_protocol'],  'cidr_ipv6': x['ipv6_ranges'][0]['cidr_ipv6']}
                        security_groups.append(rule)

                elif x['user_id_group_pairs']:
                    rule = {'to_port': x['to_port'], 'from_port': x['from_port'], 'proto': x['ip_protocol'],  'group_id': x['user_id_group_pairs'][0]['group_id']}
                    security_groups.append(rule)

    module.exit_json(inbound_rules=security_groups)


if __name__ == '__main__':
    main()
