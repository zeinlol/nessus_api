import argparse


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, help='address [url: http://donki.xyz/ or domain: donki.xyz]')
    parser.add_argument('-u', '--username', type=str, help='Nessus user name')
    parser.add_argument('-p', '--password', type=str, help='Nessus user password')
    parser.add_argument('-ht', '--host', type=str, default='localhost', help='Nessus API host')
    parser.add_argument('-pt', '--port', type=int, default=8834, help='Nessus API port')
    parser.add_argument('-o', '--output-file', type=str, default='/wd/report.json', help='Output file')
    parser.add_argument('-s', '--secure', type=bool, default=False, help='Session is secure')
    parser.add_argument('-px', '--proxy', required=False, type=str, help='Proxy settings')
    return parser.parse_args()


CLI_ARGUMENTS = init_args()
