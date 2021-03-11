import rosbag
from pathlib import Path
import numpy as np
import cv2
from urllib.parse import quote_plus
import pymongo

from importROS import msg_parser


class RosbagReader:
    def __init__(self, src_path: Path):
        bag = rosbag.Bag(src_path)
        self.path = src_path
        self.n_messages = bag.get_message_count()
        self.summary = bag.get_type_and_topic_info().topics  # type: Dict
        self.topic_to_msg_type = {}
        for k, v in self.summary.items():
            msg_type = v.msg_type.split("/")[-1]
            self.topic_to_msg_type[k] = msg_type

        self.messages = bag.read_messages()  # generator for all topics
        # messages = bag.read_messages(topics=['/camera/lane_detector', '/velodyne_points', '/adma/imu'])
        self.supported_parsers = msg_parser.MSG_REGISTRY
        self.debug = False

    def next(self):
        for topic, msg, t in self.messages:
            msg_t = self.topic_to_msg_type[topic]
            stamp = str(t.to_nsec())
            parser_name = "parse_" + msg_t
            if parser_name in self.supported_parsers:
                msg_dict = msg_parser.MSG_REGISTRY.get(parser_name)(msg)
                t = msg_dict["header"]["stamp"]["secs"]
                if self.debug:
                    print(f"{topic} -> {msg_t} -> {stamp} -> {t}")
                yield topic, msg_dict, msg_t, stamp


class SaveToLocal:
    def __init__(self,
                 topic_name: str,
                 root_path: Path,
                 date_folder: Path,
                 sensor_folder: Path,
                 ext: str = ".png"):
        self.topic_name = topic_name
        self.root_path = root_path
        self.date_folder = date_folder
        self.sensor_folder = sensor_folder
        self.ext = ext
        self.save_path = self.root_path / self.date_folder / self.sensor_folder
        self.save_path.mkdir(parents=True, exist_ok=True)

    def __call__(self, topic, msg_dict, msg_t, stamp):
        if topic == self.topic_name:
            file_name = Path(f"{stamp}{self.ext}")
            save_path = self.save_path / file_name
            if self.ext == ".npy":
                np.save(save_path, msg_dict["data"])
                # save relative path to database
                msg_dict["data"] = f"{self.date_folder.name}/{self.sensor_folder.name}/{file_name.name}"
            elif self.ext == ".png":
                cv2.imwrite(str(save_path), msg_dict["data"][:, :, ::-1])
                msg_dict["data"] = f"{self.date_folder.name}/{self.sensor_folder.name}/{file_name.name}"


class UploadToMongoDB:
    def __init__(self, save_to_local = (), erase_old=True):
        user = quote_plus("db_dev")
        password = quote_plus("123456")
        host = "192.168.2.94"
        db_name = "LyftLevel5"
        uri = "mongodb://%s:%s@%s/%s" % (user, password, host, db_name)
        self.client = pymongo.MongoClient(uri)
        self.db = self.client.Passat

        # collections
        self.collection_map = self.db.map
        self.collection_log = self.db.log
        self.collection_scene = self.db.scene
        self.collection_sample = self.db.sample
        self.collection_sample_annotation = self.db.sample_annotation
        self.collection_sample_data = self.db.sample_data
        self.collection_perception_data = self.db.perception_data
        self.collection_canbus_data = self.db.canbus_data
        self.collection_vehicle_data = self.db.vehicle_data
        self.collection_sensor = self.db.sensor

        self.prev_id_buffer = {}
        self.save_data_to_local = save_to_local

        if erase_old:
            self.collection_map.delete_many({})
            self.collection_log.delete_many({})
            self.collection_scene.delete_many({})
            self.collection_sample.delete_many({})
            self.collection_sample_annotation.delete_many({})
            self.collection_sample_data.delete_many({})
            self.collection_perception_data.delete_many({})
            self.collection_canbus_data.delete_many({})
            self.collection_vehicle_data.delete_many({})
            self.collection_sensor.delete_many({})

    def __del__(self):
        self.client.close()

    def get_collection(self, topic):
        if topic.split("/")[1] in ["CAN"]:
            return self.collection_canbus_data
        elif topic.split("/")[1] in ["camera", "velodyne_points"]:
            return self.collection_perception_data
        else:
            return self.collection_vehicle_data

    def __call__(self, topic_name, msg, msg_type, stamp):
        collection = self.get_collection(topic_name)

        # save image and points cloud to local, use file path to replace ["data"]
        for each_fn in self.save_data_to_local:
            each_fn(topic_name, msg, msg_type, stamp)

        msg["topic_name"] = topic_name
        msg["msg_type"] = msg_type
        msg["t_stamp"] = stamp
        msg["next_id"] = None
        if topic_name in self.prev_id_buffer:
            msg["prev_id"] = self.prev_id_buffer[topic_name]
        else:
            msg["prev_id"] = None
        curr_id = collection.insert_one(msg).inserted_id  # insert a new record

        # assign curr_id to prev_doc with "next_id" to build bilateral index
        if msg["prev_id"] is not None:
            collection.find_one_and_update(
                {"_id": msg["prev_id"]},
                {"$set": {"next_id": curr_id}},
                upsert=False,  # if not found, then do not create new document
            )

        self.prev_id_buffer[topic_name] = curr_id


class ImportRosbag:
    def __init__(self, rosbag_path: Path, save_root: Path):
        self.rosbag_path = rosbag_path
        self.save_root = save_root

    def passat(self, limit=-1):
        reader = RosbagReader(self.rosbag_path)

        save_lanecamera = SaveToLocal(topic_name="/camera/lane_detector",
                                      root_path=self.save_root,
                                      date_folder=Path("2020-06-18-12-45-06"),
                                      sensor_folder=Path("lane_camera"),
                                      ext=".png")
        save_velodyne = SaveToLocal(topic_name="/velodyne_points",
                                    root_path=self.save_root,
                                    date_folder=Path("2020-06-18-12-45-06"),
                                    sensor_folder=Path("velodyne"),
                                    ext=".npy")
        save_scala1 = SaveToLocal(topic_name="/scala1/pointcloud",
                                  root_path=self.save_root,
                                  date_folder=Path("2020-06-18-12-45-06"),
                                  sensor_folder=Path("scala1"),
                                  ext=".npy")
        save_scala2 = SaveToLocal(topic_name="/scala2/pointcloud",
                                  root_path=self.save_root,
                                  date_folder=Path("2020-06-18-12-45-06"),
                                  sensor_folder=Path("scala2"),
                                  ext=".npy")
        save_scala3 = SaveToLocal(topic_name="/scala3/pointcloud",
                                  root_path=self.save_root,
                                  date_folder=Path("2020-06-18-12-45-06"),
                                  sensor_folder=Path("scala3"),
                                  ext=".npy")
        save_scala4 = SaveToLocal(topic_name="/scala4/pointcloud",
                                  root_path=self.save_root,
                                  date_folder=Path("2020-06-18-12-45-06"),
                                  sensor_folder=Path("scala4"),
                                  ext=".npy")
        save_to_local = (save_lanecamera, save_velodyne, save_scala1, save_scala2, save_scala3, save_scala4)

        upload_to_mongodb = UploadToMongoDB(save_to_local)
        n = 0
        for each in reader.next():
            upload_to_mongodb(*each)
            n += 1
            if n > limit > 0:
                break
