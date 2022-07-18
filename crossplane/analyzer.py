# -*- coding: utf-8 -*-
from .errors import (
    NgxParserDirectiveUnknownError,
    NgxParserDirectiveContextError,
    NgxParserDirectiveArgumentsError
)

# bit masks for different directive argument styles
NGX_ARGS_NOARGS = 0x00000001  # 0 args
NGX_ARGS_TAKE1  = 0x00000002  # 1 args
NGX_ARGS_TAKE2  = 0x00000004  # 2 args
NGX_ARGS_TAKE3  = 0x00000008  # 3 args
NGX_ARGS_TAKE4  = 0x00000010  # 4 args
NGX_ARGS_TAKE5  = 0x00000020  # 5 args
NGX_ARGS_TAKE6  = 0x00000040  # 6 args
NGX_ARGS_TAKE7  = 0x00000080  # 7 args
NGX_ARGS_BLOCK  = 0x00000100  # followed by block
NGX_ARGS_FLAG   = 0x00000200  # 'on' or 'off'
NGX_ARGS_ANY    = 0x00000400  # >=0 args
NGX_ARGS_1MORE  = 0x00000800  # >=1 args
NGX_ARGS_2MORE  = 0x00001000  # >=2 args

# some helpful argument style aliases
NGX_ARGS_TAKE12   = (NGX_ARGS_TAKE1 | NGX_ARGS_TAKE2)
NGX_ARGS_TAKE13   = (NGX_ARGS_TAKE1 | NGX_ARGS_TAKE3)
NGX_ARGS_TAKE23   = (NGX_ARGS_TAKE2 | NGX_ARGS_TAKE3)
NGX_ARGS_TAKE34   = (NGX_ARGS_TAKE3 | NGX_ARGS_TAKE4)
NGX_ARGS_TAKE123  = (NGX_ARGS_TAKE12 | NGX_ARGS_TAKE3)
NGX_ARGS_TAKE1234 = (NGX_ARGS_TAKE123 | NGX_ARGS_TAKE4)

# bit masks for different directive locations
NGX_DIRECT_CONF      = 0x00000001  # main file (not used)
NGX_MAIN_CONF        = 0x00000002  # main context
NGX_EVENT_CONF       = 0x00000004  # events
NGX_MAIL_MAIN_CONF   = 0x00000008  # mail
NGX_MAIL_SRV_CONF    = 0x00000010  # mail > server
NGX_STREAM_MAIN_CONF = 0x00000020  # stream
NGX_STREAM_MAP_CONF  = 0x00000040  # stream > map
NGX_STREAM_SRV_CONF  = 0x00000080  # stream > server
NGX_STREAM_UPS_CONF  = 0x00000100  # stream > upstream
NGX_HTTP_MAIN_CONF   = 0x00000200  # http
NGX_HTTP_MAP_CONF    = 0x00000400  # http > map
NGX_HTTP_SRV_CONF    = 0x00000800  # http > server
NGX_HTTP_LOC_CONF    = 0x00001000  # http > location
NGX_HTTP_TYP_CONF    = 0x00002000  # http > types
NGX_HTTP_UPS_CONF    = 0x00004000  # http > upstream
NGX_HTTP_SIF_CONF    = 0x00008000  # http > server > if
NGX_HTTP_STY_CONF    = 0x00010000  # http > server > types
NGX_HTTP_LIF_CONF    = 0x00020000  # http > location > if
NGX_HTTP_LMT_CONF    = 0x00040000  # http > location > limit_except
NGX_HTTP_LTY_CONF    = 0x00080000  # http > location > types

# helpful directive location alias describing "any" context
# doesn't include NGX_HTTP_SIF_CONF, NGX_HTTP_LIF_CONF, NGX_HTTP_LMT_CONF,
# NGX_STREAM_MAP_CONF, NGX_HTTP_MAP_CONF, NGX_HTTP_TYP_CONF, NGX_HTTP_STY_CONF,
# or NGX_HTTP_LTY_CONF
NGX_ANY_CONF = (
    NGX_MAIN_CONF | NGX_EVENT_CONF | NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF |
    NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF | NGX_STREAM_UPS_CONF |
    NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_UPS_CONF
)

