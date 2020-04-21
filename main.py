from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QDialog, QColorDialog
import sys
from pandas import DataFrame, IndexSlice

from REI_calc_main_design import Ui_MainWindow
from settings_window import Ui_SettingsDialog
import REI_Calculations


class SettingsWindow(QDialog):
    caption_bgcolor = "#ffbf00"
    special_row_bgcolor = "#359aa5"

    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.set_default_colors()

    def set_default_colors(self):
        settings = QtCore.QSettings('calculator_settings')
        if not settings.value('caption_bgcolor'):
            print('Setting default colors')
            settings.setValue('caption_bgcolor', self.caption_bgcolor)
            settings.setValue('special_row_bgcolor', self.caption_bgcolor)
        
        # set default colors
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", self.caption_bgcolor
        )
        self.ui.caption_bgcolor_button.setStyleSheet(color_name)
        self.ui.caption_bgcolor_button.setText("")
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", self.special_row_bgcolor
        )
        self.ui.special_row_bgcolor_button.setStyleSheet(color_name)
        self.ui.special_row_bgcolor_button.setText("")

        self.init_controls()

    def init_controls(self):
        self.ui.caption_bgcolor_button.clicked.connect(self.set_caption_bgcolor)
        self.ui.special_row_bgcolor_button.clicked.connect(self.set_special_row_bgcolor)
        self.settings = QtCore.QSettings("calculator_settings")
        self.ui.save_button.clicked.connect(self.save_settings)

    def set_caption_bgcolor(self):
        col = QColorDialog.getColor()
        self.caption_bgcolor = col.name()
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", col.name()
        )

        if col.isValid():
            self.ui.caption_bgcolor_button.setStyleSheet(color_name)

    def set_special_row_bgcolor(self):
        col = QColorDialog.getColor()
        self.special_row_bgcolor = col.name()
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", col.name()
        )

        if col.isValid():
            self.ui.special_row_bgcolor_button.setStyleSheet(color_name)

    def save_settings(self):
        self.settings.setValue("caption_bgcolor", self.caption_bgcolor)
        self.settings.setValue("special_row_bgcolor", self.special_row_bgcolor)
        self.close()


class CalculatorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalculatorWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_signals()

    def init_signals(self):
        self.ui.Generate_Report.clicked.connect(self.generate_report)
        self.ui.actionSettings.triggered.connect(self.settings_window)

    def settings_window(self):
        settings_dialog = SettingsWindow(self)
        settings_dialog.show()

    def generate_report(self):
        print("Running calculations...")
        self.run_calculations()

    def set_dataframe_style(self):
        """Set style for dataframe in charge of storing all final calculations"""
        df.style.set_properties(
            **{"background-color": "green", "color": "white", "border-color": "white"},
            subset=IndexSlice[1, ["id", "count", "type"]]
        )

    def run_calculations(self):
        ## Initially we just need to calculate the 12 key figures.
        ## Will then build a loop for the Pro forma statement.

        # Begin by calculating the monthly payment of the loan
        payment = REI_Calculations.loan_payment(rate, term, present_value)

        # Each item that is to be showcased will have a number before it.
        # only 8 are being calculated here.  There are an additional 4
        #   - Purchase Price (taken from GUI input)
        #   - Monthly Income (taken from GUI input)
        #   - Monthly Expense ( sum(fixed_monthly, var_monthly) )
        # The desired order for the 12 are to be as follows:
        #
        # cash_2_close  Purch. Price   Monthly Income
        # Monthly Exp.  Monthly CF     50% Rule
        # NOI           NIAF           CoCR
        # Cap Rate      1% Rule        Gross Rent Mult.

        # Calculate the fixed and variable expenses
        fixed_monthly, fixed_yearly = REI_Calculations.fixed_expenses_monthly(
            electric, WandS, PMI, garbage, HOA, Insurance, taxes, other
        )

        var_monthly, var_yearly = REI_Calculations.variable_expenses_monthly(
            total_income_monthly, vacancy, rep_and_main, cap_ex, management
        )

        # 1 Calculate NOI
        NOI = REI_Calculations.NOI_yearly(
            total_income_monthly * 12, fixed_yearly, var_yearly
        )

        # 2,3 Calculate Monthly and yearly NIAF or monthly cash flows
        cf_monthly = REI_Calculations.cash_flow_monthly(
            total_income_monthly, payment, fixed_monthly, var_monthly
        )
        NIAF = REI_Calculations.NIAF_yearly(NOI, payment)

        # 4 Calculate the cash to close
        cash_2_close = REI_Calculations.cash_to_close(
            downpayment,
            closing_costs,
            emergency_fund,
            rehab_budget,
            finance_rehab_logical,
        )

        # 5 Calculate Cash on Cash Return (CoCR)
        CoCR = REI_Calculations.cash_on_cash_return(NIAF, cash_2_close)

        # 6 Calculate the cap rate
        capRate = REI_Calculations.cap_rate(NOI, purchase_price, closing_costs)

        # 7 Calculate Gross Rent Multiplier
        GRM = REI_Calculations.gross_rent_mult(
            purchase_price, rehab_budget, total_income_monthly
        )

        # 8,9 Calculate the 1 and 50 percent rules
        one_perc = REI_Calculations.one_perc_rule(
            purchase_price, rehab_budget, total_income_monthly
        )
        fifty_perc = REI_Calculations.fifty_perc_rule(
            fixed_monthly, var_monthly, total_income_monthly
        )

        ## Will need to store this data now as some of it may be overwritten
        # during the pro forma construction

        ## Now we begin the loop for ten years.  I will define a var here
        # because in the future I may make this adjustable for the number
        # of years to do the pro forma for

        ## Pro forma begins
        # Set initial values
        cum_NIAF = 0
        cum_CoCR = 0
        length_yrs = range(1, 10)

        for year_index in length_yrs:
            # Everything will be on a yearly scale and we may calculate some
            # variables two time for this first year

            # Calculate total annual income for each year
            tot_income_annual = REI_Calculations.future_value(
                rent_appreciation_input, year_index - 1, 0, tot_monthly_income
            )

            # Calculate total fixed expenses for each year
            fixed_yearly = REI_Calculations.future_value(
                exp_appreciation_input, year_index - 1, 0, fixed_monthly * 12
            )

            # Calculate total variable expenses for each year
            var_yearly = tot_income_annual * sum(
                r_and_m_input, cap_ex_input, vacancy_input, manag_input
            )

            # Calculate Total Expenses
            tot_expense_yearly = sum(fixed_yearly, var_yearly)

            # Calculate NOI
            NOI = REI_Calculations.NOI_yearly(
                tot_income_annual, fixed_yearly, var_yearly
            )

            # Calculate Debt service
            if term_input < year_index:
                payment = 0
            payment_annual = payment * 12

            # Calculate NIAF
            NIAF = REI_Calculations.NIAF_yearly(NOI, payment)

            # Calculate Property Value
            prop_value = REI_Calculations.future_value(
                prop_appreciation_input, year_index - 1, 0, arv_input
            )

            # Calculate Cash on Cash Return
            CoCR = REI_Calculations.cash_on_cash_return(NIAF, cash_2_close)

            # Calculate cumulative CoCR
            cum_CoCR = cum_CoCR + CoCR

            # Calculate cumulative NIAF
            cum_NIAF = cum_NIAF + NIAF

            # Calculate future loan balance
            loan_balance = REI_Calculations.future_value(
                int_rate_input / 12, year_index * 12, payment, loan_amount_auto
            )
            # Calculate total equity owned by investor
            tot_equity = REI_Calculations.future_equity(prop_value, loan_balance)

            # Calculate percent of equity owned by the investor
            equity_perc = tot_equity / prop_value

            # Calculate ROI
            ROI = REI_Calculations.return_on_investment(
                tot_equity, cum_NIAF, cash_2_close
            )

            # Calculate profit if sold
            total_profit_sold = REI_Calculations.tot_profit_sold(
                prop_value, selling_costs_input, loan_balance, cash_2_close, cum_NIAF
            )

            # Calculate the compounded annual growth rate (CAGR) if sold
            CAGR = REI_Calculations.compound_annual_growth_rate(
                total_profit_sold, year_index, cash_2_close
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = CalculatorWindow()
    application.show()
    sys.exit(app.exec())
