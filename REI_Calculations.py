def loan_payment(rate, term, present_value):
    # calculates the loan payment
    monthly_rate = rate / 12
    term_months = term * 12
    payment = (
        present_value
        * (monthly_rate * pow(1 + monthly_rate, term_months))
        / (pow(1 + monthly_rate, term_months) - 1)
    )
    return payment


def future_value(rate, term, payment, present_value):
    # Calculates the future value of the loan
    monthly_rate = rate / 12
    term_months = term * 12
    fut_value = present_value * pow(1 + monthly_rate, term_months) - payment * (
        (pow(1 + monthly_rate, term_months) - 1) / (monthly_rate)
    )
    return fut_value


def fixed_expenses_monthly(electric, WandS, PMI, garbage, HOA, insurance, taxes, other):
    # simple function to sum all the fixed monthly expenses.
    # Returns the monthly and yearly totals
    insurance_per_month = insurance / 12
    taxes_per_month = taxes / 12
    fixed_monthly = sum(
        electric, WandS, PMI, insurance_per_month, taxes_per_month, other
    )
    fixed_yearly = fixed_monthly * 12
    return fixed_monthly, fixed_yearly


def variable_expenses_monthly(total_income_monthly, vacancy, rep_and_main, cap_ex, management):
    # defines the monthly variable costs
    # calculates the total monthly costs
    # calculates the yearly costs
    vacancy_cost = total_income_monthly * vacancy
    r_and_m_cost = total_income_monthly * rep_and_main
    cap_ex_cost = total_income_monthly * cap_ex
    manag_cost = total_income_monthly * management
    var_monthly = sum(vacancy_cost, r_and_m_cost, cap_ex_cost, manag_cost)
    var_yearly = var_monthly * 12
    return var_monthly, var_yearly


def cash_flow_monthly(total_income_monthly, payment, fixed_expense, variable_expense):
    # Calcultes monthly cash flows
    cf_monthly = total_income_monthly - sum(payment, fixed_expense, variable_expense)
    return cf_monthly


def NOI_yearly(total_income_monthly, fixed_yearly, variable_yearly):
    # Calculates NOI
    NOI = (total_income_monthly * 12) - fixed_yearly - variable_yearly
    return NOI


def NIAF_yearly(NOI, payment):
    # Calculates NIAF
    payment_yearly = payment * 12
    NIAF = NOI - payment_yearly
    return NIAF


def cum_NIAF(tot_NIAF, NIAF):
    tot_NIAF = tot_NIAF + NIAF
    return tot_NIAF


def cash_to_close(downpayment, closing_costs, emergency_fund, rehab_budget, finance_rehab_logical):
    # Calculates the cash needed to close the deal
    if finance_rehab_logical:
        rehab_budget = 0
    cash_2_close = sum(downpayment, closing_costs, emergency_fund, rehab_budget)
    return cash_2_close


def cash_on_cash_return(NIAF, cash_2_close):
    # Calculates the cash on cash return
    CoCR = NIAF / cash_2_close
    return CoCR


def cap_rate(NOI, purchase_price, rehab_budget, closing_costs):
    # Calculates the cap rate on the property
    # Cap Rate is the NOI over the total amount of investment
    capRate = NOI / sum(purchase_price, rehab_budget, closing_costs)
    return capRate


def gross_rent_mult(purchase_price, rehab_budget, rental_income_monthly):
    # Calculates the gross rent multiplier
    # Gross rent multiplier = (total purchase price + rehab)/annual rent
    GRM = sum(purchase_price, rehab_budget) / (rental_income_monthly * 12)
    return GRM


def one_perc_rule(purchase_price, rehab_budget, total_income_monthly):
    # Calculates the percentage of rent against the purchase price + rehab
    percentage = (total_income_monthly / sum(purchase_price, rehab_budget)) * 100
    return percentage


def fifty_perc_rule(fixed_costs, variable_costs, total_income_monthly):
    # Calculates the percentage of expense (fixed and variable) to rent
    percentage = (sum(fixed_costs, variable_costs) / total_income_monthly) * 100
    return percentage


def future_equity(fut_value_property, fut_value_loan):
    tot_equity = fut_value_property - fut_value_loan
    return tot_equity


def tot_profit_sold(
    fut_value_property, selling_costs_perc, fut_value_loan, downpayment, cum_NIAF
):
    total_profit_sold = (
        fut_value_property * (1 - selling_costs_perc)
        - fut_value_loan
        - downpayment
        + cum_NIAF
    )
    return total_profit_sold


def compound_annual_growth_rate(total_profit_sold, term_years, cash_2_close):
    CAGR = pow((total_profit_sold + cash_2_close) / cash_2_close, 1 / term_years) - 1
    return CAGR


def return_on_investment(tot_equity, cum_NIAF, cash_2_close):
    ROI = ((tot_equity + cum_NIAF) / cash_2_close) - 1
    return ROI
