import argparse
from services.policy_service import PolicyService

policy_service = PolicyService()
    def process_file(incoming_path: str, output_path: str):
        incoming_policies = policy_service.read_ascii_policies_from_file(incoming_path)
        policy_service.write_ascii_policies_to_file(output_path, incoming_policies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--workspace', metavar='path', required=True,
                        help='the path to workspace')
    parser.add_argument('--schema', metavar='path', required=True,
                        help='path to schema')
    parser.add_argument('--dem', metavar='path', required=True,
                        help='path to dem')
    args = parser.parse_args()
    model_schema(workspace=args.workspace, schema=args.schema, dem=args.dem)