# directive location alias describing any "map" context
NGX_ANY_MAP = NGX_STREAM_MAP_CONF | NGX_HTTP_MAP_CONF

# directive location alias describing any "types" context
NGX_ANY_TYPES = NGX_HTTP_TYP_CONF | NGX_HTTP_STY_CONF | NGX_HTTP_LTY_CONF

# directive location alias describing any context in which arbitrary directive
# names are permitted
NGX_ANY_DIRECTIVE = NGX_ANY_MAP | NGX_ANY_TYPES

"""
DIRECTIVES
~~~~~~~~~~
This dict maps directives to lists of bit masks that define their behavior.

Each bit mask describes these behaviors:
  - how many arguments the directive can take
  - whether or not it is a block directive
  - whether this is a flag (takes one argument that's either "on" or "off")
  - which contexts it's allowed to be in

Since some directives can have different behaviors in different contexts, we
  use lists of bit masks, each describing a valid way to use the directive.

Definitions for directives that're available in the open source version of 
  nginx were taken directively from the source code. In fact, the variable
  names for the bit masks defined above were taken from the nginx source code.

Definitions for directives that're only available for nginx+ were inferred
  from the documentation at http://nginx.org/en/docs/.
"""
DIRECTIVES = {
    'absolute_redirect': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'accept_mutex': [
        {
            'ctx': NGX_EVENT_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'accept_mutex_delay': [
        {
            'ctx': NGX_EVENT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'access_log': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'add_after_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'add_before_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'add_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE23,
        },
    ],
    'add_trailer': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE23,
        },
    ],
    'addition_types': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'aio': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'aio_write': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'alias': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'allow': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ancient_browser': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'ancient_browser_value': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_basic': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_basic_user_file': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_http': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_http_header': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'auth_http_pass_client_cert': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'auth_http_timeout': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_request': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_request_set': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'autoindex': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'autoindex_exact_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'autoindex_format': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'autoindex_localtime': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'break': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_SIF_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'charset': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'charset_map': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE2,
        },
    ],
    'charset_types': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'chunked_transfer_encoding': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'client_body_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'client_body_in_file_only': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'client_body_in_single_buffer': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'client_body_temp_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
    ],
    'client_body_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'client_header_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'client_header_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'client_max_body_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'connection_pool_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'create_full_put_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'daemon': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'dav_access': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE123,
        },
    ],
    'dav_methods': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'debug_connection': [
        {
            'ctx': NGX_EVENT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'debug_points': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'default': [
        {
            'ctx': NGX_ANY_MAP,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'default_type': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'deny': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'directio': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'directio_alignment': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'disable_symlinks': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'empty_gif': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'env': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'error_log': [
        {
            'ctx': NGX_MAIN_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'error_page': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'etag': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'events': [
        {
            'ctx': NGX_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
    ],
    'expires': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'fastcgi_bind': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'fastcgi_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'fastcgi_busy_buffers_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache_background_update': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_cache_bypass': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'fastcgi_cache_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache_lock': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_cache_lock_age': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache_lock_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache_max_range_offset': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache_methods': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'fastcgi_cache_min_uses': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'fastcgi_cache_revalidate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_cache_use_stale': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'fastcgi_cache_valid': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'fastcgi_catch_stderr': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_connect_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_force_ranges': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_hide_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_ignore_client_abort': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_ignore_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'fastcgi_index': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_intercept_errors': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_keep_conn': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_limit_rate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_max_temp_file_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_next_upstream': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'fastcgi_next_upstream_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_next_upstream_tries': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_no_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'fastcgi_param': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE23,
        },
    ],
    'fastcgi_pass': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_pass_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_pass_request_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_pass_request_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_read_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_request_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_send_lowat': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_send_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_socket_keepalive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'fastcgi_split_path_info': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_store': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_store_access': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE123,
        },
    ],
    'fastcgi_temp_file_write_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_temp_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
    ],
    'flv': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'geo': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE12,
        },
    ],
    'geoip_city': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'geoip_country': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'geoip_org': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'geoip_proxy': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'geoip_proxy_recursive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'google_perftools_profiles': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_bind': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'grpc_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_connect_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_hide_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ignore_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'grpc_intercept_errors': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'grpc_next_upstream': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'grpc_next_upstream_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_next_upstream_tries': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_pass': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_pass_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_read_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_send_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_set_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'grpc_socket_keepalive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'grpc_ssl_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ssl_certificate_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ssl_ciphers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ssl_crl': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ssl_name': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ssl_password_file': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ssl_protocols': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'grpc_ssl_server_name': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'grpc_ssl_session_reuse': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'grpc_ssl_trusted_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'grpc_ssl_verify': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'grpc_ssl_verify_depth': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'gunzip': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'gunzip_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'gzip': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'gzip_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'gzip_comp_level': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'gzip_disable': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'gzip_http_version': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'gzip_min_length': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'gzip_proxied': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'gzip_static': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'gzip_types': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'gzip_vary': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'hash': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_UPS_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'hostnames': [
        {
            'ctx': NGX_ANY_MAP,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'http': [
        {
            'ctx': NGX_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
    ],
    'http2_body_preread_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_chunk_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_idle_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_max_concurrent_pushes': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_max_concurrent_streams': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_max_field_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_max_header_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_max_requests': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_push': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_push_preload': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'http2_recv_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'http2_recv_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'if': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_1MORE,
        },
    ],
    'if_modified_since': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ignore_invalid_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'image_filter': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE123,
        },
    ],
    'image_filter_buffer': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'image_filter_interlace': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'image_filter_jpeg_quality': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'image_filter_sharpen': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'image_filter_transparency': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'image_filter_webp_quality': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'imap_auth': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'imap_capabilities': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'imap_client_buffer': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'include': [
        {
            'ctx': NGX_ANY_CONF | NGX_ANY_MAP,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'index': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'internal': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'ip_hash': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'keepalive': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'keepalive_disable': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'keepalive_requests': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'keepalive_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'large_client_header_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'least_conn': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
        {
            'ctx': NGX_STREAM_UPS_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'limit_conn': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'limit_conn_dry_run': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_conn_log_level': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_conn_status': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_conn_zone': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'limit_except': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_1MORE,
        },
    ],
    'limit_rate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_rate_after': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_req': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE123,
        },
    ],
    'limit_req_dry_run': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_req_log_level': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_req_status': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'limit_req_zone': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE34,
        },
    ],
    'lingering_close': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'lingering_time': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'lingering_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'listen': [
        {
            'ctx': NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'load_module': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'location': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE12,
        },
    ],
    'lock_file': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'log_format': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'log_not_found': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'log_subrequest': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'mail': [
        {
            'ctx': NGX_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
    ],
    'map': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE2,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE2,
        },
    ],
    'map_hash_bucket_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'map_hash_max_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'master_process': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'max_ranges': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_bind': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'memcached_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_connect_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_gzip_flag': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_next_upstream': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'memcached_next_upstream_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_next_upstream_tries': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_pass': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_read_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_send_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'memcached_socket_keepalive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'merge_slashes': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'min_delete_depth': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'mirror': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'mirror_request_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'modern_browser': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'modern_browser_value': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'mp4': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'mp4_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'mp4_max_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'msie_padding': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'msie_refresh': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'multi_accept': [
        {
            'ctx': NGX_EVENT_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'open_file_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'open_file_cache_errors': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'open_file_cache_min_uses': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'open_file_cache_valid': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'open_log_file_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
    ],
    'output_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'override_charset': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'pcre_jit': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'perl': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'perl_modules': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'perl_require': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'perl_set': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'pid': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'pop3_auth': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'pop3_capabilities': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'port_in_redirect': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'postpone_output': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'preread_buffer_size': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'preread_timeout': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'protocol': [
        {
            'ctx': NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_bind': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'proxy_buffer': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'proxy_busy_buffers_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cache_background_update': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_cache_bypass': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'proxy_cache_convert_head': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_cache_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cache_lock': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_cache_lock_age': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cache_lock_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cache_max_range_offset': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cache_methods': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'proxy_cache_min_uses': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cache_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'proxy_cache_revalidate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_cache_use_stale': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'proxy_cache_valid': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'proxy_connect_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_cookie_domain': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'proxy_cookie_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'proxy_download_rate': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_force_ranges': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_headers_hash_bucket_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_headers_hash_max_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_hide_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_http_version': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ignore_client_abort': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_ignore_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'proxy_intercept_errors': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_limit_rate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_max_temp_file_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_method': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_next_upstream': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_next_upstream_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_next_upstream_tries': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_no_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'proxy_pass': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_pass_error_message': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_pass_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_pass_request_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_pass_request_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_protocol': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_protocol_timeout': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_read_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_redirect': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'proxy_request_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_requests': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_responses': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_send_lowat': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_send_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_set_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_set_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'proxy_socket_keepalive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_ssl': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_ssl_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ssl_certificate_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ssl_ciphers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ssl_crl': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ssl_name': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ssl_password_file': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ssl_protocols': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'proxy_ssl_server_name': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_ssl_session_reuse': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_ssl_trusted_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_ssl_verify': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'proxy_ssl_verify_depth': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_store': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_store_access': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE123,
        },
    ],
    'proxy_temp_file_write_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_temp_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
    ],
    'proxy_timeout': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'proxy_upload_rate': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'random': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_NOARGS | NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_UPS_CONF,
            'arg': NGX_ARGS_NOARGS | NGX_ARGS_TAKE12,
        },
    ],
    'random_index': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'read_ahead': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'real_ip_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'real_ip_recursive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'recursive_error_pages': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'referer_hash_bucket_size': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'referer_hash_max_size': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'request_pool_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'reset_timedout_connection': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'resolver': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'resolver_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'return': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_SIF_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'rewrite': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_SIF_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE23,
        },
    ],
    'rewrite_log': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_SIF_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'root': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'satisfy': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_bind': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'scgi_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'scgi_busy_buffers_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_cache_background_update': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_cache_bypass': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'scgi_cache_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_cache_lock': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_cache_lock_age': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_cache_lock_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_cache_max_range_offset': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_cache_methods': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'scgi_cache_min_uses': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_cache_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'scgi_cache_revalidate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_cache_use_stale': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'scgi_cache_valid': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'scgi_connect_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_force_ranges': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_hide_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_ignore_client_abort': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_ignore_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'scgi_intercept_errors': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_limit_rate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_max_temp_file_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_next_upstream': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'scgi_next_upstream_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_next_upstream_tries': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_no_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'scgi_param': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE23,
        },
    ],
    'scgi_pass': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_pass_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_pass_request_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_pass_request_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_read_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_request_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_send_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_socket_keepalive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'scgi_store': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_store_access': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE123,
        },
    ],
    'scgi_temp_file_write_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'scgi_temp_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
    ],
    'secure_link': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'secure_link_md5': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'secure_link_secret': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'send_lowat': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'send_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'sendfile': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'sendfile_max_chunk': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'server': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
        {
            'ctx': NGX_STREAM_UPS_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'server_name': [
        {
            'ctx': NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'server_name_in_redirect': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'server_names_hash_bucket_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'server_names_hash_max_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'server_tokens': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'set': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_SIF_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'set_real_ip_from': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'slice': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'smtp_auth': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'smtp_capabilities': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'smtp_client_buffer': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'smtp_greeting_delay': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'source_charset': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'spdy_chunk_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'spdy_headers_comp': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'split_clients': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE2,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE2,
        },
    ],
    'ssi': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssi_last_modified': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssi_min_file_chunk': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssi_silent_errors': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssi_types': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'ssi_value_length': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssl_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_certificate_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_ciphers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_client_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_crl': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_dhparam': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_early_data': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssl_ecdh_curve': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_engine': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_handshake_timeout': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_password_file': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_prefer_server_ciphers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssl_preread': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssl_protocols': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'ssl_session_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'ssl_session_ticket_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_session_tickets': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssl_session_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_stapling': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssl_stapling_file': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_stapling_responder': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_stapling_verify': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'ssl_trusted_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_verify_client': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ssl_verify_depth': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'starttls': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'stream': [
        {
            'ctx': NGX_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
    ],
    'stub_status': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS | NGX_ARGS_TAKE1,
        },
    ],
    'sub_filter': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'sub_filter_last_modified': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'sub_filter_once': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'sub_filter_types': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'subrequest_output_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'tcp_nodelay': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'tcp_nopush': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'thread_pool': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE23,
        },
    ],
    'timeout': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'timer_resolution': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'try_files': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'types': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_NOARGS,
        },
    ],
    'types_hash_bucket_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'types_hash_max_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'underscores_in_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uninitialized_variable_warn': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_SIF_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'upstream': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE1,
        },
    ],
    'use': [
        {
            'ctx': NGX_EVENT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'user': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'userid': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'userid_domain': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'userid_expires': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'userid_mark': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'userid_name': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'userid_p3p': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'userid_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'userid_service': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_bind': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'uwsgi_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'uwsgi_busy_buffers_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache_background_update': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache_bypass': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_cache_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache_lock': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_cache_lock_age': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache_lock_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache_max_range_offset': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache_methods': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_cache_min_uses': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_cache_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'uwsgi_cache_revalidate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_cache_use_stale': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_cache_valid': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_connect_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_force_ranges': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_hide_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ignore_client_abort': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_ignore_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_intercept_errors': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_limit_rate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_max_temp_file_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_modifier1': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_modifier2': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_next_upstream': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_next_upstream_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_next_upstream_tries': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_no_cache': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_param': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE23,
        },
    ],
    'uwsgi_pass': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_pass_header': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_pass_request_body': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_pass_request_headers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_read_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_request_buffering': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_send_timeout': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_socket_keepalive': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_ssl_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ssl_certificate_key': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ssl_ciphers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ssl_crl': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ssl_name': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ssl_password_file': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ssl_protocols': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'uwsgi_ssl_server_name': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_ssl_session_reuse': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_ssl_trusted_certificate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_ssl_verify': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'uwsgi_ssl_verify_depth': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_store': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_store_access': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE123,
        },
    ],
    'uwsgi_temp_file_write_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'uwsgi_temp_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
    ],
    'valid_referers': [
        {
            'ctx': NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'variables_hash_bucket_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'variables_hash_max_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'volatile': [
        {
            'ctx': NGX_ANY_MAP,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'worker_aio_requests': [
        {
            'ctx': NGX_EVENT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'worker_connections': [
        {
            'ctx': NGX_EVENT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'worker_cpu_affinity': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'worker_priority': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'worker_processes': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'worker_rlimit_core': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'worker_rlimit_nofile': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'worker_shutdown_timeout': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'working_directory': [
        {
            'ctx': NGX_MAIN_CONF | NGX_DIRECT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'xclient': [
        {
            'ctx': NGX_MAIL_MAIN_CONF | NGX_MAIL_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'xml_entities': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'xslt_last_modified': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'xslt_param': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'xslt_string_param': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'xslt_stylesheet': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'xslt_types': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'zone': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_UPS_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],

    # nginx+ directives [definitions inferred from docs]
    'api': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS | NGX_ARGS_TAKE1,
        },
    ],
    'auth_jwt': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'auth_jwt_claim_set': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'auth_jwt_header_set': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'auth_jwt_key_file': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_jwt_key_request': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'auth_jwt_leeway': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'f4f': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'f4f_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'fastcgi_cache_purge': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'health_check': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_ANY,
        },
        {
            'ctx': NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_ANY,
        },
    ],
    'health_check_timeout': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'hls': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'hls_buffers': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'hls_forward_args': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'hls_fragment': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'hls_mp4_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'hls_mp4_max_buffer_size': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'js_access': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'js_content': [
        {
            'ctx': NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'js_filter': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'js_include': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'js_path': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'js_preread': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'js_set': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'keyval': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE3,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_TAKE3,
        },
    ],
    'keyval_zone': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_1MORE,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'least_time': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
        {
            'ctx': NGX_STREAM_UPS_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'limit_zone': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE3,
        },
    ],
    'match': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_MAIN_CONF,
            'arg': NGX_ARGS_BLOCK | NGX_ARGS_TAKE1,
        },
    ],
    'memcached_force_ranges': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'mp4_limit_rate': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'mp4_limit_rate_after': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'ntlm': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'proxy_cache_purge': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'queue': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'scgi_cache_purge': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'session_log': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'session_log_format': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_2MORE,
        },
    ],
    'session_log_zone': [
        {
            'ctx': NGX_HTTP_MAIN_CONF,
            'arg': NGX_ARGS_TAKE23 | NGX_ARGS_TAKE4 | NGX_ARGS_TAKE5 | NGX_ARGS_TAKE6,
        },
    ],
    'state': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_UPS_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'status': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'status_format': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'status_zone': [
        {
            'ctx': NGX_HTTP_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
        {
            'ctx': NGX_HTTP_LIF_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'sticky': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'sticky_cookie_insert': [
        {
            'ctx': NGX_HTTP_UPS_CONF,
            'arg': NGX_ARGS_TAKE1234,
        },
    ],
    'upstream_conf': [
        {
            'ctx': NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'uwsgi_cache_purge': [
        {
            'ctx': NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'zone_sync': [
        {
            'ctx': NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_NOARGS,
        },
    ],
    'zone_sync_buffers': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE2,
        },
    ],
    'zone_sync_connect_retry_interval': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_connect_timeout': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_interval': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_recv_buffer_size': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_server': [
        {
            'ctx': NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE12,
        },
    ],
    'zone_sync_ssl': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'zone_sync_ssl_certificate': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_ssl_certificate_key': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_ssl_ciphers': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_ssl_crl': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_ssl_name': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_ssl_password_file': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_ssl_protocols': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_1MORE,
        },
    ],
    'zone_sync_ssl_server_name': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'zone_sync_ssl_trusted_certificate': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_ssl_verify': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_FLAG,
        },
    ],
    'zone_sync_ssl_verify_depth': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
    'zone_sync_timeout': [
        {
            'ctx': NGX_STREAM_MAIN_CONF | NGX_STREAM_SRV_CONF,
            'arg': NGX_ARGS_TAKE1,
        },
    ],
}

# map for getting bitmasks from certain context tuples
CONTEXTS = {
    (): NGX_MAIN_CONF,
    ('events',): NGX_EVENT_CONF,
    ('mail',): NGX_MAIL_MAIN_CONF,
    ('mail', 'server'): NGX_MAIL_SRV_CONF,
    ('stream',): NGX_STREAM_MAIN_CONF,
    ('stream', 'map'): NGX_STREAM_MAP_CONF,
    ('stream', 'server'): NGX_STREAM_SRV_CONF,
    ('stream', 'upstream'): NGX_STREAM_UPS_CONF,
    ('http',): NGX_HTTP_MAIN_CONF,
    ('http', 'map'): NGX_HTTP_MAP_CONF,
    ('http', 'server'): NGX_HTTP_SRV_CONF,
    ('http', 'location'): NGX_HTTP_LOC_CONF,
    ('http', 'types'): NGX_HTTP_TYP_CONF,
    ('http', 'upstream'): NGX_HTTP_UPS_CONF,
    ('http', 'server', 'if'): NGX_HTTP_SIF_CONF,
    ('http', 'server', 'types'): NGX_HTTP_STY_CONF,
    ('http', 'location', 'if'): NGX_HTTP_LIF_CONF,
    ('http', 'location', 'limit_except'): NGX_HTTP_LMT_CONF,
    ('http', 'location', 'types'): NGX_HTTP_LTY_CONF,
}


def enter_block_ctx(stmt, ctx):
    # don't nest because NGX_HTTP_LOC_CONF just means "location block in http"
    if ctx and ctx[0] == 'http' and stmt['directive'] == 'location':
        return ('http', 'location')

    # no other block contexts can be nested like location so just append it
    return ctx + (stmt['directive'],)


def analyze(fname, stmt, term, ctx=(), strict=False, check_ctx=True,
        check_args=True):

    directive = stmt['directive']
    line = stmt['line']

    ctx_any_directive = ctx in CONTEXTS and NGX_ANY_DIRECTIVE & CONTEXTS[ctx]

    # if strict, context doesn't permit any directive and the directive isn't
    # known, throw error
    if strict and not ctx_any_directive and directive not in DIRECTIVES:
        reason = 'unknown directive "%s"' % directive
        raise NgxParserDirectiveUnknownError(reason, fname, line)

    # if we don't know where this directive is allowed and how
    # many arguments it can take then don't bother analyzing it
    if ctx not in CONTEXTS or (not ctx_any_directive and directive not in DIRECTIVES):
        return

    args = stmt.get('args') or []
    n_args = len(args)

    if directive in DIRECTIVES:
        masks = DIRECTIVES[directive]
    elif NGX_ANY_MAP & CONTEXTS[ctx]:
        # map blocks can have arbitrary directives with 1 argument
        masks = [{'ctx': NGX_ANY_MAP, 'arg': NGX_ARGS_1MORE}]
    elif NGX_ANY_TYPES & CONTEXTS[ctx]:
        # type blocks have arbitrary directives with 1 argument
        masks = [{'ctx': NGX_ANY_TYPES, 'arg': NGX_ARGS_1MORE}]
    else:
        masks = []

    # if this directive can't be used in this context then throw an error
    if check_ctx:
        masks = [mask for mask in masks if mask['ctx'] & CONTEXTS[ctx]]
        if not masks:
            reason = '"%s" directive is not allowed here' % directive
            raise NgxParserDirectiveContextError(reason, fname, line)

    if not check_args:
        return

    valid_flag = lambda x: x.lower() in ('on', 'off')

    # do this in reverse because we only throw errors at the end if no masks
    # are valid, and typically the first bit mask is what the parser expects
    for mask in reversed(masks):
        # if the directive isn't a block but should be according to the ctx mask
        if mask['arg'] & NGX_ARGS_BLOCK and term != '{':
            reason = 'directive "%s" has no opening "{"'
            continue

        # if the directive is a block but shouldn't be according to the arg mask
        if not mask['arg'] & NGX_ARGS_BLOCK and term != ';':
            reason = 'directive "%s" is not terminated by ";"'
            continue

        # use arg mask to check the directive's arguments
        if ((mask['arg'] >> n_args & 1 and n_args <= 7) or  # NOARGS to TAKE7
            (mask['arg'] & NGX_ARGS_FLAG and n_args == 1 and valid_flag(args[0])) or
            (mask['arg'] & NGX_ARGS_ANY and n_args >= 0) or
            (mask['arg'] & NGX_ARGS_1MORE and n_args >= 1) or
            (mask['arg'] & NGX_ARGS_2MORE and n_args >= 2)):
            return
        elif mask['arg'] & NGX_ARGS_FLAG and n_args == 1 and not valid_flag(args[0]):
            reason = 'invalid value "%s" in "%%s" directive, it must be "on" or "off"' % args[0]
        else:
            reason = 'invalid number of arguments in "%s" directive'

    raise NgxParserDirectiveArgumentsError(reason % directive, fname, line)


def register_external_directives(directives):
    for directive, bitmasks in directives.iteritems():
        if bitmasks:
            DIRECTIVES[directive] = bitmasks
