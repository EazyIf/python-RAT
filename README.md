This is a rat project only for educational purposes. Never use this code for illegal or immoral purposes, The developers are not responsible for any damage caused. Read the [license](LICENSE) for more information.

## Installation

```bash
$ pip install -r requirements.txt
```

# Running the project

```bash
$ python rat.py & python dashboard.py && fg
```

This will:

1. Start the server (rat.py).
1. Send it to background.
1. Start the dashboard.py, and keep it in foreground, so you can close it with ctrl-c.
1. When you close the dashboard, you'll return to rat's (server's) foreground, so you can also close it with ctrl-c.

<!-- Thanks to [Ory Band](https://stackoverflow.com/questions/3004811/how-do-you-run-multiple-programs-in-parallel-from-a-bash-script) -->

## Contributing

Contributions are welcome! Please open an issue or pull request.
