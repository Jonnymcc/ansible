import os
import json
from ec2inventory import Ec2Instance

CACHE_PATH = '%s/.ec2-instance-cache' % (os.environ['HOME'])
ALL_INSTANCES = {}

try:
    with open(CACHE_PATH, 'r') as fp:
        REGION_RESERVATIONS = json.load(fp)

    ALL_INSTANCES = [Ec2Instance(instance_dict)
                     for reservations in REGION_RESERVATIONS.itervalues()
                     for reservation in reservations
                     for instance_dict in reservation['instances']]
except IOError:
    pass


def lookup_instance_name(host):
    '''
    Looks up instances in ec2-instance-cache file created by NewsCred
    ec2inventory module.
    '''
    ec2_instance = filter(lambda i:
                          i.private_ip == host or
                          i.public_ip == host or
                          i.private_dns == host or
                          i.public_dns == host, ALL_INSTANCES)

    if ec2_instance:
        return '%s (%s)' % (host, ec2_instance[0].name)
    else:
        return host
