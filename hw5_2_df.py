import pandas as pd
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

# Initial calculations for given data
uncle_required_return_1a = goal_seek_for_irr(target_irr, tdc, years)
remaining_profit_1a = sell_price - uncle_required_return_1a
developer_profit_1a = remaining_profit_1a * developer_share
uncle_profit_1a = remaining_profit_1a * uncle_share

minimum_sell_price_1b = (tdc * (1 + target_irr) ** years) / (1 - developer_share)
minimum_profit_1b = minimum_sell_price_1b - tdc

tdc_with_debt = 11_000_000
debt_ratio = 0.50
equity_needed = tdc_with_debt * (1 - debt_ratio)
developer_equity = 0.20
uncle_equity = 1 - developer_equity
promote_share = 0.40

uncle_required_return_2 = goal_seek_for_irr(target_irr, equity_needed * uncle_equity, years)
remaining_profit_2 = sell_price - (tdc_with_debt * debt_ratio) - uncle_required_return_2
promote = remaining_profit_2 * promote_share
developer_profit_2 = (remaining_profit_2 - promote) * developer_equity + promote
uncle_profit_2 = (remaining_profit_2 - promote) * uncle_equity

# Creating a DataFrame for better formatting and display
data = {
    "Calculation Step": [
        "Initial Total Development Cost (TDC)", 
        "Sell Price (SP)", 
        "Years", 
        "Target IRR", 
        "Uncle Share", 
        "Developer Share",
        "Uncle's required return (15% IRR)",
        "Remaining profit", 
        "Developer's profit (30% of remaining)",
        "Uncle's profit (70% of remaining)",
        "Minimum sell price to meet 15% IRR",
        "Minimum profit for developer",
        "Total Development Cost with Debt (TDC)",
        "Debt Ratio (DR)",
        "Equity Needed (EN)",
        "Developer Equity (20% of equity needed)",
        "Uncle Equity (80% of equity needed)",
        "Uncle's required return (15% IRR)",
        "Remaining profit after debt and uncle IRR",
        "Promote (40% of remaining)",
        "Developer's profit",
        "Uncle's profit (remaining after promote)",
        "Better deal for developer"
    ],
    "Developer ($)": [
        f"{tdc:,.2f}", 
        f"{sell_price:,.2f}", 
        f"{years}", 
        f"{target_irr:.2%}", 
        f"{uncle_share:.2%}", 
        f"{developer_share:.2%}", 
        "", 
        f"{remaining_profit_1a:,.2f}", 
        f"{developer_profit_1a:,.2f}", 
        "", 
        f"{minimum_sell_price_1b:,.2f}", 
        f"{minimum_profit_1b:,.2f}", 
        f"{tdc_with_debt:,.2f}", 
        f"{debt_ratio * 100:.2f}%", 
        f"{equity_needed:,.2f}", 
        f"{equity_needed * developer_equity:,.2f}", 
        "", 
        "", 
        f"{remaining_profit_2:,.2f}", 
        f"{promote:,.2f}", 
        f"{developer_profit_2:,.2f}", 
        "", 
        "Deal 1 (All Equity)" if developer_profit_1a > developer_profit_2 else "Deal 2 (50% Debt Financing)"
    ],
    "Uncle ($)": [
        f"{tdc:,.2f}", 
        f"{sell_price:,.2f}", 
        f"{years}", 
        f"{target_irr:.2%}", 
        f"{uncle_share:.2%}", 
        f"{developer_share:.2%}", 
        f"{uncle_required_return_1a:,.2f}", 
        f"{remaining_profit_1a:,.2f}", 
        "", 
        f"{uncle_profit_1a:,.2f}", 
        "", 
        "", 
        f"{tdc_with_debt:,.2f}", 
        f"{debt_ratio * 100:.2f}%", 
        f"{equity_needed:,.2f}", 
        "", 
        f"{equity_needed * uncle_equity:,.2f}", 
        f"{uncle_required_return_2:,.2f}", 
        f"{remaining_profit_2:,.2f}", 
        "", 
        "", 
        f"{uncle_profit_2:,.2f}", 
        ""
    ],
    "Notes": [
        "TDC: Total Development Cost", 
        "SP: Sell Price", 
        "", 
        "IRR: Internal Rate of Return", 
        "", 
        "", 
        "PV = FV / (1 + IRR)^n", 
        "", 
        "", 
        "", 
        "SP = UR / (1 - DS)", 
        "", 
        "", 
        "", 
        "EN = TDC * (1 - DR)", 
        "", 
        "", 
        "PV = FV / (1 + IRR)^n", 
        "", 
        "", 
        "", 
        "", 
        ""
    ]
}

df = pd.DataFrame(data)

# Pretty print the DataFrame as a table
print(df.to_string(index=False))

