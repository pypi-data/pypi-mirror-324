# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import argparse
import os
import sys

# Internal Imports
# Import only with "from x import y", to simplify the code.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from .products.firewall import backup as firewall_backup
from .utils.utils import error

#PRODUCTS = ["firewall", "linode"]
PRODUCTS = ["firewall"]


def backup() -> None:
    """"Backup objects to local or Linode Object Storage."""
    if args.storage is None:
        storage = os.getcwd()
    else:
        storage = args.storage
    for product in args.products:
        eval(f"{product}_backup(storage='{storage}')")


if "LINODE_TOKEN" in os.environ:
    token = os.environ["LINODE_TOKEN"]
else:
    error(code=1, text="Environment variable LINODE_TOKEN not setup")
parser = argparse.ArgumentParser()
parser.add_argument("--storage", type=str,
                    help="storage to save the data.")
parser.add_argument("--products", choices=PRODUCTS, nargs="+", default=PRODUCTS,
                    help="products to backup.")
args = parser.parse_args()

def main() -> None:
    backup()

if __name__=="__main__":
    main()
