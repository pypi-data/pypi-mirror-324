# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2021
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
    This module implements how includes of configuration files are handled in
    kas.
"""

import os
from pathlib import Path
from collections import OrderedDict
from collections.abc import Mapping
import functools
import logging
import json
import yaml

from jsonschema.validators import validator_for

from .kasusererror import KasUserError
from . import __file_version__, __compatible_file_version__, __version__
from . import CONFIGSCHEMA

__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2021'

SOURCE_DIR_OVERRIDE_KEY = '_source_dir'
SOURCE_DIR_HOST_OVERRIDE_KEY = '_source_dir_host'
PROJECT_CONFIG_URL = f'https://kas.readthedocs.io/en/{__version__}/' \
    'userguide/project-configuration.html'


class LoadConfigException(KasUserError):
    """
        Class for exceptions that appear while loading a configuration file.
    """
    def __init__(self, message, filename):
        super().__init__(f'{message}: {filename}')


def load_config(filename):
    """
        Load the configuration file and test if version is supported.
    """
    (_, ext) = os.path.splitext(filename)
    config = None
    if ext == '.json':
        with open(filename, 'rb') as fds:
            config = json.load(fds)
    elif ext in ['.yml', '.yaml']:
        with open(filename, 'rb') as fds:
            config = yaml.safe_load(fds)
    else:
        raise LoadConfigException('Config file extension not recognized',
                                  filename)

    validator_class = validator_for(CONFIGSCHEMA)
    validator = validator_class(CONFIGSCHEMA)
    validation_error = False

    for error in sorted(validator.iter_errors(config), key=str):
        validation_error = True
        logging.error('Config file validation Error:\n%s', error.message)
        logging.error('For a list of supported configuration elements, see %s',
                      PROJECT_CONFIG_URL)

    if validation_error:
        logging.debug('Validation against this schema failed:\n%s',
                      json.dumps(error.schema, indent=2))
        raise LoadConfigException('Error(s) occured while validating the '
                                  'config file', filename)

    try:
        version_value = int(config['header']['version'])
    except ValueError:
        # Be compatible: version string '0.10' is equivalent to file version 1
        # This check is already done in the config schema so here just set the
        # right version
        version_value = 1

    if version_value < __compatible_file_version__ or \
       version_value > __file_version__:
        raise LoadConfigException('This version of kas is compatible with '
                                  f'version {__compatible_file_version__} '
                                  f'to {__file_version__}, '
                                  f'file has version {version_value}',
                                  filename)

    if config.get('proxy_config'):
        logging.warning('Obsolete ''proxy_config'' detected. '
                        'This has no effect and will be rejected soon.')

    return (config, config.get(SOURCE_DIR_OVERRIDE_KEY, None))


class IncludeException(KasUserError):
    """
        Class for exceptions that appear in the include mechanism.
    """
    pass


class IncludeHandler:
    """
        Implements a handler where every configuration file should
        contain a dictionary as the base type with and 'includes'
        key containing a list of includes.

        The includes can be specified in two ways: as a string
        containing the path, relative to the repository root from the
        current file, or as a dictionary. The dictionary must have a
        'file' key containing the path to the include file and a 'repo'
        key containing the key of the repository. The path is interpreted
        relative to the repository root path.

        The includes are read and merged from the deepest level upwards.

        In case ``use_lock`` is ``True``, kas checks if a file
        ``<file>.lock.<ext>`` exists next to the first entry in
        ``top_files``. This filename is then appended to the list of
        ``top_files``.
    """

    def __init__(self, top_files, top_repo_path, use_lock=True):
        self.top_files = top_files
        self.top_repo_path = top_repo_path
        self.use_lock = use_lock

    def get_lockfile(self, kasfile=None):
        file = Path(kasfile or self.top_files[0])
        return file.parent / (file.stem + '.lock' + file.suffix)

    def get_top_repo_path(self):
        return self.top_repo_path

    def get_config(self, repos=None):
        """
        Parameters:
          repos -- A dictionary that maps repo names to directory paths

        Returns:
          (config, repos)
            config -- A dictionary containing the configuration
            repos -- A list of missing repo names that are needed \
                     to create a complete configuration
        """

        repos = repos or {}

        def _internal_include_handler(filename, repo_path):
            """
            Recursively loads include files and finds missing repos.

            Includes are done in the following way:

            topfile.yml:
            -------
            header:
              includes:
                - include1.yml
                - repo: repo1
                  file: include-repo1.yml
                - repo: repo2
                  file: include-repo2.yml
                - include3.yml
            -------

            Includes are merged in in this order:
            ['include1.yml', 'include2.yml', 'include-repo1.yml',
             'include-repo2.yml', 'include-repo2.yml', 'topfile.yml']
            On conflict the latter includes overwrite previous ones and
            the current file overwrites every include. (evaluation depth first
            and from top to bottom)
            """

            missing_repos = []
            configs = []
            try:
                current_config, src_dir = load_config(filename)
                # if lockfile exists and locking, inject it after current file
                lockfile = self.get_lockfile(filename)
                if self.use_lock and Path(lockfile).exists():
                    logging.debug('append lockfile %s', lockfile)
                    (cfg, rep) = _internal_include_handler(lockfile,
                                                           repo_path)
                    configs.extend(cfg)
                    missing_repos.extend(rep)
                # src_dir must only be set by auto-generated config file
                if src_dir:
                    self.top_repo_path = src_dir
                    repo_path = src_dir

            except FileNotFoundError:
                raise LoadConfigException('Configuration file not found',
                                          filename)
            if not isinstance(current_config, Mapping):
                raise IncludeException('Configuration file does not contain a '
                                       'dictionary as base type')
            header = current_config.get('header', {})

            for include in header.get('includes', []):
                if isinstance(include, str):
                    includefile = ''
                    if include.startswith(os.path.pathsep):
                        includefile = include
                    else:
                        includefile = os.path.abspath(
                            os.path.join(repo_path, include))
                        if not os.path.exists(includefile):
                            alternate = os.path.abspath(
                                os.path.join(os.path.dirname(filename),
                                             include))
                            if os.path.exists(alternate):
                                logging.warning(
                                    'Falling back to file-relative addressing '
                                    'of local include "%s"', include)
                                logging.warning(
                                    'Update your layer to repo-relative '
                                    'addressing to avoid this warning')
                                includefile = alternate
                    (cfg, rep) = _internal_include_handler(includefile,
                                                           repo_path)
                    configs.extend(cfg)
                    missing_repos.extend(rep)
                elif isinstance(include, Mapping):
                    includerepo = include.get('repo', None)
                    includedir = repos.get(includerepo, None)
                    if includedir is not None:
                        try:
                            includefile = include['file']
                        except KeyError:
                            raise IncludeException(
                                f'"file" is not specified: {include}')
                        abs_includedir = os.path.abspath(includedir)
                        (cfg, rep) = _internal_include_handler(
                            os.path.join(abs_includedir, includefile),
                            abs_includedir)
                        configs.extend(cfg)
                        missing_repos.extend(rep)
                    else:
                        missing_repos.append(includerepo)
            configs.append((filename, current_config))
            # Remove all possible duplicates in missing_repos
            missing_repos = list(OrderedDict.fromkeys(missing_repos))
            return (configs, missing_repos)

        def _internal_dict_merge(dest, upd):
            """
            Merges upd recursively into a copy of dest. The order is preserved
            as in the original dict as dict-insertion orders are preserved from
            Python 3.6 onwards.

            If keys in upd intersect with keys in dest we will do a manual
            merge (helpful for non-dict types like FunctionWrapper).
            """
            if (not isinstance(dest, Mapping)) \
                    or (not isinstance(upd, Mapping)):
                raise IncludeException('Cannot merge using non-dict')
            dest = dest.copy()
            updkeys = list(upd.keys())
            if set(list(dest.keys())) & set(updkeys):
                for key in updkeys:
                    val = upd[key]
                    try:
                        dest_subkey = dest.get(key, None)
                    except AttributeError:
                        dest_subkey = None
                    if isinstance(dest_subkey, Mapping) \
                            and isinstance(val, Mapping):
                        ret = _internal_dict_merge(dest_subkey, val)
                        dest[key] = ret
                    else:
                        dest[key] = upd[key]
                return dest
            try:
                for k in upd:
                    dest[k] = upd[k]
            except AttributeError:
                # this mapping is not a dict
                for k in upd:
                    dest[k] = upd[k]
            return dest

        configs = []
        missing_repos = []
        for configfile in self.top_files:
            cfgs, reps = _internal_include_handler(configfile,
                                                   self.top_repo_path)
            configs.extend(cfgs)
            for repo in reps:
                if repo not in missing_repos:
                    missing_repos.append(repo)

        config = functools.reduce(_internal_dict_merge,
                                  map(lambda x: x[1], configs))
        # the merged config must have the highest (used) version number
        header_version = max([int(cfg['header']['version'])
                              for _, cfg in configs])
        config['header']['version'] = header_version
        return config, missing_repos
