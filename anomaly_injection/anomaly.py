from anomaly_injection.config import get_parser
from anomaly_injection.main import main

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if not args.target:
        parser.print_help()
    else:
        main(args)
