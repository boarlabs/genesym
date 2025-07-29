from datetime import datetime
import pytz

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_one.load import Load
from src.try_one.parameters.load import LoadParameters
from src.try_one.parameters.intervals import Interval



def test_model_basic_site():