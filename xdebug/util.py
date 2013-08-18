import sublime

import json
import os
import re
import sys
import webbrowser

# Helper module
try:
    from .helper import H
except:
    from helper import H

# Settings variables
try:
    from . import settings as S
except:
    import settings as S

# Log module
from .log import debug, info


def get_real_path(uri, server=False):
    """
    Get real path

    Keyword arguments:
    uri -- Uri of file that needs to be mapped and located
    server -- Map local path to server path

    TODO: Fix mapping for root (/) and drive letters (P:/)
    """
    if uri is None:
        return uri

    # URLdecode uri
    uri = H.url_decode(uri)

    # Split scheme from uri to get absolute path
    try:
        # scheme:///path/file => scheme, /path/file
        # scheme:///C:/path/file => scheme, C:/path/file
        transport, filename = uri.split(':///', 1) 
    except:
        filename = uri

    # Normalize path for comparison and remove duplicate/trailing slashes
    uri = os.path.normpath(filename)

    # Pattern for checking if uri is a windows path
    drive_pattern = re.compile(r'^[a-zA-Z]:[\\/]')

    # Append leading slash if filesystem is not Windows
    if not drive_pattern.match(uri) and not os.path.isabs(uri):
        uri = os.path.normpath('/' + uri)

    path_mapping = S.get_project_value('path_mapping') or S.get_package_value('path_mapping')
    if not path_mapping is None:
        # Go through path mappings
        for server_path, local_path in path_mapping.items():
            server_path = os.path.normpath(server_path)
            local_path = os.path.normpath(local_path)
            # Replace path if mapping available
            if server:
                # Map local path to server path
                if local_path in uri:
                    uri = uri.replace(local_path, server_path)
                    break
            else:
                # Map server path to local path
                if server_path in uri:
                    uri = uri.replace(server_path, local_path)
                    break
    else:
        sublime.status_message("Xdebug: No path mapping defined, returning given path.")

    # Replace slashes
    if not drive_pattern.match(uri):
        uri = uri.replace("\\", "/")

    # Append scheme
    if server:
        return H.url_encode("file://" + uri)

    return uri


