from pyspark.sql.functions import when, count, col

class WinRateTransformer:

    def __init__(self):
        self.id = 1
        self.columns = []

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
        print(self.columns)

        result_df = [[0 for _ in range(len(self.columns))] for _ in range(len(self.columns))]

        for idx in range(len(win_loss_list)):
            result_df[self.columns.index(host_list[idx])][self.columns.index(oppo_list[idx])] = win_loss_list[idx]

        return result_df