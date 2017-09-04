from modules import *
host = ('../configs/r2')
print get_hostname(host)

# print 'LOOPBACKS: '.ljust(20),get_loopback(host)
# print 'IP INT: '.ljust(20),get_int_ip(host)
# print 'SHUT INT: '.ljust(20),get_shut_int(host)
# print 'ACTIVE INT: '.ljust(20),active_int(host)
# print 'DOT1Q ROUTER INT: '.ljust(20),get_dot1q(host)
# print 'OSPF PROCESS: '.ljust(20),get_ospf_process(host)
# print 'EIGRP PROCESS: '.ljust(20),get_eigrp_process(host)
# print 'BGP PROCESS: '.ljust(20),get_bgp_process(host)
# print 'OSPF PASSIVE: '.ljust(20),get_ospf_passive_default(host)
# print 'EIGRP PASSIVE: '.ljust(20),get_eigrp_passive_default(host)
# print host, device_type(host)

# for device in os.listdir('../configs/'):
#     host = '../configs/'+device
#     # print device, host
#     print device, device_type(host)

for int, acl in get_interface_acls(host):
    print int+','+ acl


# print get_interface_acls(host)

# for key,val in get_applied_acls(host).iteritems():
#     # print get_hostname(host).ljust(20), key.ljust(30), val
#     print key.ljust(30), val

#
# # Get an ACL from device
# for line in  get_acl(host, 'VPN_TUNNEL'):
#     print line

# for acl in get_acl_without_deny_any(host):
#     print acl

# print get_acl_without_deny_any(host)

# print get_services(host)
#
# for device in os.listdir('../configs/'):
#     host = '../configs/'+device
#     # print device
#     # print get_services(host)
#     for line in get_services(host):
#         if 'call' in line:
#             print get_hostname(host),device_type(host)[1],' is configured for call-home.'
#
# print count_ntp_servers(host)
#
# print device_type(host)[1]
#
#
# if device_type(host)[1] == 'NEXUS':
#     print 'We found a NXOS'

# print check_for_service(host, 'keepalives')

# print check_for_service(host, 'dhcp')

# print count_users(host)

# Check for more than one user configured.  If two then print them out.
# if count_users(host) > 1:
#     print device_type(host)
#     if device_type(host)[1] == "NEXUS":
#         for user in get_users(host):
#             print user
#     else:
#         for user in get_users(host):
#             print user

# print '\nBGP NEIGHBORS'
# print get_bgp_neighbors(host)
#
# print '\nBGP Address Families'
# print get_bgp_address_families(host)

# print '\nBGP AF NEIGHBORS'
# print get_bgp_af_neighbors(host, 'AFR')
# if get_bgp_address_families(host):
#     for af in get_bgp_address_families(host):
#         neighbors = get_bgp_af_neighbors(host, af)
#         for neighbor in neighbors:
#             if neighbor.endswith('peer-group'):
#                 neighbor = neighbor.rsplit(' ',1)[0]
#                 print neighbor
#             elif 'peer-group' in neighbor:
#                 neighbor = neighbor.rsplit(' ',2)[0]
#             else:
#                 neighbor = neighbor.rsplit(' ',1)[0]
#                 print neighbor
#
#         neighbor = neighbor.split()




# for af in get_bgp_address_families(host):
#     bgp_neigh = get_bgp_af_neighbors(host, ' address-family ipv4 vrf AFR')
#     # print af.strip()
#     for each in bgp_neigh:
#         print each
#     # print bgp_neigh

# for neighbor in get_bgp_af_neighbors(host, ' address-family ipv4 vrf EUR'):
#     print neighbor
