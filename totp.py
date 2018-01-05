'''
TOTP generator script
'''
import base64
import hmac
import sys
import time
import yaml


class Totp(object):
    '''
    TOTP object to generate TOTP tokens
    '''
    def __init__(self, key, t0=0, ti=30, hash_func='sha1', length=6):
        if isinstance(key, bytes):
            self.key = key
        else:
            self.key = base64.b32decode(bytes(key.upper(), encoding='ascii'))
        self.t0 = t0
        self.ti = ti
        self.length = length

        self.hash_func = hash_func

    def _get(self):
        '''
        Get current TOTP
        '''
        c = ((int(time.time()) - self.t0) // self.ti).to_bytes(
            8, byteorder='big', signed=False)
        h = hmac.HMAC(self.key, c, self.hash_func).digest()
        o = h[-1] & 0x0F  # Use the last 4 bits as offset
        n = bytearray(h[o:o + 4])  # Use 4 bytes from offset as the otp
        n[0] &= 0x7F  # Discard most significant bit
        res = str(int.from_bytes(n, byteorder='big', signed=False))

        if len(res) < self.length:
            return '{{:0>{}}}'.format(self.length).format(res)
        else:
            return res[-self.length:]

    def now(self):
        '''
        Get current OTP
        '''
        return self._get()

    def verify(self, otp):
        '''
        Verify OTP
        '''
        return self._get() == otp


def main():
    '''
    Print TOTP for the specified service or list all available
    '''
    # Parse command line arguments and keys file
    with open('keys.yaml', 'r') as config:
        config = yaml.load(config)
        if len(sys.argv) == 1:
            command = 'now'
        elif len(sys.argv) > 1:
            command = sys.argv[1]

        if command == 'now':
            if len(sys.argv) > 2:
                services = sys.argv[2:]
            else:
                services = config.keys()
            for service in services:
                if service not in config:
                    raise ValueError(
                        '{} not in keys.yaml file'.format(service))
        elif command == 'verify':
            if len(sys.argv) == 4:
                service = sys.argv[2]
                otp = sys.argv[3]
            else:
                raise ValueError('verify command must specify service and OTP')
        else:
            raise ValueError('"{}" command not recognized'.format(command))

    if command == 'now':
        for service in services:
            totp = Totp(**config[service])
            print('{}\n\t{}'.format(service, totp.now()))
    else:
        totp = Totp(**config[service])
        if totp.verify(otp):
            print('Yes')
        else:
            print('No')


if __name__ == '__main__':
    main()
