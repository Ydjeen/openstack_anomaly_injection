from anomaly_injection.node_control.config import get_parser
from anomaly_injection.node_control.main import main

parser = get_parser()
args = parser.parse_args()
if not args.target:
    parser.print_help()
else:
    main(args)
