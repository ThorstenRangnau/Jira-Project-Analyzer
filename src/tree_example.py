import argparse
import csv
import re

from architectural_smells.smell import Version, CyclicDependency, UnstableDependency, HubLikeDependency
from datetime import datetime
from treelib import Node, Tree

from duplicated_smell_filter import create_smell_evolution_trees


def date(date_string):
    return datetime.strptime(date_string, DATE_FORMATTER)

DATE_FORMATTER = '%Y-%m-%d'

smells = {
    1: [
        CyclicDependency(1, date('2014-08-11'), "v1", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.util'], 3, "DOES NOT MATTER"),
        CyclicDependency(2, date('2014-10-28'), "v2", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.util', 'org.apache.tajo.plan.logical', 'org.apache.tajo.plan.verifier'], 5, "DOES NOT MATTER"),
        CyclicDependency(3, date('2014-11-11'), "v3", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.util', 'org.apache.tajo.master.ha'], 4, "DOES NOT MATTER"),
        CyclicDependency(4, date('2014-10-25'), "v4", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.expr'], 5, "DOES NOT MATTER"),
        CyclicDependency(5, date('2014-11-21'), "v5", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.expr', 'org.apache.tajo.plan.logical'], 5, "DOES NOT MATTER"),
        CyclicDependency(6, date('2014-12-07'), "v6", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.expr', 'org.apache.tajo.plan.logical', 'org.apache.tajo.plan.verifier'], 7, "DOES NOT MATTER"),
        CyclicDependency(7, date('2015-01-23'), "v7", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.plan', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.expr', 'org.apache.tajo.plan.logical'], 6, "DOES NOT MATTER"),
        CyclicDependency(8, date('2015-01-23'), "v8", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.plan', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.expr', 'org.apache.tajo.plan.logical', 'org.apache.tajo.plan.verifier', 'org.apache.tajo.plan.visitor'], 6, "DOES NOT MATTER"),
        CyclicDependency(9, date('2015-01-23'), "v9", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.plan', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.algebra', 'org.apache.tajo.plan.expr', 'org.apache.tajo.plan.logical', 'org.apache.tajo.plan.verifier', 'org.apache.tajo.plan.visitor'], 3, "DOES NOT MATTER"),
        CyclicDependency(10, date('2015-01-09'), "v10", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.ha', 'org.apache.tajo.util'], 3, "DOES NOT MATTER"),
        CyclicDependency(11, date('2015-09-14'), "v11", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.exception', 'org.apache.tajo.util'], 3, "DOES NOT MATTER"),
        CyclicDependency(12, date('2016-05-19'), "v12", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.exception', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.expr', 'org.apache.tajo.plan.function.python'], 3, "DOES NOT MATTER"),
        CyclicDependency(13, date('2016-05-16'), "v13", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.exception', 'org.apache.tajo.plan', 'org.apache.tajo.util', 'org.apache.tajo.plan.logical', 'org.apache.tajo.plan.verifier'], 3, "DOES NOT MATTER"),
        CyclicDependency(14, date('2016-08-28'), "v14", ['org.apache.tajo', 'org.apache.tajo.conf', 'org.apache.tajo.exception', 'org.apache.tajo.plan', 'org.apache.tajo.storage', 'org.apache.tajo.util', 'org.apache.tajo.plan.expr', 'org.apache.tajo.plan.logical'], 3, "DOES NOT MATTER")
    ]
}

create_smell_evolution_trees(smells, None)
