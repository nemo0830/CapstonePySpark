# CapstonePySpark

## **How to run Dashboard**:

1. Download a cloud-sql-proxy first: https://cloud.google.com/sql/docs/mysql/sql-proxy

2. Install it and run: **cloud-sql-proxy -g --address 0.0.0.0 --port 1234 shaped-splicer-397009:asia-southeast1:prd-ric-database**. -g means auth with your google account, shaped-splicer-397009:asia-southeast1:prd-ric-database is the instance full name shown on Google Cloud Postgres SQL

3. Replace all the "mock_pwd" occurrence with actual password to connect. Email jilingou@gmail.com to know the actual password :)

4. (Optional) Replace os.environ["PYSPARK_PYTHON"] in the code with your python.exe location (hack for heartbeat loss error in spark)

5. You are ready to run GameStatsAnalyzer.py in the dashboard folder! Just one-click run and it will launch in your local host.