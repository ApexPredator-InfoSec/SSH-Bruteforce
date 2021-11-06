# SSH-Bruteforce
SSH login bruteforce tool

This script was created as a simple SSH login bruteforceing tool for the Red Siege python challenge.

The script accepts single username and password or lists containing multiple usernames and passwords and attempts to login to the target via SSH. It will print invalid login attempts and highlight a successful login in green

usage: python 3 -t <target> -u <username> -ul <username list> -p <password> -pl <password list> -lc <logincount threshold> -st <sleep time after hitting threshold> -to <connection attempt timeout threshold>
  
  python3 sshbrute.py -t 127.0.0.1 -u sshtest -p SSHtestPassword11
  ![image](https://user-images.githubusercontent.com/84335647/140619273-bf0f1ec7-637a-4858-9e9e-71d876bf1751.png)

  python3 sshbrute.py -t 127.0.0.1 -ul usernames.txt -p SSHtestPassword11 -lc 5 -st 5
  ![image](https://user-images.githubusercontent.com/84335647/140619308-1ba0795e-4166-48ff-8624-6f232e255b85.png)

  python3 sshbrute.py -t 127.0.0.1 -ul usernames.txt -pl passwords2.txt -lc 5 -st 5
  ![image](https://user-images.githubusercontent.com/84335647/140619322-e74ae7fb-acb9-4d62-b20d-f1d09b145c15.png)
  ![image](https://user-images.githubusercontent.com/84335647/140619329-60d3c97c-4b2d-4b21-a2c1-b42959fb35ba.png)

  python3 sshbrute.py -t 127.0.0.1 -u sshtest -pl passwords.txt -lc 5 -st 5
  ![image](https://user-images.githubusercontent.com/84335647/140619354-9dfc30dc-ce48-42f5-b06e-5480ebb18f64.png)
  ![image](https://user-images.githubusercontent.com/84335647/140619363-4f748d5f-2953-4852-b513-ebf0d3bc52f5.png)
