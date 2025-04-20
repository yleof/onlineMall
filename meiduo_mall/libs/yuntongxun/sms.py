from ronglian_sms_sdk import SmsSDK

accId = '2c94811c8b1e335b018be5da9eb42afe'
accToken = 'bef9c8ca647e4b1c8a23ed68880eaa69'
appId = '2c94811c8b1e335b018be5daa03d2b05'

def send_message(tid='1', mobile='18962321668', datas=('1234', '5')):
    sdk = SmsSDK(accId, accToken, appId)
    # 【云通讯】您的验证码是{1}，请于{2}分钟内正确输入。其中{1}和{2}为短信模板参数。
    resp = sdk.sendMessage(tid, mobile, datas)
    resp = eval(resp)
    if resp.get('statusCode') == '000000':
        return 0
    else:
        return -1

if __name__ == '__main__':
    send_message()