from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from typing import Optional, Union

class DESCrypt:
    def __init__(self, key: Optional[Union[bytes, str]] = None): # key为bytes类型或十六进制字符串
        if key is None:
            key = DESCrypt.generate_key()
        elif isinstance(key, str):
            key = bytes.fromhex(key)  # 将十六进制的形式转换为bytes类型

        self.key = key
        self.cipher = DES.new(key, DES.MODE_CBC)

    @staticmethod
    def generate_key():
        return get_random_bytes(8)  # 生成8字节的随机密钥

    def getKey(self) -> str:
        return self.key.hex()

    def encrypt(self, plain_text: str):
        iv = self.cipher.iv
        padded_text = pad(plain_text.encode("utf-8"), DES.block_size)  # 填充
        encrypted_text = self.cipher.encrypt(padded_text)
        ret = iv + encrypted_text  # 将IV与密文结合
        return ret.hex()  # 返回十六进制的形式


    def decrypt(self, encrypted_text: Union[bytes, str]):
        if isinstance(encrypted_text, str):
            encrypted_text = bytes.fromhex(encrypted_text)  # 将十六进制的形式转换为bytes类型

        iv = encrypted_text[:DES.block_size]  # 提取IV
        cipher = DES.new(self.key, DES.MODE_CBC, iv)  # 使用相同的IV初始化
        decrypted_padded_text = cipher.decrypt(encrypted_text[DES.block_size:])  # 解密
        return unpad(decrypted_padded_text, DES.block_size).decode("utf-8", errors='replace')  # 去除填充并返回明文
    


if __name__ == "__main__":
    descrypt = DESCrypt()
    print(f"Key: {descrypt.key.hex()}")

    original_text = "Hello, World!"
    encrypted = descrypt.encrypt(original_text)
    print(f"Encrypted: {encrypted}")
    
    decrypted = descrypt.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")

