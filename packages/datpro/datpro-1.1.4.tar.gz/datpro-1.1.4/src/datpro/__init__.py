# read version from installed package
from importlib.metadata import version
__version__ = version("datpro")

from datpro.datpro import detect_anomalies
from datpro.datpro import plotify
from datpro.datpro import summarize_data