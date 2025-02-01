"""
TCP/IP host for the EOQ3 domain

2019 Bjoern Annighoefer
"""

from eoq3.domainwrappers.remotedomainserver import RemoteDomainServer

from eoq3.config import Config, EOQ_DEFAULT_CONFIG
from eoq3.logger import GetLoggerInstance, LOG_LEVELS_NUM
from eoq3.domain import Domain
# external imports
import socket
from threading import Thread
import traceback
#type annotations
from typing import Dict
from abc import ABC

class TcpDomainHostA(ABC):
    """ Abstract base class to enable correct typing
    """
    def __init__(self, maxMsgSize:int, msgSep:bytes, timeout:float=0.2):
        self.maxMsgSize = maxMsgSize
        self.msgSep = msgSep
        self.timeout = timeout #the timeout used for socket polling
    
    def OnSerFrmReceivedByClient(self, frmStr:str, clientId:int):
        raise NotImplemented()
    
    def OnClientConnectionClosed(self, clientId:int):
        raise NotImplemented()

    def Log(self, leve:int, msg:str):
        raise NotImplemented()

class TcpClient:
    """A class to store information about active connections
    """
    def __init__(self, host:TcpDomainHostA, clientId:int, socketInfo, clientAddress, config:Config):
        self.host = host
        self.clientId = clientId
        self.socketInfo =  socketInfo
        self.clientAddress = clientAddress
        self.config = config
        #internals
        self.rxThread = None
        self.shallRun = True
        
    def Start(self):
        self.rxThread = Thread(target=self.__RxThread, args=('TCP Server RxThread %s:%d'%(self.clientAddress[0],self.clientAddress[1]),))
        self.rxThread.start()
        
    def Stop(self):
        self.shallRun = False
        
    def Join(self):
        self.rxThread.join()
        
    def __OnConnectionClosed(self):
        self.Stop()
        self.host.OnClientConnectionClosed(self.clientId)
        
    def __RxThread(self, name:str):
        self.socketInfo.settimeout(self.host.timeout)
        while(self.shallRun):
            try:
                msg = self.socketInfo.recv(self.host.maxMsgSize)
                if(msg):
                    msgs = msg.split(self.host.msgSep)
                    for m in msgs:
                        if(0<len(m)):
                            frmStr = m.decode("utf8")
                            try:
                                self.host.OnSerFrmReceivedByClient(frmStr,self.clientId)
                            except Exception as e:
                                self.host.Log(LOG_LEVELS_NUM.ERROR,'%s: %s raw callback failed: %s'%(self,name,str(e)))
                                traceback.print_exc()
                else: #None = msg
                    #Socket was closed by client
                    self.__OnConnectionClosed()
            except socket.timeout:
                pass #wait for next frame
            except Exception as e:
                self.host.Log(LOG_LEVELS_NUM.ERROR,'%s: %s failed: %s'%(self,name,str(e)))
                #automatically close the client
                self.__OnConnectionClosed()
        #thread ends here
        self.socketInfo.shutdown(socket.SHUT_RDWR)
        self.socketInfo.close()
                    


class TcpDomainHost(RemoteDomainServer,TcpDomainHostA):
    """Enables access to an existing domain through a TCP/IP socket.
    The server listens on a specified port and accepts incoming connections.
    Multiple clients can connect to the server.
    """
    def __init__(self, domain:Domain, shallForwardSerializedCmds:bool, host:str='localhost', port:int=6141, maxMsgSize:int=2**16, msgSep:bytes=b'\x00', config:Config=EOQ_DEFAULT_CONFIG):
        RemoteDomainServer.__init__(self,domain,shallForwardSerializedCmds,config)
        TcpDomainHostA.__init__(self, maxMsgSize, msgSep)
        self.host = host
        self.port = port
        self.maxMsgSize = maxMsgSize
        self.msgSep = msgSep #the separation sequence between two frames
        #internals
        self.logger = GetLoggerInstance(config)
        self.nClients = 0
        self.shallRun = True
        self.connections:Dict[int,TcpClient] = {}
        self.sessionIds:Dict[str,int] = {} #maps session IDs to connections
        #initialize the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        serverAddress = (self.host, self.port)
        self.socket.bind(serverAddress)
        self.socket.listen(1)
        #start receiving thread
        self.acceptThread = Thread(target=self.__AcceptThread, args=('TCP Server ListenerThread',))
        self.acceptThread.start()
    
    #@override
    def OnSerFrmReceivedByClient(self, frmStr:str, clientId:int):
        """Replaces the original OnSerFrmReceived to store the session ID for this client
        """
        frm = self.remoteFrmRxSerializer.DesFrm(frmStr)
        self.sessionIds[frm.sid] = clientId #save the session IDs of the client
        self.OnFrmReceived(frm) #continue with the original processing
        
    #@Override
    def SendSerFrm(self, frmStr:str, sessionId:str)->None:
        """Needs to be overwritten by the implementation
        """
        try: 
            client = self.connections[self.sessionIds[sessionId]]
            msg = frmStr.encode("utf8")+self.msgSep
            client.socketInfo.sendall(msg)
        except KeyError:
            self.logger.Error("Try to reply unknown session ID %s"%(sessionId))
           
    def Stop(self)->None:
        self.shallRun = False
        self.acceptThread.join()
        self.logger.Info('TCP server socket closed.')
        for c in self.connections.values():
            c.Stop()
        for c in self.connections.values():
            c.Join()
        self.logger.Info('TCP clients disconnected.')
        
        
        
    def __AcceptClient(self, socketInfo, clientAddress):
        self.nClients += 1
        client = TcpClient(self,self.nClients,socketInfo,clientAddress,self.config)
        client.Start()
        self.connections[self.nClients] = client
        self.logger.Info('TCP client %s:%d connected.'%(clientAddress[0],clientAddress[1]))
    
    #@override
    def OnClientConnectionClosed(self, clientId:int):
        """This is called back if a client closes a connection
        """
        if(clientId in self.connections):
            # remove all session IDs belonging to the client
            sessionIdsToRemove = [k for k,v in self.sessionIds.items() if v == clientId]
            for s in sessionIdsToRemove:
                del self.sessionIds[s]
            # remove the client itself
            client = self.connections[clientId]
            del self.connections[clientId]
            self.logger.Info('TCP client %s:%d disconnected.'%(client.clientAddress[0],client.clientAddress[1]))
        
    def __AcceptThread(self, name:str):
        """ Waits for clients to connect.
        If a client connects, a new thread for processing client
        requests is created.
        """
        while(self.shallRun):
            clientAddress = None
            try:
                socketInfo, clientAddress = self.socket.accept()
                self.__AcceptClient(socketInfo,clientAddress)
            except socket.timeout:
                pass #wait for next period
        #thread terminates here
        #self.socket.shutdown(socket.SHUT_RDWR) #does not work for accept socket
        self.socket.close()

    # @override
    def Log(self, leve:int, msg:str):
        self.logger.Log(leve,msg)
        
    
        