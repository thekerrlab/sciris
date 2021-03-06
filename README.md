# Welcome to Sciris

## What is Sciris?

Glad you asked! Sciris is a flexible open source framework for building scientific web applications using Python and JavaScript. It comes in two parts: `sciris` is a collection of tools that should make scientific Python coding a more pleasant experience, while `scirisweb` is a collection of tools that allow you to easily build Python webapps. Sciris is built on Numpy and Matplotlib, while Sciris Web is built on Vue.js, Flask, Twisted, Redis, and `mpld3`.

Some highlights of `sciris`:
* `odict` -- like an OrderedDict, but allows reference by position like a list, as well as many powerful methods (such as casting to array, sorting and enumeration functions, etc.)
* `promotetoarray` -- standardizes any kind of numeric input to a Numpy array, so e.g. `1`, `[1]`, `(1,)` etc. are all converted to `array([1])`
* `checktype` -- quickly determine the type of the input, e.g. `checktype([1,2,3], 'arraylike', subtype='number') # returns True`
* `findnearest` -- find the element of an array closest to the input value
* `loadobj`, `saveobj` -- flexible methods to save/load arbitrary Python objects
* `vectocolor` -- map a given vector into a set of colors
* `gridcolors` -- pick a set of colors from maximally distant parts of color-space (e.g. for plots with large numbers of lines)
* `smoothinterp` -- linear interpolation with smoothing
* `asd` -- adaptive stochastic descent, an algorithm for optimizing functions as few function evaluations as possible

Some highlights of `scirisweb`:
* `ScirisApp` -- a fully featured server that can be created as simply as `app = ScirisApp(config)` and run with `app.run()`
* `RPC` -- a simple function for defining links between the frontend and the backend
* `Datastore` -- user and data management based on Redis

## Is Sciris ready yet?

**No.** We expect a first version of Sciris to be ready by October 2018. If you would like us to let you know when it's ready for use, please email info@sciris.org.


## Installation and run instructions

### Quick start guide

Note: if you're a developer, you'll likely already have some/all of these packages installed.

1. Install [NodeJS](https://nodejs.org/en/download/) (JavaScript manager)

2. Install [Redis](https://redis.io/topics/quickstart) (database)

3. Install [Anaconda Python](https://www.anaconda.com/download/) (simulation engine)

4. Once you've done all that, to install, simply run `python setup.py develop` in the root folder, or `python setup.py develop minimal` to skip installing optional dependencies (e.g. spreadsheet reading and writing). This should install Sciris as an importable Python module. If you need Sciris Web as well, run `python setup-web.py develop`.

To test, open up a new Python window and type `import sciris` (and/or `import scirisweb`)

If you have problems, please consult the rest of this guide for more information.


### Installing on Linux

1. Install Git: `sudo apt install git`

2. Install NodeJS: `sudo apt install nodejs`

3. Install Redis: https://redis.io/topics/quickstart

4. Install [Anaconda Python](https://www.anaconda.com/download/), and make sure it's the default Python, e.g.
```
your_computer:~> python
Python 2.7.12 |Anaconda 2.1.0 (64-bit)| (default, Jul  2 2016, 17:42:40)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
```

5. Clone the Sciris repository: `git clone http://github.com/optimamodel/sciris.git`

6. Run `python setup.py develop` and `python setup-web.py develop` in the root Sciris folder.

7. To test, open up a new Python window and type `import sciris` and `import scirisweb`. You should see something like:
```
>>> import sciris
>>> import scirisweb
Sciris Web 0.7.1 (2018-08-25) -- (c) Optima Consortium
>>>
```


### Installing on Windows

#### Package and library dependencies

Make sure that you have `npm` (included in Node.js installation) and `git` installed on your machine.  
First, install [Anaconda Python](https://www.anaconda.com/download/). In your Python setup, you also need to have the following packages (instructions in parentheses show how to install with Anaconda Python environment already installed). **Note**, these should all be installed automatically when you type `python setup.py develop` and `python setup-web.py develop`.

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

Most likely, the directory for your Redis executables will be installed at
`C:\Program Files\Redis`.  In that directory, you can double-click the icon
for `redis-cli.exe` to start the redis database command line interface at
the default Redis database (#0).  You can do `keys *` to look at all of the
store key / value pairs in the database, and `exit` exits the interface.  
Most likely, you will want to use a non-default (i.e. `N` is not 0)
database.  To investigate what keys are in, for example, database #2,
while you are within `redis-cli`, you can type `select 2` to switch to that
database.


### Installing on Mac

**WARNING, work in progress!**

1. Install Git. This can be done by installing Xcode commandline tools.

            xcode-select --install

2. Install NodeJS. Visit https://nodejs.org/en/download/ and download the Mac version and install.

3. Install Redis: https://redis.io/topics/quickstart or run (Assumming brew is installed)

            brew install redis

4. Install [Anaconda Python](https://www.anaconda.com/download/), and make sure it's the default Python, e.g.
```
your_computer:~> python
Python 2.7.12 |Anaconda 2.1.0 (64-bit)| (default, Jul  2 2016, 17:42:40)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
```

5. Create a directory that will hold Scris. For reference purposes we will create and refer to that directory as `pyenv`.

6. Clone the Sciris repository into `pyenv`: `git clone http://github.com/optimamodel/sciris.git`

7. Create a Python virtual environment (venv) inside the directory Optima. This will be the parent of the Sciris folder.

        `virtualenv venv`

    More information about [python virtual environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/) can be found [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
   The project structure should be as follows;
   ```
            -pyenv
                -venv
                -sciris
   ```

8. Get into the virtual environment. While inside the `pyenv` folder, to activate the virtual environment, type:

        ./venv/bin/activate

9. Change to the Sciris root folder and type:
   ```
python setup.py develop
python setup-web.py develop
   ```

10. To test if the if everything is working accordingly, open Python window within the virtual environment and type `import sciris` and `import scirisweb`. If no errors occur, then the import worked.



## Examples

In the `examples` and `vue_proto_webapps` directories are contained a number
of working examples of web applications combining Vue, Flask, and Twisted.
These are being used as stepping stones for developing the main framework
based in `user_interface`, `session_manager`, `model_code`, and `bin`.

### Hello World

A very simple test case of Sciris. In the `examples/helloworld` folder, type `python server.py`. If you go to `localhost:8080` in your browser, it should be running a simple Python webapp.

### Scatterplotter

See the directions [here](https://github.com/optimamodel/sciris/tree/develop/examples/scatterplotter) on how to install and run this example.
