from .registry import MSG_REGISTRY


@MSG_REGISTRY.register()
def parse_GPSFix(msg):
    # msg
    # Out[52]:
    # header:
    #   seq: 66646
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 790599246
    #   frame_id: ''
    # status:
    #   header:
    #     seq: 0
    #     stamp:
    #       secs: 0
    #       nsecs:         0
    #     frame_id: ''
    #   satellites_used: 14
    #   satellite_used_prn: []
    #   satellites_visible: 14
    #   satellite_visible_prn: []
    #   satellite_visible_z: []
    #   satellite_visible_azimuth: []
    #   satellite_visible_snr: []
    #   status: 18
    #   motion_source: 0
    #   orientation_source: 0
    #   position_source: 0
    # latitude: 51.1015199
    # longitude: 13.925647699999999
    # altitude: 251.06
    # track: 134.68
    # speed: -0.004999999888241291
    # climb: 0.0
    # pitch: 0.0
    # roll: 0.0
    # dip: 0.0
    # time: 1592476949.65
    # gdop: 0.0
    # pdop: 0.0
    # hdop: 0.0
    # vdop: 0.0
    # tdop: 0.0
    # err: 0.0
    # err_horz: 0.01131370849898476
    # err_vert: 0.0
    # err_track: 0.0
    # err_speed: 0.0
    # err_climb: 0.0
    # err_time: 0.0
    # err_pitch: 0.0
    # err_roll: 0.0
    # err_dip: 0.0
    # position_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # position_covariance_type: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "status": {"header": {"seq": msg.status.header.seq,
                                  "stamp": {"secs": msg.status.header.stamp.secs,
                                            "nsecs": msg.status.header.stamp.nsecs},
                                  "frame_id": msg.status.header.frame_id,},
                       "satellites_used": msg.status.satellites_used,
                       "satellite_used_prn": msg.status.satellite_used_prn,
                       "satellites_visible": msg.status.satellites_visible,
                       "satellite_visible_prn": msg.status.satellite_visible_prn,
                       "satellite_visible_z": msg.status.satellite_visible_z,
                       "satellite_visible_azimuth": msg.status.satellite_visible_azimuth,
                       "satellite_visible_snr": msg.status.satellite_visible_snr,
                       "status": msg.status.status,
                       "motion_source": msg.status.motion_source,
                       "orientation_source": msg.status.orientation_source,
                       "position_source": msg.status.position_source,
                       },
            "latitude": msg.latitude,
            "longitude": msg.longitude,
            "altitude": msg.altitude,
            "track": msg.track,
            "speed": msg.speed,
            "climb": msg.climb,
            "pitch": msg.pitch,
            "roll": msg.roll,
            "dip": msg.dip,
            "time": msg.time,
            "gdop": msg.gdop,
            "pdop": msg.pdop,
            "hdop": msg.hdop,
            "vdop": msg.vdop,
            "tdop": msg.tdop,
            "err": msg.err,
            "err_horz": msg.err_horz,
            "err_vert": msg.err_vert,
            "err_track": msg.err_track,
            "err_speed": msg.err_speed,
            "err_climb": msg.err_climb,
            "err_time": msg.err_time,
            "err_pitch": msg.err_pitch,
            "err_roll": msg.err_roll,
            "err_dip": msg.err_dip,
            "position_covariance": msg.position_covariance,
            "position_covariance_type": msg.position_covariance_type,
            }
