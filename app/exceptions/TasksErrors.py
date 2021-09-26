class InvalidTaskClassificationError(Exception):
    valide_options: dict = {
        'valide_options' : {
            'importance': [1, 2],
            'urgency': [1,2]
        }
    }

    def __init__(self, importance, urgency) -> None:
        self.received_options = {
            'importance': importance,
            'urgency': urgency
        }

        self.message = {
            'valide_options': self.valide_options['valide_options'],
            'received_options': self.received_options
        }
        
        super().__init__(self.message)

