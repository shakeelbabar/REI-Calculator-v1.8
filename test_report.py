from pandas import DataFrame

try:
    df = DataFrame([[1, 11, 111], [2, 22, 222], [3, 33, 333]], columns=['title_1', 'title_2', 'title_3'])
    with open('report.html', 'w') as f:
        f.write(df.to_html())
except Exception as ex:
    print("something was wrong:\n", ex)
    exit(1)

print("Done")
