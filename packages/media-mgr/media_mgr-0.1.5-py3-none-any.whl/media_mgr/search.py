#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Search Methods
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from collections import defaultdict

import subprocess
import json
import os
import re

from quickcolor.color_def import color
from showexception.showexception import exception_details

from media_mgr.comms_utility import run_cmd, is_server_active, group_list

from media_mgr.media_cfg import MediaConfig
from media_mgr.server_cfg import ServerConfig

from media_mgr.paths_and_drives import get_filtered_media_paths

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# 2025-0201
# Search for titles in search path lists on servers
# - search is performed with run_cmd / subprocess via ssh
# - search contents are retrieved in lists for display
# - only search titles matching regex are returned
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def extract_search_path_collection(ipv4: str | None = None,
                                   cmd: str | None = None,
                                   getAllGroups: bool = False,
                                   shell: bool = False,
                                   verbose: bool = False):
    collection = defaultdict(list)

    cmdOutput = run_cmd(ipv4, cmd, shell = shell)
    if isinstance(cmdOutput, subprocess.CompletedProcess):
        if cmdOutput.returncode:
            raise ValueError(f'Warning: Problem retrieving command output!')

    if verbose:
        # print(json.dumps(cmdOutput,indent=4))
        pass

    medium = list(group_list(cmdOutput, 'Drive.path: '))
    if verbose:
        # print(json.dumps(medium,indent=4))
        pass

    for drivePathContents in medium:
        if not drivePathContents:
            continue
        groupId, groupContents = drivePathContents[:1], drivePathContents[1:]
        groupIdStr=''
        for groupIdElement in groupId:
            groupIdStr += groupIdElement

        if not groupIdStr:
            continue
        dumpIt, groupLabel = groupIdStr.split(' ')
        if groupContents or getAllGroups:
            collection[groupLabel] = groupContents

    return collection

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_matching_items_in_search_paths(ipv4: str | None = None,
                                       searchPathList: list | None = None,
                                       searchTerms : list | None = None,
                                       verbose: bool = False):
    searchRegex = ''
    for term in searchTerms:
        searchRegex += term + '.*'

    if verbose:
        pass
        # print(json.dumps(searchPathList, indent = 4))
        # print(f'{searchRegex=}')

    cmd = ''
    for path in searchPathList:
        cmd += f'echo \"Drive.path: {path}\" ; ls --size -h {path} | grep -i \'{searchRegex}\' ; '

    return extract_search_path_collection(ipv4 = ipv4, cmd = cmd, shell = True, verbose = verbose)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def find_items_in_search_paths(ipv4: str | None = None,
                               serverType = 'plex',
                               searchPathList: list | None = None,
                               searchTerms: list | None = None,
                               verbose: bool = False):
    if ipv4:
        if not is_server_active(ipv4 = ipv4):
            return defaultdict(list)

    if not searchPathList:
        searchPathList = get_filtered_media_paths(ipv4 = ipv4, serverType = serverType)

    collection = get_matching_items_in_search_paths(ipv4 = ipv4,
                                                    searchPathList = searchPathList,
                                                    searchTerms = searchTerms,
                                                    verbose = verbose)
    '''
    if verbose:
        print(json.dumps(collection,indent=4))
        pass
    '''

    # create a matched dictionary list (titles by paths)
    # filtering paths with matching titles (no empty paths)
    matchedTitles = defaultdict(list)
    for path in collection:
        if collection[path]:
            for item in collection[path]:
                size, _, title = item.lstrip().partition(' ')
                entry = {}
                entry['size'] = size
                entry['title'] = title
                matchedTitles[path].append(entry)

    return matchedTitles

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
def get_num_titles(collection = None):
    numTitles = 0
    for path in collection:
        numTitles += len(collection[path])

    return numTitles

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def show_matched_titles(ipv4: str | None = None,
                        serverType = 'plex',
                        searchTerms: list = ["the", "duff"],
                        verbose: bool = False):

    location = str(ipv4) if ipv4 else "local machine"

    try:
        matchedTitles = find_items_in_search_paths(ipv4 = ipv4,
                                                   serverType = serverType,
                                                   searchTerms = searchTerms,
                                                   verbose = verbose)

    except Exception as e:
        print(f'{color.CRED2}-- Processing error: Search aborted for titles ' + \
                f'matching {color.CWHITE}--> {color.CYELLOW}{" ".join(searchTerms)}' + \
                f'{color.CWHITE}<-- {color.CRED2}on {color.CWHITE}{location}\n' + \
                f'{color.CRED}   Investigate {color.CWHITE}{location}{color.CRED2} ' + \
                f'for problems with drive mounts!{color.CEND}' + \
                f'\n{e}')
        exception_details(e, "find_item_in_search_paths run", raw=True)

        return

    print('')
    print('- ' * 50)

    if not matchedTitles:
        print(f'{color.CRED2}-- Did not find any titles matching ' + \
                f'{color.CWHITE}--> {color.CYELLOW}{" ".join(searchTerms)} ' + \
                f'{color.CWHITE}<-- {color.CRED2}on {color.CWHITE}{location}{color.CEND}')
        return

    mc = MediaConfig()
    print(f'{color.CGREEN}-- Found {color.CWHITE}{get_num_titles(matchedTitles)} ' + \
            f'{color.CGREEN}titles matching {color.CWHITE}--> {color.CYELLOW}' + \
            f'{" ".join(searchTerms)} {color.CWHITE}<-- {color.CGREEN}on ' + \
            f'{color.CWHITE}{location}{color.CEND}')

    if verbose:
        print(json.dumps(matchedTitles, indent = 4))
        return

    numMatchingTitles = 0
    for path in matchedTitles:
        _, colorCode = mc.get_color_label(os.path.basename(path))
        colorCode = colorCode if colorCode else color.CRED
        for entry in matchedTitles[path]:
            numMatchingTitles += 1
            print(f'{color.CWHITE}{numMatchingTitles:>3}. {colorCode}{path}/{entry["title"]}{color.CWHITE2} ' + \
                    f'({entry["size"]}){color.CEND}')

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def show_all_matched_titles(searchTerms: list | None = None,
                            verbose: bool = False):
    srv = ServerConfig()

    for server in srv.get_server_name_list():
        show_matched_titles(ipv4 = srv.get_server_address(serverLabel = server),
                            serverType = srv.get_server_type(serverLabel = server),
                            searchTerms = searchTerms,
                            verbose = verbose)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

