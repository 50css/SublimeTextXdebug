"""
Status and feature management commands
"""
STATUS = 'status';
FEATURE_GET = 'feature_get';
FEATURE_SET = 'feature_set';


"""
Continuation commands
"""
RUN = 'run';
STEP_INTO = 'step_into';
STEP_OVER = 'step_over';
STEP_OUT = 'step_out';
STOP = 'stop';
DETACH = 'detach';


"""
Breakpoint commands
"""
BREAKPOINT_SET = 'breakpoint_set'
BREAKPOINT_GET = 'breakpoint_get'
BREAKPOINT_UPDATE = 'breakpoint_update'
BREAKPOINT_REMOVE = 'breakpoint_remove'
BREAKPOINT_LIST = 'breakpoint_list'


"""
Context/Stack commands
"""
CONTEXT_NAMES = 'context_names'
CONTEXT_GET = 'context_get'
STACK_DEPTH = 'stack-depth'
STACK_GET = 'stack_get'


"""
Status codes
"""
STATUS_STARTING = 'starting';
STATUS_STOPPING = 'stopping';
STATUS_STOPPED = 'stopped';
STATUS_RUNNING = 'running';
STATUS_BREAK = 'break';


"""
Reason codes
"""
REASON_OK = 'ok';
REASON_ERROR = 'error';
REASON_ABORTED = 'aborted';
REASON_EXCEPTION = 'exception';


"""
Response attributes/elements
"""
ATTRIBUTE_STATUS = 'status'
ATTRIBUTE_REASON = 'reason'
ELEMENT_INIT = 'init'
ELEMENT_BREAKPOINT = 'xdebug:message'
ELEMENT_PROPERTY = 'property'
ELEMENT_STACK = 'stack'


"""
Initialization attributes
"""
INIT_APPID = 'appid'
INIT_IDEKEY = 'idekey'
INIT_SESSION = 'session'
INIT_THREAD = 'thread'
INIT_PARENT = 'parent'
INIT_LANGUAGE = 'language'
INIT_PROTOCOL_VERSION = 'protocol_version'
INIT_FILEURI = 'fileuri'


"""
Breakpoint atrributes
"""
BREAKPOINT_TYPE = 'type'
BREAKPOINT_FILENAME = 'filename'
BREAKPOINT_LINENO = 'lineno'
BREAKPOINT_STATE = 'state'
BREAKPOINT_FUNCTION = 'function'
BREAKPOINT_TEMPORARY = 'temporary'
BREAKPOINT_HIT_COUNT = 'hit_count'
BREAKPOINT_HIT_VALUE = 'hit_value'
BREAKPOINT_HIT_CONDITION = 'hit_condition'
BREAKPOINT_EXCEPTION = 'exception'
BREAKPOINT_EXPRESSION = 'expression'


"""
Property attributes
"""
PROPERTY_NAME = 'name'
PROPERTY_FULLNAME = 'fullname'
PROPERTY_CLASSNAME = 'classname'
PROPERTY_PAGE = 'page'
PROPERTY_PAGESIZE = 'pagesize'
PROPERTY_TYPE = 'type'
PROPERTY_FACET = 'facet'
PROPERTY_SIZE = 'size'
PROPERTY_CHILDREN = 'children'
PROPERTY_NUMCHILDREN = 'numchildren'
PROPERTY_KEY = 'key'
PROPERTY_ADDRESS = 'address'
PROPERTY_ENCODING = 'encoding'


"""
Stack attributes
"""
STACK_LEVEL = 'level'
STACK_TYPE = 'type'
STACK_FILENAME = 'filename'
STACK_LINENO = 'lineno'
STACK_WHERE = 'where'
STACK_CMDBEGIN = 'cmdbegin'
STACK_CMDEND = 'cmdend'