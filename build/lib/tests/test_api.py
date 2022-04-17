import pytest

class InsuficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        if amount > self.balance: 
            raise InsuficientFunds("Insuficient funds in account")
        self.balance -= amount

    def collect_interest(self, rate):  
        self.balance *= rate


#client = TestClient(app)

#def ttest_root():
#    res = client.get("/")
#    message = res.json().get("message")



def add(num1: int, num2: int): 
    return num1 + num2

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def regular_bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1, num2, expected", [
    (1,2,3), (3,4 ,7)
    ])
def test_add(num1, num2, expected):
    print ("Testing add function")
    assert add(num1, num2) == expected




def test_bank_set_initial_amount( zero_bank_account):
    assert zero_bank_account.balance == 0

@pytest.mark.parametrize("deposited, withdrawed, expected", [
    (200, 100, 100), (50, 10, 40), (1200, 200, 1000)
])
def test_movements(zero_bank_account, deposited, withdrawed, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawed)
    assert zero_bank_account.balance  == expected

def test_insuficient_funds(regular_bank_account):
    with pytest.raises(Exception):
        regular_bank_account.withdraw(200)

    with pytest.raises(InsuficientFunds):
        regular_bank_account.withdraw(200)




    #zero_bank_account.collect_interest(1.1)
    #assert round( zero_bank_account.balance, 6)  == 80 * 1.1
