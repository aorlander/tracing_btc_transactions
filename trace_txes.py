from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash   # (string) the tx_hash on the Bitcoin blockchain
        self.n = n               # (int) the position of this output in the transaction
        self.amount = amount     # (int) the value of this transaction output (in Satoshi)
        self.owner = owner       # (string) the Bitcoin address of the owner of this output
        self.time = time         # (Datetime) the time of this transaction as a datetime object
        self.inputs = []         # (TXO[]) a list of TXO objects

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash', 'n', 'amount', 'owner']
        json_dict = {field: self.__dict__[field] for field in fields}
        json_dict.update({'time': datetime.timestamp(self.time)})
        if len(self.inputs) &gt > 0:
          for txo in self.inputs:
            inputs = json_dict.get('inputs', [])
            inputs.append(json.loads(txo.to_json()))
            json_dict.update({'inputs': inputs})
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    # from_tx_hash(self,tx_hash,n) - this classmethod should connect to the Bitcoin blockchain, and retrieve the nth output 
    # of the transaction with the given hash. Then it should create a new object with the fields, 'tx_hash’, 'n’, 'amount’, 
    # ‘owner’ and ‘time’ set to the values retrieved from the blockchain. This method does not need to initialize the list 
    # 'inputs’. Note that the ‘time’ field should be converted to a datetime object (using the datetime.fromtimestamp method)
    def from_tx_hash(cls,tx_hash,n=0):
        tx = rpc_connection.getrawtransaction(tx_hash,True)
        time = datetime.fromtimestamp(tx['time'])
        for txo in tx['vout']:
            if txo['n']==n:
                owner = txo['scriptPubKey']['addresses'][0]
                value_satoshi = txo['value'] * 100000000
        return TXO(tx_hash=tx_hash, n=n, amount=value_satoshi, owner=owner, time=time)

    # get_inputs(self,depth) - this method should connect to the Bitcoin blockchain, and populate the list of inputs, 
    # up to a depth d. In other words, if d=1  it should create TXO objects to populate self.inputs with the appropriate 
    # TXO objects. If d=2  it should also populate the inputs field of each of the TXOs in self.inputs etc.
    def get_inputs(self,d=1):
        pass
        
       

      
  
