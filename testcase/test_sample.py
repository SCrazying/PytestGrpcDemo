
from protobuf import IM_pb2
from protobuf import IM_pb2_grpc
from common.common_client import Common_Client
from common import logger

class Test_Sample:
    def test_runtest(self):
        rep = Common_Client().Connect().RunTest(IM_pb2.RunTestRequest(testname="Test", testnum=123))
        assert rep.results == True 
        
def func(x):
    return x + 1

def test_RunTest():
    rep = Common_Client().Connect().RunTest(IM_pb2.RunTestRequest(testname="Test", testnum=123))
    assert rep.results == True 
    
def test_answer():
    assert func(3) == 4

def test_answer1():
    assert func(4) == 5

