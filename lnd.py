import base64
import os
from os.path import expanduser
import codecs
import grpc
import sys
from lnd_grpc import rpc_pb2 as ln
from lnd_grpc import rpc_pb2_grpc as lnrpc

MESSAGE_SIZE_MB = 50 * 1024 * 1024


class Lnd:
    def __init__(self, lnd_dir):
        os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
        lnd_dir = expanduser(lnd_dir)
        combined_credentials = self.get_credentials(lnd_dir)
        channel_options = [('grpc.max_message_length', MESSAGE_SIZE_MB), ('grpc.max_receive_message_length', MESSAGE_SIZE_MB)]
        grpc_channel = grpc.secure_channel("localhost:10009", combined_credentials, channel_options)
        self.stub = lnrpc.LightningStub(grpc_channel)

    @staticmethod
    def get_credentials(lnd_dir):
        tls_certificate = open(lnd_dir + '/tls.cert', 'rb').read()
        ssl_credentials = grpc.ssl_channel_credentials(tls_certificate)
        if os.path.exists(lnd_dir + '/data/chain/bitcoin/mainnet/purge-lnd-pay-fails.macaroon'):
            macaroon = codecs.encode(open(lnd_dir + '/data/chain/bitcoin/mainnet/purge-lnd-pay-fails.macaroon', 'rb').read(), 'hex')
        else:
            print('\n*** Custom macaroon not baked, it is highly recommended to create a custom macaroon instead! ***\n')
            macaroon = codecs.encode(open(lnd_dir + '/data/chain/bitcoin/mainnet/admin.macaroon', 'rb').read(), 'hex')
        auth_credentials = grpc.metadata_call_credentials(lambda _, callback: callback([('macaroon', macaroon)], None))
        combined_credentials = grpc.composite_channel_credentials(ssl_credentials, auth_credentials)
        return combined_credentials

    def get_payments(self):
        return self.stub.ListPayments(ln.ListPaymentsRequest(max_payments=150000, reversed=True))

    def delete_failed_payments(self):
        return self.stub.DeleteAllPayments(ln.DeleteAllPaymentsRequest(failed_payments_only=True))

    def delete_failed_htlcs(self):
        return self.stub.DeleteAllPayments(ln.DeleteAllPaymentsRequest(failed_htlcs_only=True))
