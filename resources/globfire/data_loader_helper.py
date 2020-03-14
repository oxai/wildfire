import numpy as np
from resources.gee.download_fires import get_parser
from resources.gee.methods import get_ee_product


def get_arguments():
    parser = get_parser(globfire=True)
    args = parser.parse_args()

    ee_product = get_ee_product(
        platform=args.platform,
        sensor=args.sensor,
        product=args.product
    )

    zoom = args.zoom if args.zoom else 13

    subdir = args.subdir
    if not subdir:
        dir_name_base = f"{args.platform}-{args.sensor}_{args.product}_globfire_" \
                        f"{args.from_date}_{args.until_date}_{zoom}"
        subdir = dir_name_base + ("_no_fire" if args.neg else "_w_fire")

    return args, ee_product, subdir, zoom
