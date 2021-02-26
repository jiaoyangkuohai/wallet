import pandas as pd
from database import DBField
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 20)
pd.set_option("display.width", 2000)

if __name__ == '__main__':
    df = pd.read_csv("./data/out.csv")
    df0 = df[df[DBField.inOutClassifier]==DBField.inOutSelect[0]]
    df1 = df0.groupby([DBField.firstClassifier])
    df2 = df.groupby('firstClassifier')
    print(df0)
    print(df1.sum())
    print(df.columns)
    print(df2.sum())