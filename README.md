# TOTP

This is a simple utility script to generate time-based one-time passwords which are generally used as 2-factor authentication tokens for several services.

It allows every parameter specified in the RFC but uses the default values used in most current applications (including Google Authenticator an Authy)

## Usage

To use it you need to first define you keys in the `keys.yaml` file. A sample file is included with random data so you can test the script.

In order to get the keys you need to enable 2FA in any service and write down the shared key. This is usually provided as a base32 encoded string, which is recognized by default by the script.

The provided script can both generate tokens and verify existing tokens (this has no real utility ther than test the script works compared to a real application)

### Generate token

`> python3 totp.py now <service_name>`

The `service_name` can be blank to generate all available services.

`> python3 totp.py verify <service_name> <token>`

This will print `Yes` or `No`.

## License

You can do whatever you want with this. I just did it to learn more about TOTPs.
