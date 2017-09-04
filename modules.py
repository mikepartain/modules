from ciscoconfparse import *

def get_hostname(host):
    parse = CiscoConfParse(host)
    hostnames = parse.find_lines('^hostname ')
    for hostname in hostnames:
        hostname = hostname.split(' ',-1)[1]
        return hostname

def get_loopback(host):
    interface_list = []
    parse = CiscoConfParse(host)
    interfaces = parse.find_lines('^interface Loopback')
    for interface in interfaces:
        if interface not in interface_list:
            interface_list.append(interface.split(' ', -1)[1])
    return interface_list

def get_int_ip(host):
    interface_list = []
    parse = CiscoConfParse(host)
    interfaces = parse.find_parents_w_child('^interface', 'ip address')
    for interface in interfaces:
        if interface not in interface_list:
            interface_list.append(interface.split(' ',-1)[1])
    return interface_list

def get_shut_int(host):
    interface_list = []
    parse = CiscoConfParse(host)
    interfaces = parse.find_parents_w_child('^interface', '^ shutdown$')
    for interface in interfaces:
        if interface not in interface_list:
            interface_list.append(interface.split(' ', -1)[1])
    return interface_list

def active_int(host):
    interface_list = []
    parse = CiscoConfParse(host)
    interfaces = parse.find_parents_wo_child('^interface', '^ shutdown$')
    for interface in interfaces:
        if interface not in interface_list:
            interface_list.append(interface.split(' ', -1)[1])
    return interface_list

def get_dot1q(host):
    interface_list = []
    parse = CiscoConfParse(host)
    interfaces = parse.find_parents_w_child('^interface', '^ encapsulation dot1Q')
    for interface in interfaces:
        if interface not in interface_list:
            interface_list.append(interface.split(' ', -1)[1])
    return interface_list

def get_ospf_process(host):
    router = []
    parse = CiscoConfParse(host)
    ipv4_router_process = parse.find_lines('^router ospf')
    for process in ipv4_router_process:
        process = process.split(' ',-1)[2]
        if process not in router:
            router.append(process)
    return router

def get_eigrp_process(host):
    router = []
    parse = CiscoConfParse(host)
    ipv4_router_process = parse.find_lines('^router eigrp')
    for process in ipv4_router_process:
        process = process.split(' ',-1)[2]
        if process not in router:
            router.append(process)
    return router

def get_bgp_process(host):
    router = []
    parse = CiscoConfParse(host)
    ipv4_router_process = parse.find_lines('^router bgp')
    for process in ipv4_router_process:
        process = process.split(' ',-1)[2]
        if process not in router:
            router.append(process)
    return router

def get_ospf_passive_default(host):
    parse = CiscoConfParse(host)
    passive = []
    for process in get_ospf_process(host):
        # print process
        passive_enabled = parse.find_parents_w_child('^router ospf '+process+'$', 'passive-interface default')
        for pass_process in passive_enabled:
            # print 'PASSIVE:' , passive_enabled
            if pass_process not in passive:
                passive.append(pass_process)
    if passive:
        return passive
    else:
        return 'False'

def get_eigrp_passive_default(host):
    parse = CiscoConfParse(host)
    passive = []
    for process in get_eigrp_process(host):
        # print process
        passive_enabled = parse.find_parents_w_child('^router eigrp '+process+'$', 'passive-interface default')
        for pass_process in passive_enabled:
            # print 'PASSIVE:' , passive_enabled
            if pass_process not in passive:
                passive.append(pass_process)
    if passive:
        return passive
    else:
        return 'False'

