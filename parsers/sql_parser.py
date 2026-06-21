import ast
import re
from pathlib import Path

from constants import CSV_COLUMNS
from utils.additional_info import build_additional_info


SQL_COLUMNS = [
    "userid",
    "name",
    "username",
    "password",
    "email",
    "permission",
    "sex",
    "country",
    "birth",
]