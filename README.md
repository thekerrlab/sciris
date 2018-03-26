# Sciris Framework for Scientific Web Application Development

The Sciris framework is intended to be a flexible open source framework
for building web applications based on Vue.js and Python.

## Is Sciris ready yet?

**No.** We expect a first version of Sciris to be ready by September 2018. If you would like us to let you know when it's ready for use, please email info@sciris.org.


## Installation and run instructions

### Quick start guide

Note: if you're a developer, you'll likely already have some/all of these packages installed.

0. Install  [Git](https://git-scm.com/downloads) (version control)

0. Install [NodeJS](https://nodejs.org/en/download/) (JavaScript manager)

0. Install [Redis](https://redis.io/topics/quickstart) (database)

0. Install [Anaconda Python](https://www.anaconda.com/download/) for Python 2.7 (simulation engine)

0. Once you've done all that, to install, simply run `python setup.py develop` in the root folder. This should install Sciris as an importable Python module.

To test, open up a new Python window and type `import sciris`. It should say something like `Sciris v0.3 (2018-03-23) loaded`.

If you have problems, please consult the rest of this guide for more information.

### Installing on Windows

#### Package and library dependencies

Make sure that you have `npm` (included in Node.js installation) and `git` installed on your machine.  

First, install [Anaconda Python (for Python 2.7)](https://www.anaconda.com/download/). In your Python setup, you also need to have the following packages (instructions in parentheses show how to install with Anaconda Python environment already installed). **Note**, these should all be installed automatically when you type `python setup.py develop`.
* numpy (already installed under Anaconda)
* matplotlib (already installed under Anaconda)
* flask (already installed under Anaconda)
* flask-login (`conda install flask-login`)
* twisted (`conda install twisted`)
* mpld3 (`conda install mpld3`)
* redis (`pip install redis`)

#### Database dependencies

If you use Redis as your DataStore mode, you will need to have Redis installed
on your computer (as a service).  Redis does not directly support Windows,
but there is a [MicrosoftArchive page on GitHub](https://github.com/MicrosoftArchive/redis)
where you may go for installation directions on your Windows machine.
(For example, it can be installed at [this site](https://github.com/MicrosoftArchive/redis/releases)
, downloading a .msi file).  It
ends up being installed as a service which you can navigate to by going
the Windows Task Manager and going to the Services tab.  Make sure the `Redis`
service is in the Running state.

(For Linux installations, you can probably use the
[Redis Quick Start](https://redis.io/topics/quickstart) site directions.)

Most likely, the directory for your Redis executables will be installed at
`C:\Program Files\Redis`.  In that directory, you can double-click the icon
for `redis-cli.exe` to start the redis database command line interface at
the default Redis database (#0).  You can do `keys *` to look at all of the
store key / value pairs in the database, and `exit` exits the interface.  
Most likely, you will want to use a non-default (i.e. `N` is not 0)
database.  To investigate what keys are in, for example, database #2,
while you are within `redis-cli`, you can type `select 2` to switch to that
database.

### Installing on Linux

0. Install Git: `sudo apt install git`

0. Install NodeJS: `sudo apt install nodejs`

0. Install Redis: https://redis.io/topics/quickstart

0. Install [Anaconda Python](https://www.anaconda.com/download/) for Python 2.7 (not 3.4!), and make sure it's the default Python, e.g.
```
your_computer:~> python
Python 2.7.12 |Anaconda 2.1.0 (64-bit)| (default, Jul  2 2016, 17:42:40)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
```

0. Clone the Sciris repository: `git clone http://github.com/optimamodel/sciris.git`

0. Run `python setup.py develop` in the root Sciris folder.

0. To test, open up a new Python window and type `import sciris`. It should say something like
```
>>> import sciris
Sciris v0.3 (2018-03-23) loaded for local use (display=:0)
>>>
```

## Vue/Python code examples

In the `examples` and `vue_proto_webapps` directories are contained a number
of working examples of web applications combining Vue, Flask, and Twisted.
These are being used as stepping stones for developing the main framework
based in `user_interface`, `session_manager`, `model_code`, and `bin`.

### Hello World

A very simple test case of Sciris. In the `examples/helloworld` folder, type `python server.py`. If you go to `localhost:8080` in your browser, it should be running a simple Python webapp.

### Random Scatterplotter

A slightly more sophisticated version of the previous app, this creates a page with a simple button in the browser.  When the user
presses this in the browser client, the server generates a random matplotlib
scatterplot, which it then returns to the client for display.  This
demonstrates basic communication between a Vue client and a Flask/Twisted
server has been enabled.  See `vue_proto_webapps/scatterplotter_p1/README.md`
for detailed build and run instructions.
