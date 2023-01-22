class Rule34Exception(Exception):
    pass

class APIError(Rule34Exception):
    def __init__(self, status: str, detail: str) -> None:
        
        super().__init__(f'{status}: {detail}')
        
        self.status = status
        self.detail = detail

