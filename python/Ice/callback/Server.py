#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2018 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

import signal, sys, traceback, Ice

Ice.loadSlice('Callback.ice')
import Demo

class CallbackSenderI(Demo.CallbackSender):
    def initiateCallback(self, proxy, current):
        print("initiating callback")
        try:
            proxy.callback()
        except Exception:
            traceback.print_exc()

    def shutdown(self, current):
        print("Shutting down...")
        current.adapter.getCommunicator().shutdown()

#
# The Ice communicator is initlialized with Ice.initialize
# The communicator is destroyed once it goes out of scope of the with statement
#
with Ice.initialize(sys.argv, "config.server") as communicator:

    #
    # signal.signal must be called within the same scope as the communicator to catch CtrlC
    #
    signal.signal(signal.SIGINT, lambda signum, frame: communicator.shutdown())

    #
    # The communicator initialization removes all Ice-related arguments from argv
    #
    if len(sys.argv) > 1:
        print(sys.argv[0] + ": too many arguments")
        sys.exit(1)

    adapter = communicator.createObjectAdapter("Callback.Server")
    adapter.add(CallbackSenderI(), Ice.stringToIdentity("callbackSender"))
    adapter.activate()
    communicator.waitForShutdown()
sys.exit(0)