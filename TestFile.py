#! /usr/bin/python
import pdfkit
import matplotlib.pyplot as plt
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#__author__ = "shakeel"
#__date__ = "$Jun 18, 2018 12:27:33 PM$"

# width = int(input('Please enter width: '))
# price_width = 10
# item_width  = width - price_width
# header_fmt = '{{:{}}}{{:>{}}}'.format(item_width, price_width)
# fmt        = '{{:{}}}{{:>{}.2f}}'.format(item_width, price_width)
# print('=' * width)
# print(header_fmt.format('Item', 'Price'))
# print('-' * width)
# print(fmt.format('Apples', 0.4))
# print(fmt.format('Pears', 0.5))
# print(fmt.format('Cantaloupes', 1.92))
# print(fmt.format('Dried Apricots (16 oz.)', 8))
# print(fmt.format('Prunes (4 lbs.)', 12))
# print(fmt.format('Prunes (4 lbs.)', 12))
# print('=' * width)
#
#
# string = str(fmt.format("Here is price", 40))
#
# file = open(r"C:\Users\Shakeel Ahmed\PycharmProjects\untitled4\file11.txt")
# # if(file):
# #     file.write(string)
# #     print("success")
#
# lines = file.readlines()
# values = []
# for line in lines:
#     # print("1 "+line)
#     if(line.__contains__(':')):
#         parts = line.split(':')
#         print((parts[1].strip()))
#         values.append(parts[1].strip())
#
# print(len(values))
# print(values)
# # for long numbers thousand separator using comma
# print ("this is a huge number separated by commas ${0:,}".format(1345**3))

# pdfkit.from_file(r'C:\Users\Shakeel Ahmed\Desktop\report.html', 'out.pdf')

# [44343, 72496]
# val1 = 44343
# val2 = 72496
# amount1 = '${:,.0f}'.format(val1)
# amount2 = '${:,.0f}'.format(val2)
# total = val1+val2
# val1_perc = '{0:.2f}%'.format((val1/total)*100)
# val2_perc = '{0:.2f}%'.format((val2/total)*100)
# legend1 = str(amount1)+'  ('+str(val1_perc)+')'
# legend2 = str(amount2)+'  ('+str(val2_perc)+')'
# legends = [legend1, legend2]
#
# labels = 'Fixed', 'Variable'
# sizes = [val1, val2]
# # colors = ['gold', 'yellowgreen']
# explode = (0, 0)  # explode 1st slice
#
# plt.figure(1, figsize=(10,5))
#
# # Plot autopct='%1.1f%%',
# patches , texts =plt.pie(sizes, labels=legends, shadow=True, startangle=140)
# plt.legend(patches,labels, loc='upper right', bbox_to_anchor=(.95, .98), fontsize=14)
# plt.setp(texts, size=12, weight="bold")
# plt.axis('equal')
# plt.title("Fixed and Variable Expenses Analysis", fontsize=20)
# plt.savefig('save1.png')



from Graphs import Graphs
Graphs.montheExpense_PieChart(44343, 72496)
Graphs.monthlyIncome_PieChart(14760, 10000)
Graphs.fiftyRule_BarGraph(140059)
Graphs.onePercent_Rule(157600, 2000001, 500001)
Graphs.seventyPercent_Chart(3250001, 2000001, 500001)

# Graphs.monthlyIncome_PieChart(14760, 10000)