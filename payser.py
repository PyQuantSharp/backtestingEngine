if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv("exampleData/spy_options_eod.csv")

    df["time"] = df["time"].astype(str).apply(lambda x: x.split(" ")[0])

    df.to_csv("exampleData/spy_options_eod.csv", index=False)