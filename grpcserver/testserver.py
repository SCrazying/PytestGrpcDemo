import threading
import protobuf.IM_pb2_grpc
import protobuf.IM_pb2
import pytest
import grpc
import time
from concurrent import futures

import sys
sys.path.append('..')


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = '127.0.0.1'
_PORT = '5230'


class IMServer(protobuf.IM_pb2_grpc.IMServerServicer):
    def RunTest(self, request, context):
        return protobuf.IM_pb2.RunTestResponse(results=True)

flag_start_thread = False;

def Serve():
    # 定义服务器并设置最大连接数,corcurrent.futures是一个并发库，类似于线程池的概念
    # 创建一个服务器
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    # 在服务器中添加派生的接口服务（自己实现了处理函数）
    protobuf.IM_pb2_grpc.add_IMServerServicer_to_server(IMServer(), grpcServer)
    # 添加监听端口
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    #  启动服务器
    grpcServer.start()
    global flag_start_thread
    flag_start_thread = True;
    try:
        while flag_start_thread:
            time.sleep(1)
    except KeyboardInterrupt:
        grpcServer.stop(0) # 关闭服务器
    
def ServeThread():
    thread = threading.Thread(target=Serve)
    thread.start();   
    time.sleep(3)

def StopServeThread():
    global flag_start_thread
    flag_start_thread = False;
    

def Client():
    # 监听频道
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    # 客户端使用Stub类发送请求,参数为频道,为了绑定链接
    client = protobuf.IM_pb2_grpc.IMServerStub(channel=conn)
    # 返回的结果就是proto中定义的类
    response = client.RunTest(protobuf.IM_pb2.RunTestRequest(testname="Test", testnum=123))
    print(response)
    conn.close()
