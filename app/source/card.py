class Card:
    """A class to represent a card in a deck of cards"""

    def __init__(self, shape: str, index: str):
        self.shape = shape
        self.index = index
        self.value = self.val(index)

    def val(self, index):
        """Return the value of the card. if the card is an Ace, return 14 if the card is in "TJQK" return 10,11,12,13 respectively. else return the index of the card as an integer"""
        return (
            14
            if index == "A"
            else 10 + "TJQK".index(index)
            if index in "TJQK"
            else int(index)
        )
