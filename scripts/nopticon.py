"""
Python classes for Nopticon 
"""

from enum import Enum
import ipaddress
import json

class ReachSummary:
    def __init__(self, summary_json):
        self._summary = json.loads(summary_json)

        # Extract edges
        self._edges = {}
        for flow in self._summary['reach-summary']:
            flow_prefix = ipaddress.ip_network(flow['flow'])
            flow_edges = {}
            for edge_details in flow['edges']:
                edge = (edge_details['source'], edge_details['target'])
                flow_edges[edge] = edge_details
            self._edges[flow_prefix] = flow_edges

    def get_edges(self, flow):
        if flow not in self._edges:
            return {}
        return self._edges[flow]

class CommandType(Enum):
    PRINT_LOG = 0
    RESET_NETWORK_SUMMARY = 1
    REFRESH_NETWORK_SUMMARY = 2

class Command():
    def __init__(self, cmd_type):
        self._type = cmd_type

    def json(self):
        cmd = {'Command' : {'Opcode' : self._type.value}}
        if self._type == CommandType.REFRESH_NETWORK_SUMMARY:
            cmd['Command']['Timestamp'] = self._timestamp
        return json.dumps(cmd)

    @classmethod
    def print_log(cls):
        return cls(CommandType.PRINT_LOG)

    @classmethod
    def reset_summary(cls):
        return cls(CommandType.RESET_NETWORK_SUMMARY)

    @classmethod
    def refresh_summary(cls, timestamp):
        obj = cls(CommandType.REFRESH_NETWORK_SUMMARY)
        obj._timestamp = timestamp
        return obj

"""Convert policies JSON to a list of Policy objects"""
def parse_policies(policies_json):
    policies_dict = json.loads(policies_json)
    policies = []
    for policy_dict in policies_dict['policies']:
        if policy_dict['type'] == PolicyType.REACHABILITY.value:
            policies.append(ReachabilityPolicy(policy_dict))
        elif policy_dict['type'] == PolicyType.PATH_PREFERENCE.value:
            policies.append(PathPreferencePolicy(policy_dict))
    return policies

class PolicyType(Enum):
    REACHABILITY = "reachability"
    PATH_PREFERENCE = "path-preference"

class Policy:
    def __init__(self, typ, policy_dict):
        self._type = typ
        self._flow = ipaddress.ip_network(policy_dict['flow'])

    def isType(self, typ):
        return self._type == typ

class ReachabilityPolicy(Policy):
    def __init__(self, policy_dict):
        super().__init__(PolicyType.REACHABILITY, policy_dict)
        self._source = policy_dict['source'][:10]
        self._target = policy_dict['target'][:10]

    def __str__(self):
        return '%s %s->%s' % (self._flow, self._source, self._target)

class PathPreferencePolicy(Policy):
    def __init__(self, policy_dict):
        super().__init__(PolicyType.PATH_PREFERENCE, policy_dict)
        self._paths = policy_dict['paths']
        for path in self._paths:
            for i in range(0, len(path)):
                path[i] = path[i][:10]

    def __str__(self):
        return '%s %s' % (self._flow, 
                ' > '.join(['->'.join(path) for path in self._paths]))

"""Convert rdns JSON to a dictionary of IPs to router names"""
def parse_rdns(rdns_json):
    routers_dict = json.loads(rdns_json)
    rdns = {}
    for router_dict in routers_dict['routers']:
        name = router_dict['name']
        for iface_ip in router_dict['ifaces']:
            rdns[ipaddress.ip_address(iface_ip)] = name
    return rdns

