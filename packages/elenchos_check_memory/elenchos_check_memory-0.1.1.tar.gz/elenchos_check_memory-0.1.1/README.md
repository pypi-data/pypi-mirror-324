# Élenchos: Check Memory

A Élenchos command for checking total, available, used, and free memory.

## Installation and Configuration

Install Élenchos if not already installed:

```shell
cd /opt

mkdir elenchos
cd elenchos

python -m venv .venv
. .venv/bin/activate
pip install elenchos

mkdir bin
ln -s ../.venv/bin/elenchos bin/elenchos
```

Install the `check:memory` plugin:

```shell
cd /opt/elenchos
. .venv/bin/activate

pip install elenchos_check_memory
./bin/elenchos gather-commands
```

Create a configuration file `/etc/nrpe.d/check_memeory.cfg` for `nrpe`:

```
command[check_memory]=/opt/elenchos/bin/elenchos check:memory
```

Finally, restart the `nrpe` daemon:

```shell
systemctl reload nrpe
```

## License

This project is licensed under the terms of the MIT license.
