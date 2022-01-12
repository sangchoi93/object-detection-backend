class InvalidInputException(Exception):
    """Invalid user input
    """
    def __init__(self, message: str):
        self.status_code = 400
        self.message = message
        super().__init__(self.message)