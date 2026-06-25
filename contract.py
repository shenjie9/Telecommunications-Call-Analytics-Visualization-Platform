import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>. 
        This may be the first month of the contract. 
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract(Contract):
    """A term contract has a specific start and end date, and a large initial
    term deposit which is forfeited if the contract is cancelled before end
    date but returned if after end date.
    """

    end: datetime.date
    remaining_free_min: int
    right_now: datetime.date

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        Contract.__init__(self, start)
        self.end = end
        self.remaining_free_min = TERM_MINS
        self.right_now = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.right_now = (month, year)
        self.bill = bill
        self.bill.set_rates("TERM", TERM_MINS_COST)
        self.remaining_free_min = TERM_MINS
        if self.start is not None:
            self.bill.add_fixed_cost(TERM_MONTHLY_FEE)
            start = [self.start.month, self.start.year]
            if start[0] == month and start[1] == year:
                self.bill.add_fixed_cost(TERM_DEPOSIT)

    def bill_call(self, call: Call) -> None:
        # get call duration
        # only start billing if duration is over 100, ignore before
        call_length = ceil(call.duration / 60.0)
        if self.remaining_free_min > 0:
            uncharged_minutes = self.remaining_free_min - call_length
            if uncharged_minutes >= 0:
                self.remaining_free_min = uncharged_minutes
                self.bill.add_free_minutes(call_length)
            if uncharged_minutes < 0:
                self.bill.add_free_minutes(self.remaining_free_min)
                self.bill.add_billed_minutes(-uncharged_minutes)
        else:
            self.bill.add_billed_minutes(call_length)

    def cancel_contract(self) -> float:
        if self.right_now[0] >= self.end.month and self.right_now[1] == \
                self.end.year:
            return self.bill.get_cost() - TERM_DEPOSIT
        elif self.right_now[1] > self.end.year:
            return self.bill.get_cost() - TERM_DEPOSIT
        else:
            return self.bill.get_cost()


class MTMContract(Contract):
    """A month-to-month Contract with no end date, initial term deposit or
    free minutes but also has higher rates for calls.
    """

    def __init__(self, start: datetime.date) -> None:
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("MTM", MTM_MINS_COST)
        self.bill.add_fixed_cost(MTM_MONTHLY_FEE)


class PrepaidContract(Contract):
    """A prepaid contract has a start date but no end date and has a certain
    balance, which represents the amount of money owed./
    """

    balance: int

    def __init__(self, start: datetime.date, balance: int) -> None:
        Contract.__init__(self, start)
        self.balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        if self.bill is None:
            self.bill = bill
            self.bill.set_rates("PREPAID", PREPAID_MINS_COST)
            self.bill.add_fixed_cost(self.balance)
        else:
            if self.bill.get_cost() < 0:
                self.balance = self.bill.get_cost()
                self.bill = bill
                self.bill.set_rates("PREPAID", PREPAID_MINS_COST)
                if self.balance > -10:
                    self.balance += -25
                self.bill.add_fixed_cost(self.balance)
            elif self.bill.get_cost() >= 0:
                self.balance = -25
                self.bill = bill
                self.bill.set_rates("PREPAID", PREPAID_MINS_COST)
                self.bill.add_fixed_cost(self.balance)

    def cancel_contract(self) -> float:
        if self.bill.get_cost() >= 0:
            return self.bill.get_cost()
        else:
            return 0.0


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
