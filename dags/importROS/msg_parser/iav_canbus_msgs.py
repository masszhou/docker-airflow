from .registry import MSG_REGISTRY


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x1(msg):
    # msg
    # Out[56]:
    # header:
    #   seq: 33768
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 658448979
    #   frame_id: ''
    # CRC: 10
    # Counter: 1
    # LateralAcceleration: -9.313225746154785e-09
    # LongitudinalAcceleration: -0.125
    # VehicleVelocity: 0.0
    # YawRate: 0.26999998092651367
    # YawRateSign: 1
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "LateralAcceleration": msg.LateralAcceleration,
            "LongitudinalAcceleration": msg.LongitudinalAcceleration,
            "VehicleVelocity": msg.VehicleVelocity,
            "YawRate": msg.YawRate,
            "YawRateSign": msg.YawRateSign
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x2(msg):
    # msg
    # Out[59]:
    # header:
    #   seq: 33768
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 658460210
    #   frame_id: ''
    # CRC: 160
    # Counter: 1
    # SteeringWheelAngle: 1.7000000476837158
    # SteeringWheelAngleSign: 0
    # SteeringWheelSpeed: 0.0
    # SteeringWheelSpeedSign: 0
    # SteeringWheelTorque: 0.07000000029802322
    # SteeringWheelTorqueSign: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "SteeringWheelAngle": msg.SteeringWheelAngle,
            "SteeringWheelAngleSign": msg.SteeringWheelAngleSign,
            "SteeringWheelSpeed": msg.SteeringWheelSpeed,
            "SteeringWheelSpeedSign": msg.SteeringWheelSpeedSign,
            "SteeringWheelTorque": msg.SteeringWheelTorque,
            "SteeringWheelTorqueSign": msg.SteeringWheelTorqueSign,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x21(msg):
    # msg
    # Out[62]:
    # header:
    #   seq: 6750
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 360973398
    #   frame_id: ''
    # CRC: 245
    # Counter: 10
    # Curvature: 1.7301499610766768e-07
    # CurvatureRate: 1.4523493518936448e-09
    # OffsetLateral: 0.0
    # YawAngle: -5.364418029785156e-07
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "Curvature": msg.Curvature,
            "CurvatureRate": msg.CurvatureRate,
            "OffsetLateral": msg.OffsetLateral,
            "YawAngle": msg.YawAngle,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x22(msg):
    # msg
    # Out[58]:
    # header:
    #   seq: 6750
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 360982961
    #   frame_id: ''
    # CRC: 210
    # Counter: 10
    # Camera_x_Position: -0.9736325740814209
    # Camera_y_Position: 9.5367431640625e-07
    # Color: 0
    # MaxDistanceLongitudinal: 0.0
    # OffsetLongitudinal: 0.0
    # TypeVar: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "Camera_x_Position": msg.Camera_x_Position,
            "Camera_y_Position": msg.Camera_y_Position,
            "Color": msg.Color,
            "MaxDistanceLongitudinal": msg.MaxDistanceLongitudinal,
            "OffsetLongitudinal": msg.OffsetLongitudinal,
            "TypeVar": msg.TypeVar,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x24(msg):
    # msg
    # Out[64]:
    # header:
    #   seq: 6750
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 361000006
    #   frame_id: ''
    # CRC: 10
    # Counter: 10
    # Color: 0
    # MaxDistanceLongitudinal: 0.0
    # OffsetLongitudinal: 0.0
    # TypeVar: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "Color": msg.Color,
            "MaxDistanceLongitudinal": msg.MaxDistanceLongitudinal,
            "OffsetLongitudinal": msg.OffsetLongitudinal,
            "TypeVar": msg.TypeVar,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x3(msg):
    # msg
    # Out[67]:
    # header:
    #   seq: 33764
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 594943859
    #   frame_id: ''
    # CRC: 194
    # Counter: 13
    # DriverDoor: 1
    # PassengerDoor: 1
    # RearDriverDoor: 1
    # RearPassengerDoor: 1
    # DriverSeatbelt: 3
    # PassengerSeatbelt: 2
    # RearDriverSeatbelt: 2
    # RearPassengerSeatbelt: 2
    # RearMiddleSeatbelt: 2
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "DriverDoor": msg.DriverDoor,
            "PassengerDoor": msg.PassengerDoor,
            "RearDriverDoor": msg.RearDriverDoor,
            "RearPassengerDoor": msg.RearPassengerDoor,
            "DriverSeatbelt": msg.DriverSeatbelt,
            "PassengerSeatbelt": msg.PassengerSeatbelt,
            "RearDriverSeatbelt": msg.RearDriverSeatbelt,
            "RearPassengerSeatbelt": msg.RearPassengerSeatbelt,
            "RearMiddleSeatbelt": msg.RearMiddleSeatbelt,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x31(msg):
    # msg
    # Out[70]:
    # header:
    #   seq: 16889
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 815399924
    #   frame_id: ''
    # CRC: 171
    # Counter: 11
    # FusedState: False
    # ID: 0
    # RelPosX: 0.0
    # RelPosY: 0.0
    # RelVelocityX: 0.0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "FusedState": msg.FusedState,
            "ID": msg.ID,
            "RelPosX": msg.RelPosX,
            "RelPosY": msg.RelPosY,
            "RelVelocityX": msg.RelVelocityX,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x4(msg):
    # msg
    # Out[76]:
    # header:
    #   seq: 67533
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 636155882
    #   frame_id: ''
    # CRC: 51
    # Counter: 14
    # EngineSpeed: 749.5
    # EngineTorque: 0.0
    # Gear: 8
    # ThrottlePedalPos: 0.0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "EngineSpeed": msg.EngineSpeed,
            "EngineTorque": msg.EngineTorque,
            "Gear": msg.Gear,
            "ThrottlePedalPos": msg.ThrottlePedalPos,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x41(msg):
    # msg
    # Out[79]:
    # header:
    #   seq: 33775
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 797507511
    #   frame_id: ''
    # CRC: 251
    # Counter: 8
    # RearID: 0
    # RearPosX: 25.25
    # RearPosY: 15.875
    # RearRelVelocityX: 90.25
    # RearTracked: False
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "RearID": msg.RearID,
            "RearPosX": msg.RearPosX,
            "RearPosY": msg.RearPosY,
            "RearRelVelocityX": msg.RearRelVelocityX,
            "RearTracked": msg.RearTracked,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x5(msg):
    # msg
    # Out[82]:
    # header:
    #   seq: 33767
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 653677708
    #   frame_id: ''
    # CRC: 164
    # Counter: 0
    # DimmedHeadlights: False
    # DriverBraking: True
    # ExteriorLightSensor: 6126.0
    # ExteriorRainSensor: 0.0
    # ExteriorTemperature: 23.5
    # FogLightFront: False
    # FogLightRear: False
    # HighBeam: False
    # Horn: False
    # Odometer: 15434.0
    # TurnIndicatorsLeft: False
    # TurnIndicatorsRight: False
    # WheelPressureState: False
    # Wipers: False
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "DimmedHeadlights": msg.DimmedHeadlights,
            "DriverBraking": msg.DriverBraking,
            "ExteriorLightSensor": msg.ExteriorLightSensor,
            "ExteriorRainSensor": msg.ExteriorRainSensor,
            "ExteriorTemperature": msg.ExteriorTemperature,
            "FogLightFront": msg.FogLightFront,
            "FogLightRear": msg.FogLightRear,
            "HighBeam": msg.HighBeam,
            "Horn": msg.Horn,
            "Odometer": msg.Odometer,
            "TurnIndicatorsLeft": msg.TurnIndicatorsLeft,
            "TurnIndicatorsRight": msg.TurnIndicatorsRight,
            "WheelPressureState": msg.WheelPressureState,
            "Wipers": msg.Wipers,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x53(msg):
    # msg
    # Out[85]:
    # header:
    #   seq: 33776
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 815443859
    #   frame_id: ''
    # CRC: 249
    # Counter: 9
    # USSRearLeft: 511.0
    # USSRearLeftMiddle: 511.0
    # USSRearRight: 511.0
    # USSRearRightMiddle: 511.0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "USSRearLeft": msg.USSRearLeft,
            "USSRearLeftMiddle": msg.USSRearLeftMiddle,
            "USSRearRight": msg.USSRearRight,
            "USSRearRightMiddle": msg.USSRearRightMiddle,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x54(msg):
    # msg
    # Out[88]:
    # header:
    #   seq: 33761
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 518037220
    #   frame_id: ''
    # CRC: 250
    # Counter: 10
    # USSFrontLeft: 511.0
    # USSFrontLeftMiddle: 511.0
    # USSFrontRight: 511.0
    # USSFrontRightMiddle: 511.0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "USSFrontLeft": msg.USSFrontLeft,
            "USSFrontLeftMiddle": msg.USSFrontLeftMiddle,
            "USSFrontRight": msg.USSFrontRight,
            "USSFrontRightMiddle": msg.USSFrontRightMiddle,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x55(msg):
    # msg
    # Out[91]:
    # header:
    #   seq: 33761
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 518060387
    #   frame_id: ''
    # CRC: 214
    # Counter: 10
    # USSFrontLeftSide: 511.0
    # USSFrontRightSide: 511.0
    # USSRearLeftSide: 511.0
    # USSRearRightSide: 166.0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "USSFrontLeftSide": msg.USSFrontLeftSide,
            "USSFrontRightSide": msg.USSFrontRightSide,
            "USSRearLeftSide": msg.USSRearLeftSide,
            "USSRearRightSide": msg.USSRearRightSide,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x6(msg):
    # msg
    # Out[94]:
    # header:
    #   seq: 33767
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 653689207
    #   frame_id: ''
    # CRC: 8
    # Counter: 0
    # ABSstate: False
    # ACCmainSwitch: False
    # ACCrequest: 3.0149998664855957
    # ACCresumeButton: False
    # ACCsetButton: False
    # ACCstate: 2
    # ASRstate: False
    # EPBstate: 0
    # ESCstate: False
    # FDstate: False
    # FrontAssistIntervention: 0
    # LCAstateLeft: False
    # LCAstateRight: False
    # LDWdistanceToLine: 1.25
    # LDWselection: False
    # LDWtimeToLine: 3.0
    # LDWwarningLeft: False
    # LDWwarningRight: False
    # LKAstate: False
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "ABSstate": msg.ABSstate,
            "ACCmainSwitch": msg.ACCmainSwitch,
            "ACCrequest": msg.ACCrequest,
            "ACCresumeButton": msg.ACCresumeButton,
            "ACCsetButton": msg.ACCsetButton,
            "ACCstate": msg.ACCstate,
            "ASRstate": msg.ASRstate,
            "EPBstate": msg.EPBstate,
            "ESCstate": msg.ESCstate,
            "FDstate": msg.FDstate,
            "FrontAssistIntervention": msg.FrontAssistIntervention,
            "LCAstateLeft": msg.LCAstateLeft,
            "LCAstateRight": msg.LCAstateRight,
            "LDWdistanceToLine": msg.LDWdistanceToLine,
            "LDWselection": msg.LDWselection,
            "LDWtimeToLine": msg.LDWtimeToLine,
            "LDWwarningLeft": msg.LDWwarningLeft,
            "LDWwarningRight": msg.LDWwarningRight,
            "LKAstate": msg.LKAstate,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x7(msg):
    # msg
    # Out[97]:
    # header:
    #   seq: 33767
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 653703274
    #   frame_id: ''
    # CRC: 10
    # Counter: 0
    # TrafficSign1: 10
    # TrafficSign2: 0
    # TrafficSign3: 0
    # AdditionalSign1: 0
    # AdditionalSign2: 0
    # AdditionalSign3: 0
    # SourceSign1: 0
    # SourceSign2: 0
    # SourceSign3: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "TrafficSign1": msg.TrafficSign1,
            "TrafficSign2": msg.TrafficSign2,
            "TrafficSign3": msg.TrafficSign3,
            "AdditionalSign1": msg.AdditionalSign1,
            "AdditionalSign2": msg.AdditionalSign2,
            "AdditionalSign3": msg.AdditionalSign3,
            "SourceSign1": msg.SourceSign1,
            "SourceSign2": msg.SourceSign2,
            "SourceSign3": msg.SourceSign3,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x8(msg):
    # msg
    # Out[101]:
    # header:
    #   seq: 33762
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 555392952
    #   frame_id: ''
    # CRC: 1
    # Counter: 11
    # TrafficSign4: 10
    # TrafficSign5: 0
    # AdditionalSign4: 0
    # AdditionalSign5: 0
    # SourceSign4: 0
    # SourceSign5: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "TrafficSign4": msg.TrafficSign4,
            "TrafficSign5": msg.TrafficSign5,
            "AdditionalSign4": msg.AdditionalSign4,
            "AdditionalSign5": msg.AdditionalSign5,
            "SourceSign4": msg.SourceSign4,
            "SourceSign5": msg.SourceSign5,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0x9(msg):
    # msg
    # Out[104]:
    # header:
    #   seq: 33762
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 555400394
    #   frame_id: ''
    # CRC: 220
    # Counter: 11
    # HeadingDirection: 223.5
    # LatDegree: 51.101531982421875
    # LatDirection: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "HeadingDirection": msg.HeadingDirection,
            "LatDegree": msg.LatDegree,
            "LatDirection": msg.LatDirection,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0xa(msg):
    # msg
    # Out[107]:
    # header:
    #   seq: 33760
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 514076688
    #   frame_id: ''
    # CRC: 162
    # Counter: 9
    # LongDegree: 13.925650596618652
    # LongDirection: 0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "LongDegree": msg.LongDegree,
            "LongDirection": msg.LongDirection,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0xb(msg):
    # msg
    # Out[110]:
    # header:
    #   seq: 33760
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 514082083
    #   frame_id: ''
    # CRC: 148
    # Counter: 9
    # UTC: 1592476949
    # Altitude: 254.0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "UTC": msg.UTC,
            "Altitude": msg.Altitude,
            }


