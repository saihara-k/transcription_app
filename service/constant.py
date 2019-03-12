# 基本情報の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2 ** 11

# 認証用のJSONファイル
CREDENTIAL_JSON = 'secret.json'

# 録音に関する基本情報
RECORD_SECONDS = 5
iDeviceindex = 0

# 録音のモード(無音が続いても録音し続けるかどうか)
IndefinitelyRec = False
