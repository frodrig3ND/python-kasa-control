# CLI

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create-new-device`: Creates a new device in the DB Args: name...
* `get-all-devices`: Display a list of all devices to terminal
* `get-one-device`: Acquire a device on its id Args: id (int): id...
* `turn-off-device`: Turn off a device based on its id Args: id...
* `turn-on-device`: Turn on a device based on its id Args: id...
* `version`: Get program version number

## `create-new-device`

Creates a new device in the DB

Args:
    name (str): Name to assing device
    ip_addr (str): IP address of device

**Usage**:

```console
$ create-new-device [OPTIONS] NAME IP_ADDR
```

**Arguments**:

* `NAME`: [required]
* `IP_ADDR`: [required]

**Options**:

* `--help`: Show this message and exit.

## `get-all-devices`

Display a list of all devices to terminal

**Usage**:

```console
$ get-all-devices [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `get-one-device`

Acquire a device on its id

Args:
    id (int): id of device to get

**Usage**:

```console
$ get-one-device [OPTIONS] ID
```

**Arguments**:

* `ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `turn-off-device`

Turn off a device based on its id

Args:
    id (int): id of device to turn off

**Usage**:

```console
$ turn-off-device [OPTIONS] ID
```

**Arguments**:

* `ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `turn-on-device`

Turn on a device based on its id

Args:
    id (int): id of device to turn off

**Usage**:

```console
$ turn-on-device [OPTIONS] ID
```

**Arguments**:

* `ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `version`

Get program version number

**Usage**:

```console
$ version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
