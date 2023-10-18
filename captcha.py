from httpx import Client
from base64 import b64encode, b64decode
from random import randint,choice
from json import dumps,loads
from datetime import datetime
from time import sleep
from Crypto.Cipher import AES # pip install pycryptodome
from .util import SSL
import tzlocal, math, hashlib

Cliimg=Client(headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})
Clicap=Client(headers={"user-agent":"FunCaptchaSolverBylarina/0.1"},timeout=15)

def pos(id,method):
    x=(id%3)*100+(id%3)*3+3+10+randint(1,80)
    y=math.floor(id/3)*100+math.floor(id / 3)*3+3+10+randint(1,80)
    if method=="method_1":
        return {"x":x,"y":y}
    elif method=="method_2":
        return {"x":x,"y":(y+x*x)}
    elif method=="method_3":
        return {"a":x,"b":y}
    elif method=="method_4":
        return [x,y]
    elif method=="method_5":
        return [math.sqrt(x),math.sqrt(y)]
    else: # default
        return {"px":round(x/300, 2),"py":round(y/200,2),"x":x,"y":y}

def encrypt(data, key:str):
    data = data + chr(16-len(data)%16)*(16-len(data)%16)
    salt = b"".join(choice("abcdefghijklmnopqrstuvwxyz").encode() for _ in range(8))
    salted, dx = b"", b""
    while len(salted) < 48:
        dx = hashlib.md5(dx+key.encode()+salt).digest()
        salted += dx
    key = salted[:32]
    iv = salted[32:32+16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = {"ct": b64encode(aes.encrypt(data.encode())).decode("utf-8"), "iv": iv.hex(), "s": salt.hex()}
    return dumps(encrypted_data, separators=(',', ':'))

def decrypt(data,key:str):
    data = loads(data)
    dk = key.encode()+bytes.fromhex(data["s"])
    md5 = [hashlib.md5(dk).digest()]
    result = md5[0]
    for i in range(1, 3+1):
        md5.insert(i, hashlib.md5((md5[i-1]+dk)).digest())
        result += md5[i]
    aes = AES.new(result[:32], AES.MODE_CBC, bytes.fromhex(data["iv"]))
    data = aes.decrypt(b64decode(data["ct"]))
    return data



class FunCaptcha:
    def __init__(self,sitekey,k,fp,ua,proxies=None) -> None:
        self.Cli:Client=None
        self.k=k
        self.ua=ua
        self.fp=fp
        self.Token:str=None
        self.TokenSess:str=None
        self.proxies=proxies
        self.sitekey=sitekey
        self.tier="30"
    def Request(self,method,url,data=None,json=None):
        time_=self.unix()
        for _ in range(5):
            try:return self.Cli.request(method,url,data=data,json=json,headers={"cookie":f"timestamp={time_}; __cf_bm=BSC;","x-requested-id":encrypt('{}',f"REQUESTED{self.TokenSess}ID"),"x-newrelic-timestamp":time_})
            except:sleep(1)
    def GetImage(self):
        pass
    def unix(self):
        a=str(int(float(datetime.now(tzlocal.get_localzone()).timestamp()*1e3)))
        return a[0:7]+"00"+a[7:]
    def SolveW(self,text,data):
        for _ in range(5): # max try
            try:
                id=Clicap.post("https://api.nopecha.com/",json={
                    "key": self.k,
                    "type": "funcaptcha",
                    "task": text,
                    "image_data": [data]
                }).json()
                if id.get("error",0) != 0: sleep(0.5);continue
                for _ in range(15): # 15 sec
                    resp=Clicap.get(f"https://api.nopecha.com/",params={"key":self.k,"id":id["data"]}).json()
                    if resp.get("data",0) != 0: return resp["data"]
                    sleep(1)
                return [] # renew captcha
            except:pass# Exception as e:print("nopecha",e)
    def Solve(self):
        self.Cli=Client(headers={
            "accept": "*/*",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            # "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "cookie": "__cf_bm=NIu6ZNtQp4.loEyvCTbTMg_AF2w7EQFBjzLpq9.17f8-1671658854-0-ARBSy+Ol9pPaUNhVJAaZgNPtZhKbP+iwMy1OpGcEhSNuT2l7kwCrjdlAIuMH8c7OFvMLBxip0nfqGT1tT61I/DM=; timestamp=167165800898083",
            "origin":"https://roblox-api.arkoselabs.com",
            "referer":"https://roblox-api.arkoselabs.com/",
            # "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            # "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": '"Windows"',
            # "sec-fetch-dest": "empty",
            # "sec-fetch-mode": "cors",
            # "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            # "x-newrelic-timestamp": "167165800898083",
            # "x-requested-id": "{"ct":"Qnj7EetCV/c3sYuybK3hJg==","iv":"f34247c0b8973c906b9b7d589be8276c","s":"c36e3881b5ce8e6b"}",
            "x-requested-with": "XMLHttpRequest",
        },verify=SSL()(),timeout=10) # ,proxies=self.proxies
        resp=self.Request("POST","https://roblox-api.arkoselabs.com/fc/gfct/",data={"token":self.TokenSess,"sid":"us-east-1","lang":"en","render_type":"canvas","analytics_tier":self.tier,"data[status]":"init"}).json()
        if resp.get("error",0) != 0:return False
        GameToken=resp["challengeID"]
        try:
            FindThing=resp["string_table"][f"3.instructions-{resp['game_data']['game_variant']}"]
        except:print("! ERROR",resp)
        encrypted_img=resp["game_data"]["customGUI"].get("encrypted_mode",False)
        api_breaker=resp["game_data"]["customGUI"].get("api_breaker",0)
        Answer=[]
        if encrypted_img:
            keyimg=self.Request("POST","https://roblox-api.arkoselabs.com/fc/ekey/",data={"sid":"us-east-1","session_token":self.TokenSess,"game_token":GameToken,}).json().get("decryption_key",0)
            if keyimg==0:return False
        print(f"[*] solve type : {FindThing} len : {len(resp['game_data']['customGUI']['_challenge_imgs'])}")
        # print(f"https://roblox-api.arkoselabs.com/fc/gc/?token={self.TokenSess}&r=us-east-1&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc")
        for url in resp["game_data"]["customGUI"]["_challenge_imgs"]:
            resp=Cliimg.get(url,headers={"referer":"https://roblox-api.arkoselabs.com/fc/assets/tile-game-ui/13.33.0/standard/index.html?meta=3"})
            if resp.status_code != 200:return False
            if encrypted_img: # if encrypted
                data=decrypt(resp.text,keyimg).decode()
                # Image.open(BytesIO(b64decode(data))).save("asd.png")
            else:
                data=b64encode(resp.content).decode()
            resp=self.SolveW(FindThing,data)#["data"]
            # print(resp)
            if len(resp) == 0:return False
            Answer.append(pos(resp.index(True),api_breaker))
            resp=self.Request("POST","https://roblox-api.arkoselabs.com/fc/ca/",data={
                "sid":"us-east-1",
                "session_token":self.TokenSess,
                "game_token":GameToken,        
                "guess":encrypt(dumps(Answer),self.TokenSess),
                "analytics_tier":self.tier,
                "bio":"eyJtYmlvIjoiIiwidGJpbyI6IiIsImtiaW8iOiIifQ==", # will fix this later <3
            }).json()
            # if resp.status_code != 200:
            #     print(resp,self.Token,f"https://roblox-api.arkoselabs.com/fc/gc/?token={self.TokenSess}&r=us-east-1&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc")
            #     return False
            # resp=resp.json()
            # print(resp)
            if resp.get("solved",False):return True
            # timeout
            if resp.get("response",0) != "not answered":return False
            if encrypted_img:keyimg=resp["decryption_key"]
        return False
    def Do(self,blob):
        Clix=Client(proxies=self.proxies,verify=SSL()(),timeout=10,headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "*/*","Origin": "https://www.roblox.com","Referer": "https://www.roblox.com/","Accept-Language": "en-US","Accept-Encoding": "gzip, deflate","user-agent": self.ua})
        for _ in range(5):
            try:
                resp=Clix.post(f"https://roblox-api.arkoselabs.com/fc/gt2/public_key/{self.sitekey}",data={"bda":self.fp,"public_key":self.sitekey,"site":"https://www.roblox.com","userbrowser":self.ua,"language":"en","capi_version":"1.4.3","capi_mode":"inline","style_theme":"default","rnd":f"0.{randint(1100153120312819,90023570840000682)}","data[blob]":blob}).json()
                if resp.get("token",0) == 0:sleep(1);continue
                self.Token=resp["token"]
                self.TokenSess=self.Token.split("|")[0]
                break
            except Exception as e:print(e)
        for _ in range(5): # max try
            try:
                if self.Solve():break
            except:pass
        return self.Token