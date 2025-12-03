from ._anvil_designer import TestTemplate
from anvil import *
import anvil.server
import time


class Test(TestTemplate):
    def __init__(self, **properties):
        time.sleep(10)
        # Set Form properties and Data Bindings.
        #self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
        resp = anvil.server.call("check_port", "85.190.98.95", 22)
        print(resp)

    def button_2_click(self, **event_args):
        resp = anvil.server.call('dns_a_propagation', "wireguard.carlbomsdata.se")
        print(resp)
        
