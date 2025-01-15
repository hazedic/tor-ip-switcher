# tor-ip-switcher
> *This script is a CLI tool for interacting with the Tor network's control port to issue a NEWNYM signal, which requests a new IP address for the Tor client. It connects to the Tor control port, authenticates using a password (if provided), and repeatedly requests a new identity (IP) at a specified interval. The script logs the results in the terminal and can be used for scenarios requiring IP rotation through the Tor network.*

## Usage

If the ControlPort 9051 and HashedControlPassword are not set in your torrc file, you can either provide the password as a command-line argument (--passwd "your_password") or set it in the torrc file for persistent configuration.

### Option 1: Setting the Password via the Command-Line Argument
If you prefer to pass the password directly when running the script, you can use the --passwd argument as shown below:

```sh
$ python tor-ip-switcher.py --host localhost --port 9051 --passwd "your_password" --interval 30
```

### Option 2: Configuring the Password in torrc
To set the password permanently in the torrc file, follow these steps:

1. Locate and open the **torrc** file. On Linux systems, it is typically located at:
    - /etc/tor/torrc

2. Add the following lines to the torrc file:
```sh
ControlPort 9051
HashedControlPassword <hashed_password>
```

```sh
# This will output the hashed password, which you can then copy and paste into your torrc file.
tor --hash-password "your_password"
```

3. After making these changes, restart the Tor service to apply the new settings:
```sh
sudo service tor restart
```
Once the password is set in the torrc file, the script will automatically authenticate using the password without the need for the --passwd argument.

**Note:** This script has been tested on Kali Linux 2024.3.