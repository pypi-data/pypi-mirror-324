import os
from evalsync.proto.sync_pb2 import StateSync, ServiceState, ExperimentCommand, ManagerMessage
import zmq

class ExperimentManager:
    def __init__(self, experiment_id: str, num_workers: int):
        self.context = zmq.Context()
        self.experiment_id = experiment_id
        self.ready_workers = 0
        self.num_workers = num_workers
        
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f"ipc://{experiment_id}-worker")
        self.sub_socket.subscribe("")

        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"ipc://{experiment_id}-manager")

    def cleanup(self):
        self.sub_socket.close()
        self.pub_socket.close()
        self.context.term()
        if os.path.exists(f"{self.experiment_id}-manager"):
            os.remove(f"{self.experiment_id}-manager")
        if os.path.exists(f"{self.experiment_id}-worker"):
            os.remove(f"{self.experiment_id}-worker")

    def wait_all_workers(self):
        while self.ready_workers < self.num_workers:
            message = StateSync()
            StateSync.ParseFromString(message, self.sub_socket.recv())
            if message.state == ServiceState.READY:
                self.ready_workers += 1

    def start(self):
        self.pub_socket.send(ManagerMessage(command=ExperimentCommand.BEGIN).SerializeToString())

    def stop(self):
        self.pub_socket.send(ManagerMessage(command=ExperimentCommand.END).SerializeToString())

