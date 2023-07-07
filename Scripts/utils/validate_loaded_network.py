import utils.log as log

def validate_loaded(network, fares=None):
    for line in network.transit_lines():
        if str(line.vehicle.mode) in "mr":
            segments = list(line.segments())
            for seg1,seg2 in zip(segments[:-1],segments[1:]):
                if seg1.data1 == 0 and (seg2.allow_boardings == 1 or seg2.allow_alightings ==1):
                    msg = "Segment id {} must not have zero speed if the next segment has boarding/alighting allowed".format(seg1.id)
                    log.error(msg)
                    raise ValueError(msg)
                if seg1.data1 != 0 and (seg2.allow_boardings == 0 and seg2.allow_alightings ==0):
                    msg = "Segment id {} must not have non-zero speed if the next segment has boarding/alighting disallowed".format(seg1.id)
                    log.error(msg)
                    raise ValueError(msg)