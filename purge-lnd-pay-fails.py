import argparse
import codecs
import grpc
import os
import sys

from lnd_grpc import rpc_pb2 as ln
from lnd_grpc import rpc_pb2_grpc as lnrpc
from lnd import Lnd


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--lnd-dir", default="~/.lnd", dest="lnddir", help="lnd directory; default ~/.lnd",
    )
    arg_parser.add_argument(
        "--only-failed-htlcs", default=False, dest="only_failed_htlcs", action='store_true', help="delete only failed htlcs in a payment, but keep payment; default is false",
    )
    arg_parser.add_argument(
        "--only-failed-payments", default=False, dest="only_failed_payments", action='store_true', help="delete only failed payments including the failed payment htlcs; default is false",
    )
    args = arg_parser.parse_args()
    lnd = Lnd(args.lnddir)

    decision = 'not yet'

    if args.only_failed_htlcs is True or args.only_failed_payments is True:
        while decision != 'y' and decision != 'n':
            decision = input('Really delete all failed htlcs? (y/n) ') if args.only_failed_htlcs is True else input('Really delete all failed payments? (y/n) ')
            if decision == 'n':
                sys.exit('Stopping program.')
        print('Your current payments history will be saved to payments-history.txt')
        with open('payments-history.txt', 'w') as f:
            print(lnd.get_payments(), file=f)
        if args.only_failed_payments is True:
            print("Purging all failed payments.")
            lnd.delete_failed_htlcs()
        if args.only_failed_htlcs is True:
            print("Purging all failed htlcs only.")
            lnd.delete_failed_htlcs()
        print('Done.')
        print("Please ensure database compaction is enabled in your lnd config then restart lnd.")
    else:
        arg_parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
