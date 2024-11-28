# xxfer

xxfer is a Python package for sending and/or receiving files to/from a remote source.  Both the sender and the receiver must run the application on their respective machines.

## Installation

There are several installation options.  At the time of this writing, the most straightforward method is installing via command line using pip:

```bash
pip install -i https://test.pypi.org/simple/ xxfer
```

Alternatively, you can download from source (see Releases page) and build it yourself. Downlod the necessary source files, navigate into the downloaded directory, and run:

```bash
python3 -m build
```

## Usage

xxfer offers two distinct modes of operation: Interactive Mode, which prompts the user at each step to enter the requrired information (recommended for new users); and the Command Line Interface, which may be more intuitive (and quicker) for so-called 'power users'.

### Interactive Mode

To launch xxfer in interactive mode -- and assuming you've installed it via pip as discussed above -- you can launch it quite simply with:

```bash
python3 -m xxfer
```

Follow the onscreen prompts to send/receive files.

### Command Line Interface

#### Sending Files

For more advanced users (or those more familiar with command line interfaces), xxfer can be launched directly from the terminal with simple one-liners.  For example, to send a file:

```bash
python3 xxfer.py -s [DESTINATION_IP] -p [DESTINATION_PORT] -f [TARGET_FILE]
```

Provided the remote client is actively listening (ie, running another copy of xxfer on their machine), xxfer will compress and encrypt the file(s) and then immediately send them.

##### Note

By default (this is subject to change in future updates), xxfer encrypts *all* files transmitted using AES encryption on the individual files within the compressed archive.  At this time, the encryption/decryption keys are generated automatically and without user input.  Again, this feature is subject to change in coming updates.

If you are *sending* a file via xxfer, please note that once your file(s) have been transmitted, you will receive a hex-encoded decryption key.  Please ensure you save this decryption and send it to the remote client -- otherwise they'll simply receive an encrypted, zipped archive.

#### Receiving Files

To receive files via the command line interface, simply run:

```bash
python3 xxfer.py -r
```

Provided you have ensured your configuration file is correctly configured -- and you __have forwarded the necessary port on your router/firewall__ -- this will create a listener client.  The client will continue listening on that connection indefinitely or until it either 1) receives an incoming transmission or 2) the connection is closed via the user, for example with [CTRL+C].

## Contributing

If you have *any* feature requests, issues, ideas, or other contributions, feel free to submit a PR or an Issue.

## License

MIT
