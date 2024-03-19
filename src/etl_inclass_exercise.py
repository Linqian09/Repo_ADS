# Databricks notebook source
# MAGIC %md #### Workshop for ETL

# COMMAND ----------

from pyspark.sql.functions import datediff, current_date, avg
from pyspark.sql.types import IntegerType

# COMMAND ----------

df_laptimes = spark.read.csv('s3://columbia-gr5069-main/raw/lap_times.csv', header=True)

# COMMAND ----------

display(df_laptimes)

# COMMAND ----------

df_driver =spark.read.csv('s3://columbia-gr5069-main/raw/drivers.csv', header=True)
df_driver.count()

# COMMAND ----------

display(df_driver)

# COMMAND ----------

# MAGIC %md
# MAGIC Transform Data

# COMMAND ----------

df_driver = df_driver.withColumn('age', datediff(current_date(), df_driver.dob)/365)

display(df_driver)

# COMMAND ----------

df_driver = df_driver.withColumn('age', df_driver['age'].cast(IntegerType()))
display(df_driver)

# COMMAND ----------

df_lap_drivers = df_driver.select('driverId','nationality', 'age', 'forename', 'surname', 'url').join(df_laptimes, on = ['driverId'])

# COMMAND ----------

display(df_laptimes)

# COMMAND ----------

# MAGIC %md
# MAGIC Aggregate by Age

# COMMAND ----------

df_lap_drivers = df_lap_drivers.groupby('nationality', 'driverId').agg(avg('milliseconds')) 

# COMMAND ----------

# MAGIC %md ### Stroring Data in S3
# MAGIC

# COMMAND ----------

df_lap_drivers.write.csv('s3://ly2625-gr5069/processed/in_class_workshop/laptimes_by_drivers.csv')
