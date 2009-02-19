#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
"""config.py: Configuration handling routines"""

# Copyright (c) 2009, Nicolas Dandrimont <Nicolas.Dandrimont@crans.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from __future__ import with_statement

import os
import re

CONFIG_PATH = '~/.config/feeds2mail/feeds'

NAME_RE = re.compile("^[a-zA-Z0-9_.]+$")

class ConfigFileError(Exception):
    """The config file could not be parsed properly."""
    pass

class ConfigFileNotFound(Exception):
    """The config file could not be opened."""
    pass

def parse_config(config):
    """Parses feeds2html's config file. Returns a dict of all feeds

    The file format is simple: each line defines a new feed, by its name
    (constituted of characters in the range[a-zA-Z0-9_.]), a space, and the URL
    used to access the feed. Raises ConfigFileError on error."""
    
    parsed_config = {}

    config_lines = config.splitlines()
    for config_line in config_lines:
        try:
            feed_name, feed_url = config_line.split(" ", 1)
        except ValueError:
            raise ConfigFileError("Format not respected: %r" % config_line)

        if NAME_RE.match(feed_name):
            if feed_name not in parsed_config:
                parsed_config[feed_name] = feed_url
            else:
                raise ConfigFileError("Duplicated feed name: %r" % feed_name)
        else:
            raise ConfigFileError("Feed name %r doesn't fit format" % feed_name)
    
    return parsed_config

def parse_config_file(filename = None):
    """Returns config file contents.
    
    If filename is not defined, returns the contents of the default config
    file. Raises ConfigFileNotFound on error."""

    if not filename:
        filename = CONFIG_PATH

    filename = os.path.expanduser(filename)

    try:
        with open(filename, 'rb') as configfile:
            contents = configfile.read()
    except IOError:
        raise ConfigFileNotFound("Could not read file '%s'" % filename)
    else:
        return parse_config(contents)
