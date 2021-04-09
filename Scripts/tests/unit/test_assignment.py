#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
from collections import namedtuple

from assignment.emme_bindings.mock_project import MockProject
from assignment.emme_assignment import EmmeAssignmentModel


class EmmeAssignmentTest(unittest.TestCase):
    def test_assignment(self):
        context = MockProject()
        ass_model = EmmeAssignmentModel(context, 19)
        ass_model.prepare_network()
