#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Charles Roydhouse <git@charlesr.me>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the <organization> nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# History:
# 2015-03-15
#    revision 1.0
#
# Usage: /fullwidth to convert text to fullwidth ('/help fullwidth' for help)

import re
import sys

import_ok = True
try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    import_ok = False

if sys.version_info[0] == 3:
        def unichr(i):
            return chr(i)

SCRIPT_NAME        = 'fullwidth'
SCRIPT_AUTHOR      = 'cer'
SCRIPT_VERSION     = '1.0'
SCRIPT_LICENSE     = 'BSD'
SCRIPT_DESC        = 'Convert text to fullwidth'


def fullwidth(input):
    FULLWIDTH_OFFSET = 65248
    output = [unichr(ord(c) + FULLWIDTH_OFFSET)
            if re.match(r'[A-Za-z0-9\-_+=,.:;|<>?!@#$%^&*()\'"\\/\[\]{}~`]', c)
            else c for c in input]
    return ''.join(output)


def fullwidth_cmd_cb(data, buffer, args):
    input = args.decode('UTF-8')
    input_method = 'command'
    if not input:
        input = weechat.buffer_get_string(buffer, 'input')
        input = input.decode('UTF-8')
        input_method = 'keybinding'

    output = fullwidth(input)

    if input_method == 'keybinding':
        weechat.buffer_set(buffer, 'input', output.encode('UTF-8'))
    else:
        weechat.command(buffer, output.encode('UTF-8'))
    return weechat.WEECHAT_RC_OK


if __name__ == '__main__':
    if import_ok:
        if weechat.register(SCRIPT_NAME,
                            SCRIPT_AUTHOR,
                            SCRIPT_VERSION,
                            SCRIPT_LICENSE,
                            SCRIPT_DESC,
                            '',
                            ''):
            weechat.hook_command('fullwidth',
                                 SCRIPT_DESC,
                                 'text',
                                 'text: text to be converted to fullwidth',
                                 '',
                                 'fullwidth_cmd_cb',
                                 '')
    else:
        print(fullwidth(' '.join(sys.argv[1:])))
