# Import necessary libraries
import numpy as np
import numpy_financial as npf

# Function to calculate IRR
def calculate_irr(initial_investment, final_value, years):
    return (final_value / initial_investment) ** (1 / years) - 1

# Function to calculate developer's profit in an all-equity deal
def calculate_developer_profit_all_equity(sell_price, tdc, years, irr_threshold, uncle_share, developer_share):
    # Uncle's return calculation
    uncle_return = tdc * (1 + irr_threshold) ** years
    remaining_profit = sell_price - uncle_return
    developer_profit = remaining_profit * developer_share
    return developer_profit

# Function to calculate minimum profit so the developer doesn't work for free in an all-equity deal
def calculate_minimum_profit_for_developer_all_equity(tdc, years, irr_threshold, developer_share):
    uncle_return = tdc * (1 + irr_threshold) ** years
    minimum_sell_price = uncle_return / (1 - developer_share)
    minimum_profit = minimum_sell_price - tdc
    return minimum_profit

# Function to calculate developer's profit with debt financing
def calculate_developer_profit_with_debt(sell_price, tdc, debt_ratio, equity_split, developer_equity, irr_threshold, promote_share):
    total_debt = tdc * debt_ratio
    equity_needed = tdc - total_debt
    uncle_investment = equity_needed * (1 - developer_equity)
    developer_investment = equity_needed * developer_equity
    
    uncle_return = uncle_investment * (1 + irr_threshold) ** 2
    remaining_profit = sell_price - total_debt - uncle_return
    
    promote = remaining_profit * promote_share
    developer_profit = (remaining_profit - promote) * equity_split + promote
    
    return developer_profit, promote

# Question 1a: Developer's profit if he sells the project for $20mm after 2 years in an all-equity deal
# Assume a developer has no money to invest but has found a development opportunity. His uncle is willing to invest with him 100% of the equity but requires the following terms:
# - No developer fee allowed
# - First, annual 15% IRR to the uncle
# - Then split will be 30% to the developer and 70% to the uncle.
# a) Assuming an ‘all equity’ deal of $10mm TDC, what will be the developer’s profit if he sells the project for $20mm after 2 years?

sell_price = 20_000_000
tdc = 10_000_000
years = 2
irr_threshold = 0.15
uncle_share = 0.70
developer_share = 0.30

developer_profit_1a = calculate_developer_profit_all_equity(sell_price, tdc, years, irr_threshold, uncle_share, developer_share)
print(f"1a. Developer's profit (all equity, sell for $20 million): ${developer_profit_1a:,.2f}")

# Question 1b: Minimum profit so the developer doesn't work for free in an all-equity deal
# b) Assuming an ‘all equity’ deal of $10mm TDC and cashing out after 2 years. What should be the minimum profit so the developer doesn’t work for free?

minimum_profit_1b = calculate_minimum_profit_for_developer_all_equity(tdc, years, irr_threshold, developer_share)
print(f"1b. Minimum profit for developer not to work for free (all equity): ${minimum_profit_1b:,.2f}")

# Question 2: Developer's profit with 50% debt financing
# Assume the developer was able to finance the project with 50% debt. TDC is now $11mm due to the financing costs and the developer sells the project after 2 years for $20mm. The developer invests 20% of the equity, the uncle 80% and the developer gets 40% promote after 15% IRR.
# - What is the split now after the 15% hurdle is met?
# - What is the value of the promote (the promote size)?
# - What’s a better deal for the developer: the terms under question #1 or #2?

tdc_with_debt = 11_000_000
debt_ratio = 0.50
equity_split = 0.70
developer_equity = 0.20
promote_share = 0.40

developer_profit_2, promote_size = calculate_developer_profit_with_debt(sell_price, tdc_with_debt, debt_ratio, equity_split, developer_equity, irr_threshold, promote_share)
print(f"2. Developer's profit (50% debt financing, sell for $20 million): ${developer_profit_2:,.2f}")
print(f"2. Value of the promote: ${promote_size:,.2f}")

# Comparison of the two deals
better_deal = "Deal 1" if developer_profit_1a > developer_profit_2 else "Deal 2"
print(f"3. Better deal for the developer: {better_deal}")

def calculate_npv(cash_flows, discount_rate):
    npv = sum([cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows)])
    return npv

# Calculate NPV for Question 1a
initial_investment_1a = -tdc
final_value_1a = sell_price
cash_flows_1a = [initial_investment_1a] + [0] * (years - 1) + [final_value_1a]
discount_rate_1a = irr_threshold

npv_1a = calculate_npv(cash_flows_1a, discount_rate_1a)
print(f"NPV for Question 1a (all equity, sell for $20 million): ${npv_1a:,.2f}")

# Calculate NPV for Question 2
initial_investment_2 = -tdc_with_debt
final_value_2 = sell_price - tdc_with_debt * debt_ratio
cash_flows_2 = [initial_investment_2] + [0] * (years - 1) + [final_value_2]
discount_rate_2 = irr_threshold

npv_2 = calculate_npv(cash_flows_2, discount_rate_2)
print(f"NPV for Question 2 (50% debt financing, sell for $20 million): ${npv_2:,.2f}")

def calculate_irr_alternative(cash_flows):
    return npf.irr(cash_flows)

# IRR for Question 1a
cash_flows_1a_alt = [-tdc] + [0] * (years - 1) + [sell_price]
irr_1a_alt = calculate_irr_alternative(cash_flows_1a_alt)
print(f"IRR for Question 1a (alternative): {irr_1a_alt:.2%}")

# IRR for Question 2
cash_flows_2_alt = [-tdc_with_debt] + [0] * (years - 1) + [sell_price - tdc_with_debt * debt_ratio]
irr_2_alt = calculate_irr_alternative(cash_flows_2_alt)
print(f"IRR for Question 2 (alternative): {irr_2_alt:.2%}")

import unittest

class TestFinancialCalculations(unittest.TestCase):
    def setUp(self):
        self.sell_price = 20_000_000
        self.tdc = 10_000_000
        self.tdc_with_debt = 11_000_000
        self.years = 2
        self.irr_threshold = 0.15
        self.uncle_share = 0.70
        self.developer_share = 0.30
        self.debt_ratio = 0.50
        self.equity_split = 0.70
        self.developer_equity = 0.20
        self.promote_share = 0.40

    def test_developer_profit_all_equity(self):
        developer_profit_mainline = calculate_developer_profit_all_equity(
            self.sell_price, self.tdc, self.years, self.irr_threshold, self.uncle_share, self.developer_share)
        
        npv = calculate_npv([-self.tdc] + [0] * (self.years - 1) + [self.sell_price], self.irr_threshold)
        
        self.assertAlmostEqual(developer_profit_mainline, npv, delta=np.abs(developer_profit_mainline * 0.025))
    
    def test_developer_profit_with_debt(self):
        developer_profit_mainline, promote_mainline = calculate_developer_profit_with_debt(
            self.sell_price, self.tdc_with_debt, self.debt_ratio, self.equity_split, self.developer_equity, self.irr_threshold, self.promote_share)
        
        npv = calculate_npv([-self.tdc_with_debt] + [0] * (self.years - 1) + [self.sell_price - self.tdc_with_debt * self.debt_ratio], self.irr_threshold)
        
        self.assertAlmostEqual(developer_profit_mainline, npv, delta=np.abs(developer_profit_mainline * 0.025))

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

