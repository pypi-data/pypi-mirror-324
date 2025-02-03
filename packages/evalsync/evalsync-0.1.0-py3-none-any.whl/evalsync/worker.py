from evalsync.proto.sync_pb2 import StateSync, ServiceState, ManagerMessage, ExperimentCommand
import zmq

class ExperimentWorker:
    def __init__(self, experiment_id: str):
        self.context = zmq.Context()
        self.experiment_id = experiment_id
        self.state = ServiceState.INIT

        # we pub on the worker channel and sub on the manager channel
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f"ipc://{experiment_id}-manager")
        self.sub_socket.subscribe("")

        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"ipc://{experiment_id}-worker")

        self.metadata = {}

    def cleanup(self):
        self.sub_socket.close()
        self.pub_socket.close()
        self.context.term()

    def notify_manager(self) -> bool:
        message = StateSync(state=self.state, error_message="ready", metadata=self.metadata).SerializeToString()
        print(f"send {message}")
        self.pub_socket.send(message)
        return True

    def ready(self) -> bool:
        if self.state == ServiceState.INIT:
            self.state = ServiceState.READY
            self.notify_manager()
            return True
        else:
            return False

    def wait_for_start(self) -> bool:
        if self.state == ServiceState.READY:
            while self.state != ServiceState.RUNNING:
                message = ManagerMessage()
                ManagerMessage.ParseFromString(message, self.sub_socket.recv())
                match message.command:
                    case ExperimentCommand.BEGIN:
                        self.state = ServiceState.RUNNING
                        self.notify_manager()
                        return True
                    case ExperimentCommand.END | ExperimentCommand.ABORT:
                        self.state = ServiceState.ERROR
                        self.notify_manager()
                        return False

        return False

    def end(self):
        if self.state == ServiceState.RUNNING:
            self.state = ServiceState.DONE
            self.notify_manager()
            return True
        else:
            return False

    def wait_for_end(self):
        if self.state == ServiceState.RUNNING:
            while self.state != ServiceState.DONE:
                message = ManagerMessage()
                ManagerMessage.ParseFromString(message, self.sub_socket.recv())
                match message.command:
                    case ExperimentCommand.END:
                        self.state = ServiceState.DONE
                        self.notify_manager()
                        return True
                    case ExperimentCommand.BEGIN | ExperimentCommand.ABORT:
                        self.state = ServiceState.ERROR
                        self.notify_manager()
                        return True
        return False