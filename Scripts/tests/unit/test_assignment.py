#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
from collections import namedtuple

import assignment.emme_bindings.mock_project as mock
from assignment.emme_assignment import EmmeAssignmentModel


class EmmeAssignmentTest(unittest.TestCase):
    def test_assignment(self):
        context = mock.MockProject()
        for scenario in context.modeller.emmebank.scenarios():
            network = scenario.get_network()
            for id in ('c', 'b'):
                network._modes[id] = mock.Mode(id)
            for id in range(1, 5):
                network._nodes[id] = mock.Node(id)
            for link in ((1, 2), (2, 3), (3, 4)):
                network._links[link] = mock.Link(*link, length=3.5)
            for id in range(1, 4):
                network._transit_lines[id] = mock.TransitLine(
                    id, network.mode('b'), headway=5)
            line = network.transit_line(1)
            line._segments.append(
                mock.TransitSegment(line, network.link(1, 2)))

        ass_model = EmmeAssignmentModel(context, 19)
        ass_model.prepare_network()
