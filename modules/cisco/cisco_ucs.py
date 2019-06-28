from modules.host import Host

class CiscoUCS(Host):
    def __init__(self, name):
        super().__init__(self, name)

    def connect(self):
        print("Log from CiscoUCS")
        pass
