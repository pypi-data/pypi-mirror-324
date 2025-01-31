from .nsys_event import NsysEvent
from pandas import read_sql_table, DataFrame
from sqlalchemy import text
import os.path


class CUDAGraphsSemantic(NsysEvent):

    cuda_graph_execution_named = 63_000_008 # To display with the rest of the CUDA Activities along with kernels
    cuda_graph_id = 63_000_100
    cuda_graph_exec_id = 63_000_101

    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        if self.check_table("CUPTI_ACTIVITY_KIND_GRAPH_TRACE"):
            with open(os.path.join(os.path.dirname(__file__), '../scripts/graph_cupti.sql'), 'r') as query:
                self.query = text(query.read())
            return True
        else:
            self._empty = True
            return False
    
    def _preprocess(self):
        self._df.reset_index(inplace=True)
        return super()._preprocess()
