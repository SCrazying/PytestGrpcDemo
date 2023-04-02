
import protobuf.IM_pb2_grpc
import protobuf.IM_pb2
import grpc
import threading
from concurrent import futures
from common.load_config import config_data
# import common.logger
from common.logger import LOG_ERROR
from common.logger import LOG_INFO


class Common_Client(object):
    host = 'localhost'
    port = '5230'
    conn = None
    client = None
    _instance_lock = threading.Lock()

    def load_config(self):
        LOG_INFO("__init__")
        try:
            self.host = config_data["IM"]["im_gprc_host"]
            self.port = config_data["IM"]["Im_grpc_port"]
        except:
            LOG_ERROR("config log error !!!")
            
    def __new__(cls, *args, **kwargs):
          
            if not hasattr(Common_Client, "_instance"):
                with Common_Client._instance_lock:
                    if not hasattr(Common_Client, "_instance"):
                        Common_Client._instance = object.__new__(cls)  
            return Common_Client._instance

    def __init__(self):
        pass
       
    def Connect(self):
        if Common_Client.conn == None:
            self.load_config()
            try:
                # 监听频道
                LOG_INFO("start listening " + Common_Client.host+ ":" + Common_Client.port)
                Common_Client.conn = grpc.insecure_channel(Common_Client.host + ':' + Common_Client.port)
            except:
                LOG_ERROR("start listening " + Common_Client.host+":"+Common_Client.port + " failed")
                return None
        # 客户端使用Stub类发送请求,参数为频道,为了绑定链接
        if Common_Client.client == None:
            Common_Client.client = protobuf.IM_pb2_grpc.IMServerStub(channel=Common_Client.conn)
            LOG_INFO("client connect" + Common_Client.host+":"+Common_Client.port + " succeed")
        return Common_Client.client

    def DisConnect(self):
        if Common_Client.conn != None:
            Common_Client.conn.close()
            Common_Client.conn = None
            Common_Client.client = None
            LOG_INFO("DisConnect " + Common_Client.host+":"+Common_Client.port + " succeed")

    def __del__(self): 
        # 单例析构的时候调用
        LOG_INFO("单例析构，DisConnect")
        self.DisConnect();
        pass