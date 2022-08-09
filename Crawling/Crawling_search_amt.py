import pandas as pd
import urllib.request
from datetime import datetime, timedelta
import json
import sys
import os
import warnings
import re
from pathlib import Path
BASE_DIR = Path().resolve().parent/'Data_Preprocessing'
warnings.filterwarnings(action='ignore')

today = str(datetime.now().date())
recent_8_days = str(datetime.now().date() - timedelta(weeks=1,days=1))
regex = '\(.*\)|\s-\s'

