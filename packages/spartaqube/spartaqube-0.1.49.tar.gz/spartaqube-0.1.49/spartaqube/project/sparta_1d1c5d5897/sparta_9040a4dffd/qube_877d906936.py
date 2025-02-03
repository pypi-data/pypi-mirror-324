_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_dd0eed2170():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_ab337fe574(objectToCrypt):A=objectToCrypt;C=sparta_dd0eed2170();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_976fd2da65(apiAuth):A=apiAuth;B=sparta_dd0eed2170();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_7b73e28f96(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_942290856e(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_7b73e28f96(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_db0160bd9c(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_7b73e28f96(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_10e3acb4ef(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_4f8be77c9e(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_10e3acb4ef(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_8c3d7a5f0c(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_10e3acb4ef(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_99409f7287(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_5fecd4ccbf(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_99409f7287(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_dbeaf906de(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_99409f7287(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_0f3727dd4f():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_bfb952d58b(objectToCrypt):A=objectToCrypt;C=sparta_0f3727dd4f();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_9b234d7d53(objectToDecrypt):A=objectToDecrypt;B=sparta_0f3727dd4f();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)