def get_region_icon(icon):
    # Default icons for color schemes from default theme
    default_current = 'bookmark'
    default_disabled = 'dot'
    default_enabled = 'circle'

    # Package icons (without .png extension)
    package_breakpoint_current = 'breakpoint_current'
    package_breakpoint_disabled = 'breakpoint_disabled'
    package_breakpoint_enabled = 'breakpoint_enabled'
    package_current_line = 'current_line'

    # List to check for duplicate icon entries
    icon_list = [default_current, default_disabled, default_enabled]

    # Determine icon path
    icon_path = None
    if S.PACKAGE_FOLDER is not None:
        if sublime.version() == '' or int(sublime.version()) > 3000:
            # ST3: Packages/Xdebug Client/icons/breakpoint_enabled.png
            icon_path = "Packages/" + S.PACKAGE_FOLDER + '/icons/{0}.png'
        else:
            # ST2: ../Xdebug Client/icons/breakpoint_enabled
            icon_path = "../" + S.PACKAGE_FOLDER + '/icons/{0}'
        # Append icon path to package icons
        package_breakpoint_current = icon_path.format(package_breakpoint_current)
        package_breakpoint_disabled = icon_path.format(package_breakpoint_disabled)
        package_breakpoint_enabled = icon_path.format(package_breakpoint_enabled)
        package_current_line = icon_path.format(package_current_line)
        # Add to duplicate list
        icon_list.append(icon_path.format(package_breakpoint_current))
        icon_list.append(icon_path.format(package_breakpoint_disabled))
        icon_list.append(icon_path.format(package_breakpoint_enabled))
        icon_list.append(icon_path.format(package_current_line))

    # Get user defined icons from settings
    breakpoint_current = S.get_project_value(S.KEY_BREAKPOINT_CURRENT) or S.get_package_value(S.KEY_BREAKPOINT_CURRENT)
    breakpoint_disabled = S.get_project_value(S.KEY_BREAKPOINT_DISABLED) or S.get_package_value(S.KEY_BREAKPOINT_DISABLED)
    breakpoint_enabled = S.get_project_value(S.KEY_BREAKPOINT_ENABLED) or S.get_package_value(S.KEY_BREAKPOINT_ENABLED)
    current_line = S.get_project_value(S.KEY_CURRENT_LINE) or S.get_package_value(S.KEY_CURRENT_LINE)

    # Duplicate check, enabled breakpoint
    if breakpoint_enabled not in icon_list:
        icon_list.append(breakpoint_enabled)
    else:
        breakpoint_enabled = None
    # Duplicate check, disabled breakpoint
    if breakpoint_disabled not in icon_list:
        icon_list.append(breakpoint_disabled)
    else:
        breakpoint_disabled = None
    # Duplicate check, current line
    if current_line not in icon_list:
        icon_list.append(current_line)
    else:
        current_line = None
    # Duplicate check, current breakpoint
    if breakpoint_current not in icon_list:
        icon_list.append(breakpoint_current)
    else:
        breakpoint_current = None

    # Use default/package icon if no user defined or duplicate detected
    if not breakpoint_current and icon_path is not None:
        breakpoint_current = package_breakpoint_current
    if not breakpoint_disabled:
        breakpoint_disabled = default_disabled if icon_path is None else package_breakpoint_disabled
    if not breakpoint_enabled:
        breakpoint_enabled = default_enabled if icon_path is None else package_breakpoint_enabled
    if not current_line:
        current_line = default_current if icon_path is None else package_current_line

    # Return icon for icon name
    if icon == S.KEY_CURRENT_LINE:
        return current_line
    elif icon == S.KEY_BREAKPOINT_CURRENT:
        return breakpoint_current
    elif icon == S.KEY_BREAKPOINT_DISABLED:
        return breakpoint_disabled
    elif icon == S.KEY_BREAKPOINT_ENABLED:
        return breakpoint_enabled
    else:
        info("Invalid icon name. (" + icon + ")")
        return


def launch_browser():
    url = S.get_project_value('url') or S.get_package_value('url')
    if not url:
        sublime.status_message('Xdebug: No URL defined in (project) settings file.')
        return
    ide_key = S.get_project_value('ide_key') or S.get_package_value('ide_key') or S.DEFAULT_IDE_KEY

    # Start debug session
    if S.SESSION and (S.SESSION.listening or not S.SESSION.connected):
        webbrowser.open(url + '?XDEBUG_SESSION_START=' + ide_key)
    # Stop debug session
    else:
        # Check if we should execute script
        browser_no_execute = S.get_project_value('browser_no_execute') or S.get_package_value('browser_no_execute')
        if browser_no_execute:
            # Without executing script
            webbrowser.open(url + '?XDEBUG_SESSION_STOP_NO_EXEC=' + ide_key)
        else:
            # Run script normally
            webbrowser.open(url + '?XDEBUG_SESSION_STOP=' + ide_key)


def load_breakpoint_data():
    data_path = os.path.join(sublime.packages_path(), 'User', S.FILE_BREAKPOINT_DATA)
    data = {}
    try:
        data_file = open(data_path, 'rb')
    except:
        e = sys.exc_info()[1]
        info('Failed to open %s.' % data_path)
        debug(e)

    try:
        data = json.loads(H.data_read(data_file.read()))
    except:
        e = sys.exc_info()[1]
        info('Failed to parse %s.' % data_path)
        debug(e)

    # Do not use deleted files or entries without breakpoints
    if data:
        for filename, breakpoint_data in data.copy().items():
            if not breakpoint_data or not os.path.isfile(filename):
                del data[filename]

    if not isinstance(S.BREAKPOINT, dict):
        S.BREAKPOINT = {}

    # Set breakpoint data
    S.BREAKPOINT.update(data)


def save_breakpoint_data():
    data_path = os.path.join(sublime.packages_path(), 'User', S.FILE_BREAKPOINT_DATA)
    with open(data_path, 'wb') as data:
        data.write(H.data_write(json.dumps(S.BREAKPOINT)))