import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mtick
class Graphs:
    def montheExpense_PieChart(fixed, variable):
        sizes = [fixed, variable]
        total = fixed + variable
        val1_perc = '{0:.2f}%'.format((fixed / total) * 100)
        val2_perc = '{0:.2f}%'.format((variable / total) * 100)
        legend1 = str(fixed) + '  (' + str(val1_perc) + ')'
        legend2 = str(variable) + '  (' + str(val2_perc) + ')'
        labels = [legend1, legend2]
        legends = 'Fixed', 'Variable'
        # colors = ['gold', 'yellowgreen']
        explode = (0, 0)  # explode 1st slice
        plt.figure(1, figsize=(10, 5))
        # Plot autopct='%1.1f%%',
        patches, texts = plt.pie(sizes, labels=labels, shadow=True, startangle=140)
        plt.legend(patches, legends, loc='upper right', bbox_to_anchor=(.95, .98), fontsize=14)
        plt.setp(texts, size=12, weight="bold")
        plt.axis('equal')
        plt.title("Fixed and Variable Expenses Analysis", fontsize=20)
        plt.savefig('Monthly Expense.png')
        print("saved figure Expense")

    def monthlyIncome_PieChart(rent, other):
        plt.clf()
        sizes = [rent, other]
        total = rent + other
        val1_perc = '{0:.2f}%'.format((rent / total) * 100)
        val2_perc = '{0:.2f}%'.format((other / total) * 100)
        legend1 = str(rent) + '  (' + str(val1_perc) + ')'
        legend2 = str(other) + '  (' + str(val2_perc) + ')'
        labels = [legend1, legend2]
        legends = 'Rental Income', 'Other Income'
        # colors = ['gold', 'yellowgreen']
        explode = (0, 0)  # explode 1st slice
        plt.figure(1, figsize=(10, 5))
        # Plot autopct='%1.1f%%',
        patches, texts = plt.pie(sizes, labels=labels, shadow=True, startangle=140)
        plt.legend(patches, legends, loc='upper right', bbox_to_anchor=(.95, .98), fontsize=14)
        plt.setp(texts, size=12, weight="bold")
        plt.axis('equal')
        plt.title("Rent and Other Income Chart", fontsize=20)
        plt.savefig('Monthly Income.png')
        print("saved figure Income")

    def fiftyRule_BarGraph(total_income):
        plt.clf()
        tick = mtick.StrMethodFormatter('${x:,.0f}')
        fig = plt.figure(1, figsize=(8, 4))
        ax = fig.add_axes([0, 0, 1, 1])
        langs = ['50% of Income', 'Total Expense']
        amount = [total_income / 2, total_income]
        ax.barh(langs, amount, color=['green', 'blue'])
        ax.xaxis.set_major_formatter(tick)
        total = mpatches.Patch(color='blue', label='Total Income')
        half = mpatches.Patch(color='green', label='50% of Income')
        plt.legend(handles=[total, half])
        plt.title("50% Income Analysis", fontsize=20)
        plt.savefig('Half Income.png', dpi=400, bbox_inches='tight')
        print("saved half income")

# ## 1% Rule - Bar Graph
    def onePercent_Rule(total_income_monthly, purchase_price, rehab_budget):
        one_perc_goal   = 1 # need this to be 1%
        one_perc_act    = total_income_monthly / (purchase_price+rehab_budget)
#         # Create a horizontal bar graph
#             # x-axis as (%)
#             # y-axis as Names: {'1% Monthly Income Goal' 'Actual Monthly Income Percentage'}
#         # If possible, on the right side of of each bar I would like to show ($) amount
        one_perc_goal_doll  = (purchase_price+rehab_budget) * .01
        one_perc_act_doll   = total_income_monthly
        tick = mtick.StrMethodFormatter('${x:,.0f}')
        fig = plt.figure(1, figsize=(6, 6))
        plt.clf()
        ax = fig.add_axes([0, 0, 1, 1])
        langs = ['1% Goal Mnthly Income','Actuall 1% Mnthly Income']
        amount = [one_perc_act_doll, one_perc_goal_doll]
        ax.barh(langs, amount, color=['Red', 'Black'])
        # ax.yaxis.set_major_formatter(tick)
        ax.xaxis.set_major_formatter(tick)
        actual = mpatches.Patch(color='Red', label='Desired Rent Income')
        goal = mpatches.Patch(color='Black', label='Actual 1% Monthly Income')
        plt.legend(handles=[goal, actual])
        plt.title("1% Desired Monthly Income", fontsize=20)
        plt.savefig('1% Goal Chart (horizontal)', dpi=400, bbox_inches='tight')
        print("saved 1% income")

        ## 70% Rule - Bar Graph
    def seventyPercent_Chart(arv, rehab_budget, purchase_price):
        print("arv ",arv)
        print("rehab budget ",rehab_budget)
        print("purchase price ",purchase_price)
        # This is the rule to say that our max offer should be 70% of the ARV - any repairs needed
        max_offer_price     = (arv * .70) - rehab_budget
        act_offer_price     = purchase_price
        # Create a horizontal bar graph
            # x-axis as ($)
            # y-axis as Names: {'Max Offer Price' 'Actual Offer Price'}
        # If possible, on the right side of each bar I would like to show the percentage
        max_offer_perc      = 70 # as a percentage - 70%
        act_offer_perc      = (purchase_price + rehab_budget) / arv
        tick = mtick.StrMethodFormatter('${x:,.0f}')
        plt.clf()
        fig = plt.figure(1, figsize=(2,4))
        ax = fig.add_axes([0,0,1,1])
        langs = ['Max Offer Price', 'Actual Offer Price']
        amount = [act_offer_price, max_offer_price]
        ax.barh(langs, amount, color=['Green', 'Blue'])
        ax.xaxis.set_major_formatter(tick)
        max = mpatches.Patch(color='Blue', label='Actual Offer Price')
        actual = mpatches.Patch(color='Green', label='Max Offer Price')
        plt.legend(handles=[max, actual])
        plt.title("70% Monthly Income", fontsize=20)
        plt.savefig('70% Rule Chart', dpi=400, bbox_inches='tight')
        print("saved 70% rule chart")