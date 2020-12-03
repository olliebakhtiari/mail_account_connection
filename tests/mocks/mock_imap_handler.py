class MockImapHandler:
    def __init__(self):
        self.mailbox_map = {'Inbox': [], 'Important': []}

    def fetch(self):
        pass

    def search(self):
        pass

    def store(self):
        pass

    def select(self):
        pass