@MSG_REGISTRY.register()
def parse_VehicleDataCanMsg0xc(msg):
    # msg
    # Out[114]:
    # header:
    #   seq: 33760
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 514087206
    #   frame_id: ''
    # CRC: 246
    # Counter: 9
    # FLDirection: 3
    # FRDirection: 3
    # RLDirection: 3
    # RRDirection: 3
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "FLDirection": msg.FLDirection,
            "FRDirection": msg.FRDirection,
            "RLDirection": msg.RLDirection,
            "RRDirection": msg.RRDirection,
            }


@MSG_REGISTRY.register()
def parse_CustomerCanMsg0x150(msg):
    # msg
    # Out[50]:
    # header:
    #   seq: 6756
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 750767334
    #   frame_id: ''
    # CRC: 52
    # Counter: 13
    # GatewayClearanceAI: False
    # GatewayClearanceEBI: False
    # GatewayClearanceSI: False
    # AngleDeviationLimitationSI: False
    # AngleGradientLimitationSI: False
    # AngleLimitationSI: False
    # AIState: 1
    # EBIState: 1
    # GIState: 1
    # SIState: 1
    # PDIState: 1
    # GWState: 2
    # LimitationsReceivedSI: 1
    # SoftwareVersionMajor: 0
    # SoftwareVersionMinor: 7
    # SoftwareVersionRevision: 6
    # VIState: 1
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "GatewayClearanceAI": msg.GatewayClearanceAI,
            "GatewayClearanceEBI": msg.GatewayClearanceEBI,
            "GatewayClearanceSI": msg.GatewayClearanceSI,
            "AngleDeviationLimitationSI": msg.AngleDeviationLimitationSI,
            "AngleGradientLimitationSI": msg.AngleGradientLimitationSI,
            "AngleLimitationSI": msg.AngleLimitationSI,
            "AIState": msg.AIState,
            "EBIState": msg.EBIState,
            "GIState": msg.GIState,
            "SIState": msg.SIState,
            "PDIState": msg.PDIState,
            "GWState": msg.GWState,
            "LimitationsReceivedSI": msg.LimitationsReceivedSI,
            "SoftwareVersionMajor": msg.SoftwareVersionMajor,
            "SoftwareVersionMinor": msg.SoftwareVersionMinor,
            "SoftwareVersionRevision": msg.SoftwareVersionRevision,
            "VIState": msg.VIState,
            }


@MSG_REGISTRY.register()
def parse_CustomerCanMsg0x160(msg):
    # msg
    # Out[54]:
    # header:
    #   seq: 33748
    #   stamp:
    #     secs: 1592477106
    #     nsecs: 520740082
    #   frame_id: ''
    # CRC: 4
    # Counter: 4
    # ActivationRequest: False
    # CancelRequest: False
    # ClearanceEBI: False
    # DecelerationRequest: 0.0
    return {"header": {"seq": msg.header.seq,
                       "stamp": {"secs": msg.header.stamp.secs,
                                 "nsecs": msg.header.stamp.nsecs},
                       "frame_id": msg.header.frame_id,},
            "CRC": msg.CRC,
            "Counter": msg.Counter,
            "ActivationRequest": msg.ActivationRequest,
            "CancelRequest": msg.CancelRequest,
            "ClearanceEBI": msg.ClearanceEBI,
            "DecelerationRequest": msg.DecelerationRequest,
            }
