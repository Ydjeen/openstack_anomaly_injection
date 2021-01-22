from anomaly_injection.node_control.config import get_parser
from anomaly_injection.node_control.main import main

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if not args.target:
        parser.print_help()
    else:
        main(args)
