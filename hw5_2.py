import numpy as np
import numpy_financial as npf

def calculate_irr(cash_flows):
    return npf.irr(cash_flows)

def goal_seek_for_irr(target_irr, tdc, years, initial_guess=1_000_000):
    step = 100_000
    tolerance = 0.0001
    max_iterations = 1000
    iteration = 0
    current_guess = initial_guess
    
    while iteration < max_iterations:
        cash_flows = [-tdc] + [0] * (years - 1) + [current_guess]
        irr = calculate_irr(cash_flows)
        
        if abs(irr - target_irr) < tolerance:
            return current_guess
        
        if irr < target_irr:
            current_guess += step
        else:
            current_guess -= step
            step /= 2
        
        iteration += 1
    
    raise ValueError("Goal seeking did not converge")

# Given data
sell_price = 20_000_000
tdc = 10_000_000
years = 2
target_irr = 0.15
uncle_share = 0.70
developer_share = 0.30

# Print given data
print("Given Data:")
print(f"Sell Price: ${sell_price:,.2f}")
print(f"Total Development Cost (TDC): ${tdc:,.2f}")
print(f"Years: {years}")
print(f"Target IRR: {target_irr:.2%}")
print(f"Uncle Share: {uncle_share:.2%}")
print(f"Developer Share: {developer_share:.2%}")
print()

# Question 1a: Developer's profit if he sells the project for $20mm after 2 years in an all-equity deal
uncle_required_return_1a = goal_seek_for_irr(target_irr, tdc, years)
print(f"Uncle's required return for 15% IRR: ${uncle_required_return_1a:,.2f}")

remaining_profit_1a = sell_price - uncle_required_return_1a
print(f"Remaining profit after uncle's return: ${remaining_profit_1a:,.2f}")

developer_profit_1a = remaining_profit_1a * developer_share
uncle_profit_1a = remaining_profit_1a * uncle_share
print(f"Developer's profit (30% of remaining): ${developer_profit_1a:,.2f}")
print(f"Uncle's profit (70% of remaining): ${uncle_profit_1a:,.2f}")

# Question 1b: Minimum profit so the developer doesn't work for free in an all-equity deal
def calculate_minimum_sell_price(tdc, years, irr_threshold, developer_share):
    uncle_return = tdc * (1 + irr_threshold) ** years
    minimum_sell_price = uncle_return / (1 - developer_share)
    return minimum_sell_price

minimum_sell_price_1b = calculate_minimum_sell_price(tdc, years, target_irr, developer_share)
print(f"Minimum sell price to meet 15% IRR: ${minimum_sell_price_1b:,.2f}")

minimum_profit_1b = minimum_sell_price_1b - tdc
print(f"Minimum profit for developer: ${minimum_profit_1b:,.2f}")

# Question 2: Developer's profit with 50% debt financing
tdc_with_debt = 11_000_000
debt_ratio = 0.50
equity_needed = tdc_with_debt * (1 - debt_ratio)
developer_equity = 0.20
uncle_equity = 1 - developer_equity
promote_share = 0.40

uncle_required_return_2 = goal_seek_for_irr(target_irr, equity_needed * uncle_equity, years)
print(f"Uncle's required return for 15% IRR with debt: ${uncle_required_return_2:,.2f}")

remaining_profit_2 = sell_price - (tdc_with_debt * debt_ratio) - uncle_required_return_2
print(f"Remaining profit after debt and uncle's return: ${remaining_profit_2:,.2f}")

promote = remaining_profit_2 * promote_share
print(f"Promote (40% of remaining): ${promote:,.2f}")

developer_profit_2 = (remaining_profit_2 - promote) * developer_equity + promote
uncle_profit_2 = (remaining_profit_2 - promote) * uncle_equity
print(f"Developer's profit: ${developer_profit_2:,.2f}")
print(f"Uncle's profit: ${uncle_profit_2:,.2f}")

