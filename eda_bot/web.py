import webbrowser
from eda_bot import constants

class Web:

    def __new__(cls) -> 'Web':
        if not hasattr(cls, 'instance'):
            cls.__instance: 'Web' = super(Web, cls).__new__(cls)
        return cls.__instance

    def run(cls):
        url = constants.WEBPAGE
        webbrowser.open(url)