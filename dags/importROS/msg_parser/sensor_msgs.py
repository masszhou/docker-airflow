import numpy as np
import cv2
import sensor_msgs.point_cloud2 as pc2
from .registry import MSG_REGISTRY


@MSG_REGISTRY.register()
def parse_Image(msg):
    # msg
    # Out[8]:
    # header:
    #   seq: 17869
    #   stamp:
    #     secs: 0
    #     nsecs:         0
    #   frame_id: ''
    # height: 600
    # width: 960
    # encoding: "bayer_rggb8"
    # is_bigendian: 0
    # step: 960
    # data: [15, ...

    # topic -> '/camera/lane_detector'
    # msg.encoding -> bayer_rggb8 -> cv2.COLOR_BayerBG2BGR
    # t -> rospy.Time[1542980983382315965]
    # t.to_time() -> 1542980983.3823159
    # t.to_nsec() -> 1542980983382315965 int
    img_bayer = np.frombuffer(msg.data, dtype=np.uint8).reshape([msg.height, msg.width])
    img_rgb = cv2.cvtColor(img_bayer, cv2.COLOR_BayerBG2RGB)
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "height": msg.height,
            "width": msg.width,
            "encoding": msg.encoding,
            "is_bigendian": msg.is_bigendian,
            "step": msg.step,
            "data": img_rgb,
            }


@MSG_REGISTRY.register()
def parse_PointCloud2(msg):
    # msg
    # Out[14]:
    # header:
    #   seq: 2405
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 552577000
    #   frame_id: "velodyne"
    # height: 1
    # width: 47420
    # fields:
    #   -
    #     name: "x"
    #     offset: 0
    #     datatype: 7
    #     count: 1
    #   -
    #     name: "y"
    #     offset: 4
    #     datatype: 7
    #     count: 1
    #   -
    #     name: "z"
    #     offset: 8
    #     datatype: 7
    #     count: 1
    #   -
    #     name: "intensity"
    #     offset: 16
    #     datatype: 7
    #     count: 1
    #   -
    #     name: "ring"
    #     offset: 20
    #     datatype: 4
    #     count: 1
    # is_bigendian: False
    # point_step: 32
    # row_step: 1517440
    # data: [4, 146, 197, ...
    pts = pc2.read_points(msg)
    pts = np.array(list(pts))
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "height": msg.height,
            "width": msg.width,
            # "fields": msg.fields,  # type: List[Dict] fields are duplicated information for the same topic
            "is_bigendian": msg.is_bigendian,
            "point_step": msg.point_step,
            "row_step": msg.row_step,
            "data": pts,
            "is_dense": msg.is_dense,
            }


@MSG_REGISTRY.register()
def parse_Imu(msg):
    # msg
    # Out[50]:
    # header:
    #   seq: 66638
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 710593201
    #   frame_id: ''
    # orientation:
    #   x: -0.0017942248606739168
    #   y: 0.006801225219946978
    #   z: 0.9227752223730226
    #   w: 0.3852744645925494
    # orientation_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # angular_velocity:
    #   x: -0.0013962633674964309
    #   y: 0.0
    #   z: 0.0
    # angular_velocity_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # linear_acceleration:
    #   x: -0.09809999912977219
    #   y: 0.05886000022292137
    #   z: 9.790379524230957
    # linear_acceleration_covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "orientation": {"x": msg.orientation.x,
                            "y": msg.orientation.y,
                            "z": msg.orientation.z,
                            "w": msg.orientation.w},
            "orientation_covariance": msg.orientation_covariance,
            "angular_velocity": {"x": msg.angular_velocity.x,
                                 "y": msg.angular_velocity.y,
                                 "z": msg.angular_velocity.z},
            "angular_velocity_covariance": msg.angular_velocity_covariance,
            "linear_acceleration": {"x": msg.linear_acceleration.x,
                                    "y": msg.linear_acceleration.y,
                                    "z": msg.linear_acceleration.z},
            "linear_acceleration_covariance": msg.linear_acceleration_covariance
            }
