import pytest
import os
import grpc

from protobuf import IM_pb2
from protobuf import IM_pb2_grpc

from grpcserver import testserver


def find_protos(path):
    file_name_list = os.listdir(path)
    proto_file_name_list = []
    for file_name in file_name_list:
        if str.endswith(file_name,"proto"):
            proto_file_name_list.append(file_name)
    return proto_file_name_list
    
def proto2grpc(file_name_list):
    for sub_file in file_name_list:
        os.system(
            "python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=./ ./protobuf/"+sub_file)
   

        
if __name__ == '__main__':    
    # 生成对应的grpc 服务文件
    file_name_list = find_protos("./protobuf")
    proto2grpc(file_name_list)
    
    # 启动grpcserver
    testserver.Serve();   
    # 测试grpc 连通性
    testserver.Client()
    
    pytest.main()
