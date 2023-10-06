import pandas as pd
from pyspark.sql.functions import when, count, col

class WinRateTransformer:

    def __init__(self):
        self.id = 1
        self.columns = []
        self.tier_num = 4
        self.schema = ["team_name", "win_rate", "tier_num"]

    def read_table_and_transform(self, df):
        df_t = df.groupBy(["host_team", "oppo_team"]) \
            .agg(
            count(when(col("game_outcome") == "win", True)).alias("total_wins"),
            count("*").alias("total_matches")
        ) \
            .withColumn("win_rate", col("total_wins") / col("total_matches"))

        return df_t

    def process_matrix(self, df):
        host_list = df.select("host_team").rdd.flatMap(lambda x: x).collect()
        oppo_list = df.select("oppo_team").rdd.flatMap(lambda x: x).collect()
        win_loss_list = df.select("win_rate").rdd.flatMap(lambda x: x).collect()
        self.columns = sorted(list(set(host_list + oppo_list)))

        result_df = [[0 for _ in range(len(self.columns))] for _ in range(len(self.columns))]

        for idx in range(len(win_loss_list)):
            result_df[self.columns.index(host_list[idx])][self.columns.index(oppo_list[idx])] = win_loss_list[idx]

        return result_df

    def calculate_win_rate_and_assign_tiers(self, win_loss_2d):
        win_rates = [round(round(sum(row)/len(row), 2) * 100, 1) for row in win_loss_2d]
        combined_matrix = sorted(list(zip(self.columns, win_rates)), key=lambda x: x[1], reverse=True)
        team_size = len(combined_matrix)//self.tier_num## must make sure it is divisible by self.tier_num
        tier_list = []
        for i in range(len(combined_matrix)):
            if i % (len(combined_matrix)//self.tier_num) == 0:
                team_size -= 1
            tier_list.append("tier" + str(self.tier_num + 1 - team_size))
        modified_list = [combined_matrix[idx] + tuple([tier_list[idx]]) for idx in range(len(combined_matrix))]
        return pd.DataFrame(modified_list, columns=self.schema)