# Print results in a formatted tabular format
print("------------------------------------------------------------------------------------------------------")
print("| Calculation Step                          | Developer ($)      | Uncle ($)           | Notes                        |")
print("------------------------------------------------------------------------------------------------------")
print("| Given Data                                |                    |                     |                              |")
print(f"| Initial Total Development Cost (TDC)      | {tdc:15,.2f}     | {tdc:15,.2f}     | TDC: Total Development Cost   |")
print(f"| Sell Price (SP)                           | {sell_price:15,.2f} | {sell_price:15,.2f} | SP: Sell Price               |")
print(f"| Years                                     | {years:<15}       | {years:<15}       |                              |")
print(f"| Target IRR                                | {target_irr:<15.2%} | {target_irr:<15.2%} | IRR: Internal Rate of Return |")
print(f"| Uncle Share                               | {uncle_share:<15.2%} | {uncle_share:<15.2%} |                              |")
print(f"| Developer Share                           | {developer_share:<15.2%} | {developer_share:<15.2%} |                              |")
print("------------------------------------------------------------------------------------------------------")
print("| Question 1a: Developer's profit (all equity)                                                     |")
print("------------------------------------------------------------------------------------------------------")
print(f"| Uncle's required return (15% IRR)         |                    | {uncle_required_return_1a:15,.2f}  | PV = FV / (1 + IRR)^n         |")
print(f"| Remaining profit                          | {remaining_profit_1a:15,.2f} | {remaining_profit_1a:15,.2f} |                              |")
print(f"| Developer's profit (30% of remaining)     | {developer_profit_1a:15,.2f}  |                     |                              |")
print(f"| Uncle's profit (70% of remaining)         |                     | {uncle_profit_1a:15,.2f}  |                              |")
print("------------------------------------------------------------------------------------------------------")
print("| Question 1b: Minimum profit (all equity)                                                        |")
print("------------------------------------------------------------------------------------------------------")
print(f"| Minimum sell price to meet 15% IRR        | {minimum_sell_price_1b:15,.2f} |                     | SP = UR / (1 - DS)           |")
print(f"| Minimum profit for developer              | {minimum_profit_1b:15,.2f}  |                     |                              |")
print("------------------------------------------------------------------------------------------------------")
print("| Question 2: Developer's profit (50% debt financing)                                             |")
print("------------------------------------------------------------------------------------------------------")
print(f"| Total Development Cost with Debt (TDC)    | {tdc_with_debt:15,.2f} | {tdc_with_debt:15,.2f} |                              |")
print(f"| Debt Ratio (DR)                           | {debt_ratio * 100:<15.2f}% | {debt_ratio * 100:<15.2f}% |                              |")
print(f"| Equity Needed (EN)                        | {equity_needed:15,.2f} | {equity_needed:15,.2f} | EN = TDC * (1 - DR)           |")
print(f"| Developer Equity (20% of equity needed)   | {equity_needed * developer_equity:15,.2f} |                     |                              |")
print(f"| Uncle Equity (80% of equity needed)       |                     | {equity_needed * uncle_equity:15,.2f} |                              |")
print(f"| Uncle's required return (15% IRR)         |                     | {uncle_required_return_2:15,.2f}  | PV = FV / (1 + IRR)^n         |")
print(f"| Remaining profit after debt and uncle IRR | {remaining_profit_2:15,.2f} | {remaining_profit_2:15,.2f} |                              |")
print(f"| Promote (40% of remaining)                | {promote:15,.2f}  |                     |                              |")
print(f"| Developer's profit                        | {developer_profit_2:15,.2f}  |                     |                              |")
print(f"| Uncle's profit (remaining after promote)  |                     | {uncle_profit_2:15,.2f}  |                              |")
print("------------------------------------------------------------------------------------------------------")
print("| Comparison of Deals                                       |")
print("------------------------------------------------------------------------------------------------------")
better_deal = "Deal 1 (All Equity)" if developer_profit_1a > developer_profit_2 else "Deal 2 (50% Debt Financing)"
print(f"| Better deal for developer                  | {better_deal:<15}  |                     |                              |")
print("------------------------------------------------------------------------------------------------------")

