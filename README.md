# ec2_group_conversion

ec2_group_conversion is an ansible module that it tries to convert ec2_group_facts output to ec2_group input. Its mission is to maintain security group inbound rules when you use ec2_group ansible module.

At the global level, ec2_group_conversion functional steps are:

  - Receive ec2_group_facts output from a security group
  - Transform this dictionary in an ec2_group rules input array
  - Export the array to inbound_rules variable
  
# Module Example
```
- ec2_group_conversion:
    security_group: [{"description":"Connectivity rule for BSC-SG-D-EW1-ALL-T1-ZZ1","group_id":"sg-511d792c","group_name":"BSC-SG-D-EW1-ALL-T1-ZZ1","ip_permissions":[{"from_port":23,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[{"cidr_ipv6":"::/0"}],"prefix_list_ids":[],"to_port":23,"user_id_group_pairs":[]},{"from_port":222,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":222,"user_id_group_pairs":[]},{"from_port":53,"ip_protocol":"udp","ip_ranges":[],"ipv6_ranges":[{"cidr_ipv6":"::/0"}],"prefix_list_ids":[],"to_port":53,"user_id_group_pairs":[]},{"from_port":2242,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":2242,"user_id_group_pairs":[]},{"from_port":0,"ip_protocol":"tcp","ip_ranges":[],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":0,"user_id_group_pairs":[{"group_id":"sg-4b723f36","user_id":"2342343542342345"}]},{"from_port":123,"ip_protocol":"tcp","ip_ranges":[{"cidr_ip":"10.219.0.0/32"}],"ipv6_ranges":[],"prefix_list_ids":[],"to_port":123,"user_id_group_pairs":[]}],"ip_permissions_egress":[{"ip_protocol":"-1","ip_ranges":[{"cidr_ip":"0.0.0.0/0"}],"ipv6_ranges":[],"prefix_list_ids":[],"user_id_group_pairs":[]}],"owner_id":"266912643964","tags":{"Name":"BSC-SG-D-EW1-ALL-T1-ZZ1"},"vpc_id":"vpc-dd60a2ba"}]
```

# Use of case Example
```
- name: List {{ tag }} security group properties
  ec2_group_facts:
    aws_access_key: "{{ key }}"
    aws_secret_key: "{{ secret }}"
    region: "{{ region }}"
    validate_certs: no
    filters:
      "tag:Name": "{{ tag }}"
  register: output

- name: Conversion {{ tag }} security group rules to make an rules array
  ec2_group_conversion:
    security_group: '{{ output.security_groups }}'
  register: security_group

- name: Upate {{ tag }} security group
  ec2_group:
    state: present
    name: "{{ tag }}"
    tags:
      Name: "{{ tag }}"
    description: "{{ desc }}"
    aws_access_key: "{{ key }}"
    aws_secret_key: "{{ secret }}"
    vpc_id: "{{ vpc }}"
    region: "{{ region }}"
    rules: "{{ rules + security_group.inbound_rules }}"
    validate_certs: no
```
