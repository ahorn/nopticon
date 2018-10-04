#!/usr/bin/python3

"""
List edges contained in a network summary
"""

from argparse import ArgumentParser
import ipaddress
import json
from nopticon import NetworkSummary

def check_reachability(policy, summary):
    assert(policy['type'] == 'reachability')
    flow = ipaddress.ip_network(policy['flow'])
    edge = (policy['source'], policy['target'])
    if flow not in summary.get_edges():
        return -1
    if edge not in summary.get_edges()[flow]:
        return -1
    edge_details = summary.get_edges()[flow][edge]
    return edge_details['rank-0']

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='List edges contained in a network summary')
    arg_parser.add_argument('-summary', dest='summary_path', action='store',
            required=True, help='Path to summary JSON file')
    arg_parser.add_argument('-policies', dest='policies_path', action='store',
            required=True, help='Path to policies JSON file')
    settings = arg_parser.parse_args()

    # Load summary
    with open(settings.summary_path, 'r') as sf:
        summary_json = sf.read()
    summary = NetworkSummary(summary_json)

    # Load policies
    with open(settings.policies_path, 'r') as pf:
        policies_json = pf.read()
    policies = json.loads(policies_json)

    for policy in policies['policies']:
        if policy['type'] == 'reachability':
            print('%s %s->%s %f' % (policy['flow'], policy['source'], policy['target'], check_reachability(policy, summary)))

if __name__ == '__main__':
    main()
