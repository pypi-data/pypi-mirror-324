# 🐍
The environment in which you install this package will permit you to use ".🐍" in addition to the usual ".py" extension.

# Caveat emptor
Deviating from long-standing conventions is a recipe for pain and annoyance.

The less traveled path can be fun though! And that is what this silly package is about.

# How it works
Besides package metadata, this package simply adds the two files below to the "site-packages" directory in which you install it.

1) `./ext/snake/__init__.py`: appends ".🐍" to the list of file extensions recognized by [importlib].
1) `./_ext-snake.pth`: directs a Python interpreter using the package directory to load `ext.snake` before pretty much anything else.

It's really that simple.

[importlib]: https://docs.python.org/3/library/importlib.html

# For more fun
Add an alias to the configuration of your favorite shell to alias the `python` command to 🐍 too!

Running Python scripts would then look similar to the following.

```bash
# Without ext-snake
$ python my_script.py

# With ext-snake
$ 🐍 my_script.🐍
```

I typically run my Python code as a module (e.g. `python -m my_module`). I configured 🐍 to map to `python -m` on my system.

```bash
# Without ext-snake
$ python -m my_module

# With ext-snake
$ 🐍 my_module
```

# Customization
I will ignore any request to modify this package for other file extensions. If you want a different emoji (e.g. 💰), you can replicate the approach to your own whim in minutes.
