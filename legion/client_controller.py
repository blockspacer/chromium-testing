#!/usr/bin/env python
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""The main client_controller code.

This code is the main entry point for the client machines and handles
registering with the host server and running the local RPC server.
"""

import argparse
import logging
import socket
import sys
import time

#pylint: disable=relative-import
import client_rpc_server
import common_lib


def main():
  print ' '.join(sys.argv)
  common_lib.InitLogging()
  logging.info('Client controller starting')

  parser = argparse.ArgumentParser()
  parser.add_argument('--otp',
                      help='One time token used to authenticate with the host')
  parser.add_argument('--host',
                      help='The ip address of the host')
  parser.add_argument('--idle-timeout', type=int,
                      default=common_lib.DEFAULT_TIMEOUT_SECS,
                      help='The idle timeout for the rpc server in seconds')
  args, _ = parser.parse_known_args()

  logging.info(
      'Registering with discovery server at %s using OTP %s', args.host,
      args.otp)
  server = common_lib.ConnectToServer(args.host).RegisterClient(
      args.otp, common_lib.MY_IP)

  server = client_rpc_server.RPCServer(args.host, args.idle_timeout)

  server.serve_forever()
  return 0


if __name__ == '__main__':
  sys.exit(main())
