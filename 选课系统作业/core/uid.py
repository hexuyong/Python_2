#-*- coding:UTF-8 -*-
# author:hexy
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#version:3.5.2
#author:wangeq

import hashlib
import time

def create_md():
    m = hashlib.md5()
    m.update(bytes(str(time.time()),encoding='utf-8'))
    return m.hexdigest()