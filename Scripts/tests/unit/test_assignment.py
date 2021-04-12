#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
import numpy

import assignment.emme_bindings.mock_project as mock
from assignment.emme_assignment import EmmeAssignmentModel


class EmmeAssignmentTest(unittest.TestCase):
    def test_assignment(self):
        context = mock.MockProject()
        for scenario in context.modeller.emmebank.scenarios():
            network = scenario.get_network()
            for idx in ('c', 'b'):
                network._modes[idx] = mock.Mode(idx)
            for idx in (101, 4003, 16001, 16002):
                network.create_node(idx, is_centroid=True)
                network.node(idx).label = 'A'
            for idx in range(1, 5):
                network.create_node(idx)
                network.node(idx).label = 'A'
            for link in ((1, 2), (2, 3), (3, 4)):
                network._links[link] = mock.Link(network, *link, length=3.5)
            for idx in range(1, 4):
                network._transit_lines[idx] = mock.TransitLine(
                    network, idx, network.mode('b'), headway=5)
            mock.TransitSegment(
                network, network.transit_line(1), network.link(1, 2))

        ass_model = EmmeAssignmentModel(context, 19)
        ass_model.prepare_network()
        fares = {
            "fare": {
                'A': 59,
            },
            "exclusive": {},
            "dist_fare": 3.0,
            "start_fare": 35,
        }
        peripheral_cost = numpy.arange(8).reshape((2, 4))
        ass_model.calc_transit_cost(fares, peripheral_cost)
