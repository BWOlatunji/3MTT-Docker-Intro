import pandas as pd

df = pd.DataFrame({"product": ["A", "B", "C"],
                   "sales": [120, 95, 180]})
print(df.describe())
