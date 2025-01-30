import os
import subprocess
import base64
import  hashlib
import execjs

class CryptoEncrypt:

    def __init__(self):
        try:
            # 执行 node -v 命令，并捕获标准输出和标准错误输出
            result = subprocess.run(['node', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 检查命令执行的返回码，0 表示执行成功
            if result.returncode == 0:
                print('检测到node环境已安装')
                os.system('npm install crypto-js')
                pass
        except FileNotFoundError:
            print('未检测到node环境，请先安装node环境')




    def info(self):
        print('''当前类是一个集各种加密工具方法集合的工具类，你可以利用此工具实现各种加密算法如MD5,AES....''')

    def md5(self,value):
        # 创建md5对象
        md5 = hashlib.md5()
        # 更新md5对象
        md5.update(value.encode('utf8'))
        return md5.hexdigest()
    def sha1(self,value):
        # 创建sha1对象
        sha1 = hashlib.sha1()
        # 更新sha1对象
        sha1.update(value.encode('utf8'))
        return sha1.hexdigest()

    def sha256(self,value):
        # 创建sha256对象
        sha256 = hashlib.sha256()
        # 更新sha256对象
        sha256.update(value.encode('utf8'))
        return sha256.hexdigest()

    def sha512(self,value):
        # 创建sha512对象
        sha512 = hashlib.sha512()
        # 更新sha512对象
        sha512.update(value.encode('utf8'))
        return sha512.hexdigest()

    def sha384(self,value):
        # 创建sha384对象
        sha384 = hashlib.sha384()
        # 更新sha384对象
        sha384.update(value.encode('utf8'))
        return sha384.hexdigest()
    def sha224(self,value):
        # 创建sha224对象
        sha224 = hashlib.sha224()
        # 更新sha224对象
        sha224.update(value.encode('utf8'))
        return sha224.hexdigest()

    def ripemd(self,value):
        # 创建sha3对象
        ripemd = hashlib.new('ripemd160')
        # 更新sha3对象
        ripemd.update(value.encode('utf8'))
        return ripemd.hexdigest()

    def base64Encrypt(self,value):
        bytes_string = value.encode('utf8')
        return base64.b64encode(bytes_string).decode('utf8')

    def base64Decrypt(self,value):
        bytes_string = value.encode('utf8')
        return base64.b64decode(bytes_string).decode('utf8')

    def test(self):
        with open('crypto.js', 'r', encoding='utf8') as f:
            js_code = f.read()
            ctx = execjs.compile(js_code)
            return ctx.call('test')



