# _*_ encoding: utf-8 _*_
__author__ = 'Phantom3389'
__date__ = '2018/3/12 15:12'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "tieba"])