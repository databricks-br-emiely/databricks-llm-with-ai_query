# Databricks notebook source
# MAGIC %run ./_common

# COMMAND ----------

from dbacademy import dbgems

username = spark.sql("SELECT current_user() as username").collect()[0].username

local_part = username.split("@")[0]
hash_basis = f"{username}{dbgems.get_workspace_id()}"
username_hash = dbgems.stable_hash(hash_basis, length=4)

username = f"{local_part}_{username_hash}".replace(".", "_")


# Add custom attributes to the SQL context here.
dbgems.set_spark_config("username", username)


# COMMAND ----------

import re

#DA = DBAcademyHelper(course_config, lesson_config)
#DA.reset_lesson()
#DA.init()

#DA.init_mlflow_as_job()

#DA.conclude_setup()
