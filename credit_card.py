"""
Name: Bereket Asrat
INST326 
Calculating Credit Card

"""

"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys

def get_min_payment(balance, fees=0):
    """Compute the minimum credit card payment."""
    min_payment = (balance * 0.02) + fees
    return max(min_payment, 25)

def interest_charged(balance, apr):
    """Compute the interest accrued in the next payment."""
    daily_rate = apr / 100 / 365
    return daily_rate * balance * 30

def remaining_payments(balance, apr, targetamount=None, credit_line=5000, fees=0):
    """Compute the number of payments required to pay off the balance."""
    payments = 0
    over_75, over_50, over_25 = 0, 0, 0
    
    while balance > 0:
        payment = get_min_payment(balance, fees) if targetamount is None else targetamount
        interest = interest_charged(balance, apr)
        principal_payment = payment - interest
        
        if principal_payment <= 0:
            print("The card balance cannot be paid off with the given parameters.")
            sys.exit(1)
        
        balance -= principal_payment

        if balance > credit_line * 0.75:
            over_75 += 1
        if balance > credit_line * 0.50:
            over_50 += 1
        if balance > credit_line * 0.25:
            over_25 += 1
        
        payments += 1
    
    return payments, over_25, over_50, over_75

def main(balance, apr, targetamount=None, credit_line=5000, fees=0):
    """Compute and display credit card payment details."""
    min_payment = get_min_payment(balance, fees)
    print(f"Your recommended starting minimum payment is ${min_payment:.1f}.")
    
    if targetamount is not None and targetamount < min_payment:
        print("Your target payment is less than the minimum payment for this credit card.")
        sys.exit(1)
    
    payments, over_25, over_50, over_75 = remaining_payments(balance, apr, targetamount, credit_line, fees)
    
    if targetamount is None:
        print(f"If you pay the minimum payments each month, you will pay off the credit card in {payments} payments")
    else:
        print(f"If you make payments of ${targetamount}, you will pay off the credit card in {payments} payments")
    
    result = (f"You will spend a total of {over_25} months over 25% of the credit line\n"
              f"You will spend a total of {over_50} months over 50% of the credit line\n"
              f"You will spend a total of {over_75} months over 75% of the credit line")
    print(result)
    return result

def parse_args(args_list):
    """Parse and validate command-line arguments."""
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type=float, help='The total amount of balance left on the credit account')
    parser.add_argument('apr', type=int, help='The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type=int, help='The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type=int, default=None, help='The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type=float, default=0, help='The fees that are applied monthly.')
    
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    
    print(main(arguments.balance_amount, arguments.apr, credit_line=arguments.credit_line, targetamount=arguments.payment, fees=arguments.fees))