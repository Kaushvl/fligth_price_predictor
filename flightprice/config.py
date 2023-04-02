import pymongo 
import pandas as pd
import numpy as np
import os, sys
import json
from dataclasses import dataclass

@dataclass
class Environmentvariable:
    mongo_db_url = os.getenv("MONGO_DB_URL")

env_var = Environmentvariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "price"
print("env_var, mongo_db_url")