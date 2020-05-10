# argon2crack
A simple password cracker for argon2 hashes based on passlib python library. Argon2crack is multithreaded and requires argon2-cffi or argon2pure backends for password cracking. Currently supports only wordlists as inputs.

![Landing Page](https://github.com/DotDotSlashRepo/argon2crack/raw/master/argon2crack.PNG)

**Requires Python3**


## Pre-requisites
It is recommended to use argon2-cffi backend as there are serious preformance improvements with this backend.
```shell
pip install argon2-cffi
pip install passlib
```
Alternatively you may use argon2pure backend as well.
```shell
pip install argon2pure
pip install passlib
```

## Installation

Clone this repository on your local computer.
Run `python argon2crack.py -h`.

## Help

Script supports wordlists only.

```shell
usage: argon2crack.py [-h] [--threads [THREADS]] [--passwordlist [PASSWORDLIST]] --hashlist HASHLIST

Script to crack argon2 hashes.

optional arguments:
  -h, --help            show this help message and exit
  --threads [THREADS]   number of threads for execution, by default up-to 30 threads are used
  --passwordlist [PASSWORDLIST]
                        wordlist file for password cracking, uses 10k-most-common.txt by default

required named arguments:
  --hashlist HASHLIST   file containing argon2 hashes, in the format username:password_hash
```

## Credits

* Inspired by NETSEC- https://netsec.ws/?p=420
* Thanks to Argon2 Team for the supercool password hashing algorithm- https://github.com/hynek/argon2-cffi

## Notes

* If you have issues with argon2 backend engines, try reinstalling argon2-cffi. Worked for me.
* Time taken for cracking is dependant on the capacity of your machine and the complexity of the hash(m,t,p parameters and hash length)
* Script is tested only on Python 3.8.2 on Windows and Debian.
