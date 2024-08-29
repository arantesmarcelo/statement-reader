class Transaction:
    def __init__(self):
        self.id: int = 0
        self.date = ""
        self.type: str = ""
        self.description: str = ""
        self.amount: float = 0
        self.balance: float = 0

    def print_me(self):
        print(
            f"Date: {self.date} \nType: {self.type} \nDescription: {self.description} \nAmount: {self.amount} \n"
            f"Balance: {self.balance}")
