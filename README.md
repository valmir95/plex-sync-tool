# plex-tool-sync

A python tool used to sync and create playlists (and **soon** collections) based on lists from various external sources. The project has been implemented in such a way that adding new external sources is quite easy. You simply implement the _SourceService_ and _ExternalSource_ classes for the desired service and model. The appropriate classes are then created on runtime based on the list urls given from _config.toml_ with the use of factory classes and methods.

Currently the following links from external sources are available and/or worked on:

-   IMDB lists (including search, chart and list urls)
-   Trakt lists
-   _TMBD lists (in progress)_

## Usage

First, you need to create a config file with your playlists/collections with their list urls and your Plex server info. It needs to be called _config.toml_. Take a look at _configexample.toml_ for usage example and descriptions

Minimum Python version: 3.8 (based on [vermin](http://ace.ajax.org))
Developed using Python version: 3.9.2

Install the dependencies

```sh
pip3 install -r requirements.txt
```

And then simply run it

```sh
pip3 main.py
```

After executing the script, it will run and sync the lists from _conifg.toml_.
