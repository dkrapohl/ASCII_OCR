import argparse, os
from services.policy_service import PolicyService

policy_service = PolicyService()


def process_file(incoming_path: str, output_path: str):
    # ensure the input file and the output directory exist
    if not os.path.isfile(incoming_path):
        print("Input file path does not exist: {0}".format(incoming_path))

    incoming_policies = policy_service.read_ascii_policies_from_file(incoming_path)
    policy_service.write_numeric_policies_to_file_with_validity(output_path, incoming_policies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse a file of ASCII policy numbers and output them as normal text with corrections')
    parser.add_argument('--in_path', metavar='path', required=True,
                        help='the full path to the input file including directory')
    parser.add_argument('--out_path', metavar='path', required=True,
                        help='the full path to the output file including directory')
    args = parser.parse_args()
    process_file(incoming_path=args.in_path, output_path=args.out_path)
