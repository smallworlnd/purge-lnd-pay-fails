## This repo is deprecated
This code is no longer useful since cleaning failed payments and failed HTLCs is now easily done via `lncli`.

# purge-lnd-pay-fails

Do you run auto-rebalance scripts? Have you collected a huge amount of failed payments over the years and it's bogging down your node? It's a good idea to get rid of that dead weight to keep your node running optimally. This script can delete failed htlcs within payments and failed payments depending on how you choose to run it.

After running the script, you'll need to restart `lnd` so it can compact your `channel.db` file. To auto-compact `channel.db` on startup, add `db.bolt.auto-compact=true` to your `lnd.conf` and then restart `lnd`.

## Installation

You'll need an active `lnd`, version 0.9.0+ (https://github.com/lightningnetwork/lnd), with routerrpc built in, Python 3 and the requirements.

Get the Repository in the directory where you want to install
```
git clone https://github.com/smallworlnd/purge-lnd-pay-fails
```
Change Directory
```
cd purge-lnd-pay-fails
```
Install

```
pip3 install -r requirements.txt
```

## Usage

Running the script will save all payments history to a file and then delete either all failed htlcs, or all failed payments, or both depending on the user input.

It's highly recommended you bake a custom macaroon for this script using the following command:
```
lncli bakemacaroon uri:/lnrpc.Lightning/DeleteAllPayments uri:/lnrpc.Lightning/ListPayments --save_to=/path/to/lnd/data/chain/bitcoin/mainnet/purge-lnd-pay-fails.macaroon
```

where `/path/to/lnd` specifies your own installation path, usually `~/.lnd` for example.

### Command line arguments

```
usage: purge-lnd-pay-fails.py [-h] [--lnd-dir LNDDIR] [--only-failed-htlcs] [--only-failed-payments]

optional arguments:
  -h, --help            show this help message and exit
  --lnd-dir LNDDIR      lnd directory; default ~/.lnd
  --only-failed-htlcs   delete only failed htlcs in a payment, but keep payment itself; default is false
  --only-failed-payments
                        delete only failed payments; default is false
```
