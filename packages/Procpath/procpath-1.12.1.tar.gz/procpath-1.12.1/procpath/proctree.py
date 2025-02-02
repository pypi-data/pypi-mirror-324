import collections
import json
import logging
import os
from typing import Dict, List, Optional, Type

import jsonpyth

from .procfile import ProcfileType


__all__ = 'Forest', 'JsonPathQueryError', 'flatten', 'process_exists', 'query'

logger = logging.getLogger(__package__)


class AttrDict(dict):
    """
    Attribute key access dictionary.

    It is used for ``jsonpyth`` filter expressions which operate over
    dictionaries and would need subscription otherwise.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class TreeError(Exception):
    """Generic process tree error."""


class JsonPathQueryError(TreeError):
    """JSON Path query error."""


class Forest:

    _procfile_registry: List[Dict[str, ProcfileType]]
    """
    2-pass registry of profiles.

    Elements are dictionaries mapping names to procfile callables.
    """

    _skip_self: bool
    _dictcls: type
    _procfs: str

    def __init__(
        self,
        proc_file_registry: Dict[str, ProcfileType],
        procfs: str = '/proc',
        skip_self: bool = True,
        dictcls: Type[dict] = AttrDict,
    ):
        if 'stat' not in proc_file_registry:
            raise TreeError('stat file reader is required')

        registry = proc_file_registry.copy()
        self._procfile_registry = [{'stat': registry.pop('stat')}, registry]

        is_local_procfs = procfs == '/proc'  # kind of, but a good enough start
        self._skip_self = skip_self and is_local_procfs

        self._procfs = procfs
        self._dictcls = dictcls

    def _get_pid_list(self) -> List[int]:
        all_pids = [int(p) for p in os.listdir(self._procfs) if p.isdigit()]
        if self._skip_self:
            try:
                all_pids.remove(os.getpid())
            except ValueError:
                logger.warning('Procpath process PID was not found in collected PIDs')

        return all_pids

    def _read_process_dict(self, pid, pass_n, *, raise_on_missing_file=True):
        result = self._dictcls()
        for name, pfile in self._procfile_registry[pass_n].items():
            try:
                result[name] = pfile.reader(f'{self._procfs}/{pid}/{name}', dictcls=self._dictcls)
            except (
                # Permission
                PermissionError,
                # Race condition
                FileNotFoundError, ProcessLookupError,
                # Partial and/or corrupted
                ValueError, TypeError,
            ) as ex:
                # Permission errors reported as warnings because they
                # typically mean insufficient privilege what the user
                # may want to raise. Missing file errors mean that it's
                # either a race condition on first pass read which is
                # re-raised, or on second pass where it's reported for
                # debugging message because the user can do nothing.
                #
                # Note that ProcessLookupError can be raise from read()
                # of a procfs file of a process that has just gone. On
                # open() FileNotFoundError is raised in the same case.
                #
                # ValueError may be cause by a partially available/read
                # procfs file (seen on "io" on 3.10 Kernel). TypeError
                # has not been seen but hypothetically can happen in a
                # similar case.
                level = logging.WARNING
                if isinstance(ex, (FileNotFoundError, ProcessLookupError)):
                    if raise_on_missing_file:
                        raise
                    else:
                        level = logging.DEBUG

                msg = 'Storing empty values for pid %d, procfile %s because of %s'
                logger.log(level, msg, pid, name, ex)
                result[name] = (
                    self._dictcls(pfile.empty) if isinstance(pfile.empty, dict) else pfile.empty
                )

        return result

    def _strip_branches(self, nodemap: dict, branch_pids: list) -> dict:
        # Stack of roots of target branches
        nodes = [nodemap[p] for p in branch_pids if p in nodemap]

        # Collect nodes that connect the branches to the root
        result = {}
        path_to_root_children_map = collections.defaultdict(set)
        for node in nodes:
            while node['stat']['ppid'] in nodemap:
                ppid = node['stat']['ppid']
                if ppid not in result:
                    result[ppid] = self._dictcls(nodemap[ppid], children=[])
                parent = result[ppid]

                pid = node['stat']['pid']
                if pid not in path_to_root_children_map[ppid]:
                    parent['children'].append(node)
                    path_to_root_children_map[ppid].add(pid)

                node = parent

        # Collect the branches' descendants
        while nodes:
            node = nodes.pop()
            result[node['stat']['pid']] = node
            nodes.extend(node.get('children', []))

        return result

    def _get_nodemap(self, branch_pids: Optional[list] = None) -> dict:
        """
        Fetch forest expansion dictionary.

        The structure looks like this::

            [
                {'stat': {'pid': 1, 'ppid': 0, ...}, 'children': [
                    {'stat': {'pid': 2, 'ppid': 1, ...}},
                    {'stat': {'pid': 3, 'ppid': 1, ...}},
                    ...
                ]},
                {'stat': {'pid': 2, 'ppid': 1, ...}},
                {'stat': {'pid': 3, 'ppid': 1, ...}},
                ...
            ]

        It allows building a forest in two passes utilising the property
        of dictionaries for the same PID being the same instance.

        Optional branch PID list allows to strip other branches in the
        forest. Given branches are still connected to the root to require
        no change to the JSONPath queries.

        Process procfile collection works in 2 passes. On first pass
        only ``stat``` is read to build the forest structure. On the
        second pass the rest is read. When combined with a branch
        filter it allows to avoid many unnecessary file operations and
        parsing (especially for human-readable ``status``).

        Before first pass all PIDs are read from ``/proc``. In case of
        race condition a procfile may disappear right before the first
        pass. In that case the PID is ignored. If PID is missing on the
        second pass, it's filled with empty values.
        """

        all_pids = self._get_pid_list()
        result = {}
        for pid in all_pids.copy():
            try:
                result[pid] = self._read_process_dict(pid, pass_n=0)
            except (FileNotFoundError, ProcessLookupError):
                all_pids.remove(pid)  # race condition

        for pid in all_pids:
            node = result[pid]
            ppid = node['stat']['ppid']
            if ppid in result:
                result[ppid].setdefault('children', []).append(node)  # type: ignore

        if branch_pids:
            result = self._strip_branches(result, branch_pids)

        for pid, node in result.items():
            node.update(self._read_process_dict(pid, pass_n=1, raise_on_missing_file=False))

        return result

    def get_roots(self, branch_pids: Optional[list] = None) -> list:
        """
        Get root nodes, containing its descendants, of the process forest.

        If optional branch PID list is provided, other branches are
        stripped from the result.
        """

        nodemap = self._get_nodemap(branch_pids)
        return [n for n in nodemap.values() if n['stat']['ppid'] not in nodemap]


def query(roots: List[dict], jsonpath: str) -> list:
    """
    Execute JSONPath query on given root notes.

    :raises JsonPathQueryError:
        Indicated query error.
    """

    try:
        result = jsonpyth.jsonpath({'children': roots}, jsonpath, always_return_list=True)
    except jsonpyth.JsonPathSyntaxError as ex:
        raise JsonPathQueryError(str(ex)) from ex
    else:
        return result


def _flatten_hierarchy(node_list):
    """Turn forest node list recursively into a flat list."""

    result = []
    for node in node_list:
        result.append(node)
        result.extend(_flatten_hierarchy(node.get('children', [])))

    return result

def _flatten_value(v):
    """Turn list values into their JSON string representation."""

    return json.dumps(v, separators=(',', ':')) if isinstance(v, list) else v

def _flatten_file_keys(node: dict, procfile_list):
    """Make flat dictionary out of proc file nested dictionary."""

    result = {}
    for procfile_name, value in node.items():
        if procfile_name not in procfile_list:
            continue

        if isinstance(value, dict):
            result.update({f'{procfile_name}_{k}': _flatten_value(v) for k, v in value.items()})
        else:
            result[procfile_name] = value

    return result

def flatten(node_list, procfile_list):
    """
    Make a PID → flat mapping out of node list.

    Only keys occurring in ``procfile_list`` are taken into result.
    """

    result = _flatten_hierarchy(node_list)
    result = {n['stat']['pid']: _flatten_file_keys(n, procfile_list) for n in result}
    return list(result.values())


def process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