def device_type(host):
    parse = CiscoConfParse(host)
    # Cisco Specifics
    is_cisco = parse.find_lines('^version ')
    is_bgp = parse.find_lines('^router bgp')
    is_ospf = parse.find_lines('^router ospf')
    is_eigrp = parse.find_lines('^router eigrp')
    is_cisco_router = parse.find_lines('boot system flash:')
    is_vlan = parse.find_lines('^interface Vlan')  # Check for interface Vlans, these will be counted later
    is_vtp = parse.find_lines('^vtp mode')
    is_cer = parse.find_lines('^hostname.*CER')
    interfaces = parse.find_lines('^ ip address')  # Check for IP addresses, these will be counted later
    nxos_interfaces = parse.find_lines('^  ip address')  # Check for IP addresses, these will be counted later
    is_router = parse.find_lines('^interface Embedded-Service-Engine0/0')
    is_isr = parse.find_lines('^license udi')
    is_isr2 = parse.find_lines('^boot system flash:c')
    is_voice = parse.find_lines('^voice service')
    is_vg224 = parse.find_lines('^boot system?.*:vg')
    is_asr = parse.find_lines('flash.*asr')
    is_nexus = parse.find_lines('^feature')
    is_5k = parse.find_lines('^boot system?.*n5000')
    is_7k = parse.find_lines('^boot system?.*n7000')
    is_vpn = parse.find_lines('^crypto keyring')

    #Brocade Specifics
    is_brocade = parse.find_lines('^ver ')
    is_l2_brocade = parse.find_lines('^ip address')  # If device has lines starting with IP it is a L2 Manual
    is_l3_brocade = parse.find_lines('^vlan')  # If device has lines starting with vlan, L3 Manual
    b_l2_switch = parse.find_lines('^ip address')  # If device has lines starting with IP it is a L2 Manual
    b_l3_switch = parse.find_lines('^vlan')  # If device has lines starting with vlan, L3 Manual
    is_adx = parse.find_lines('^server cache')

    # Is Junos
    is_junos = parse.find_lines('root-authentication {')

    # print len(interfaces)

    if is_cisco:
        VENDOR = 'Cisco'
        if is_vlan and is_vtp:
            if len(interfaces)>1:
                TYPE = 'L3 Switch'
            else:
                TYPE = 'L2 Switch'
            # print 'Switch'
        elif is_router or is_isr or is_isr2 or is_asr:
            if is_vpn and is_eigrp:
                TYPE = 'VPN'
            else:
                TYPE = 'Router'

        elif is_nexus:
            TYPE = 'NEXUS'

        return (VENDOR, TYPE)


    elif is_brocade:
        VENDOR = 'Brocade'
        if b_l2_switch:
            TYPE = 'L2 Switch'
        elif is_adx:
            TYPE = 'LoadBalancer'
        return VENDOR, TYPE

def get_interface_acls(host):
    interface_list = []
    parse = CiscoConfParse(host)
    interfaces = parse.find_parents_w_child('^interface', 'access-group')
    for interface in interfaces:
        acls = parse.find_children_w_parents(interface, 'access-group')
        for acl in acls:
            acl_int = (interface, acl)

        if interface not in interface_list:
            interface_list.append(acl_int)
    return interface_list

def get_applied_acls(host):
    acl ={}
    interface_list = get_interface_acls(host)
    parse = CiscoConfParse(host)
    for interface in interface_list:
        acls = parse.find_children_w_parents(interface, 'access-group')
        for line in acls:
            line = line.split(' ',4)[3]

            acl.update({interface:line})
    return acl
    #     if interface not in interface_list:
    #         interface_list.append(interface.split(' ', -1)[1])
    # return interface_list

def get_acl(host, acl):
    parse = CiscoConfParse(host)
    acl_config = parse.find_all_children(r'access-list.*'+acl)
    return acl_config

def get_acl_without_deny_any(host):
    parse = CiscoConfParse(host)
    bad_extended_acls = parse.find_parents_wo_child('^ip access-list extended', 'deny any any log')
    bad_standard_acls = parse.find_parents_wo_child('^ip access-list standard', 'deny.*any log')
    bad_acls = bad_extended_acls + bad_standard_acls
    return bad_acls

def get_services(host):
    parse = CiscoConfParse(host)
    services = parse.find_lines('^service ')
    return services

def count_ntp_servers(host):
    parse = CiscoConfParse(host)
    ntp_servers = parse.find_lines('^ntp server')
    return len(ntp_servers)

def count_users(host):
    parse = CiscoConfParse(host)
    ntp_servers = parse.find_lines('^username ')
    return len(ntp_servers)

def get_users(host):
    parse = CiscoConfParse(host)
    users = parse.find_lines('^username ')
    return users

def get_bgp_neighbors(host):
    parse = CiscoConfParse(host)
    BGP_NEIGH = parse.find_children_w_parents('^router bgp', ' neighbor [1-9].*activate')
    BGP_PEER = parse.find_children_w_parents('^router bgp', ' neighbor.*peer-group')
    bgp_neighbors = BGP_NEIGH + BGP_PEER
    return bgp_neighbors

def get_bgp_address_families(host):
    parse = CiscoConfParse(host)
    address_families = parse.find_children_w_parents('^router bgp', 'address-family ipv4 vrf')
    return address_families

def get_bgp_af_neighbors(host, af):
    BGP_NEIGHBORS = []
    parse = CiscoConfParse(host)
    # BGP_NEIGH = parse.find_children_w_parents(af, ' neighbor [1-9].*activate')
    BGP_NEIGH = parse.find_children_w_parents(af, ' neighbor [1-9].*activate')
    for NEIGHBOR in BGP_NEIGH:
        # print NEIGHBOR
        if 'peer-group' not in NEIGHBOR:
            BGP_NEIGHBORS.append(NEIGHBOR)
    BGP_PEER = parse.find_children_w_parents(af, ' neighbor.*peer-group')
    bgp_neighbors = BGP_NEIGH + BGP_PEER
    return bgp_neighbors

def get_unauth_bgp_peers(host, neighbor):
    parse = CiscoConfParse(host)

def check_for_service(host, service):
    parse = CiscoConfParse(host)
    service = parse.find_lines('^service.*'+service)
    return service





