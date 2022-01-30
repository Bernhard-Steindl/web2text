import sys
import pandas as pd
from scipy import stats

# TODO: is this the correct way? should we rather check elsehow?

def main():
    """
    Statistical signficance testing of two samples distribution for comparing splits?
    """
    if len(sys.argv) < 2:
        print("USAGE: python t-test.py [cleaneval|web2text]")
        sys.exit()

    split = sys.argv[1]
    df = pd.read_csv(f"{split}.csv")
    df.drop(columns=["_"], inplace=True)
    random_df = pd.read_csv(f"random.csv")
    random_df.drop(columns=["_"], inplace=True)

    # TODO: should we take unary values or "normal" ones?



    for col in df.columns:
        their_split_vals = df[col]
        random_vals = random_df[col]
        print(f"{col}: {stats.ttest_ind(random_vals, their_split_vals)}")


    



if __name__ == '__main__':
  main()