if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv("exampleData/spy_options_eod.csv")
    print(df.head())