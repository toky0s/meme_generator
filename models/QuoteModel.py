class QuoteModel:
    def __init__(self, body: str, author: str) -> None:
        self.body = body
        self.author = author

    def __str__(self):
        return f'"{self.body}" - {self.author}'