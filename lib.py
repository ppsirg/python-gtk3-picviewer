#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" package provide some own stuff """

import os
import re

PIC = 1
TXT = 2
VID = 4


def load_file_list(dirname=".", option=0):
    """ load filelist """
    path = os.path.dirname(dirname)
    if path != '':
        os.chdir(path)
        filename = os.path.basename(dirname)
    else:
        filename = dirname

    filelist = os.listdir('.')
    filelist = get_str_with_re(filelist, filename)
    if option & PIC:
        filelist = [l for l in filelist if is_image(l)]
    filelist = natural_sort(filelist)
    return filelist


def get_str_with_re(stringlist, regex):
    """ returns the strings in stringlist witch compares to the regex """
    return [l for l in stringlist for m in [re.search(regex, l)] if m]


def get_flat_list(org_list):
    """ get all elements of a list of lists in a flat list """
    return [item for sublist in org_list for item in sublist]


def natural_sort(l):
    """ sort a list in natural way (1 ... 10 insteed of 10 ... 1) """
    return sorted(l, key=_natural_sort_key)


def _natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    """ helper function for natural sort """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def is_image(filename):
    """ File is image if it has a common suffix and it is a regular file """
    if not os.path.isfile(filename):
        return False
    return filename.split('.')[-1].lower() in ['jpg', 'png', 'bmp', 'tif', 'jpeg', 'svg', 'gif']


def scale(w, h, x, y, maximum=True):
    """ returns the scaling informations for picture dimensions """
    nw = y * w // h
    nh = x * h // w
    if maximum ^ (nw >= x):
        return nw or 1, y
    return x, nh or 1


def compare_lists(org, new):
    """ compares 2 lists (strings) and returns a string with the result """
    return "".join(["1" if sign1 == sign2 else "0" for sign1, sign2 in zip(org, new)])
