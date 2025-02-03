import threading
import time
import uuid
import pytest
from evalsync import ExperimentWorker, ExperimentManager

@pytest.mark.timeout(15)
def test_normal_flow():
    experiment_id = f"/tmp/{uuid.uuid4()}"

    manager = ExperimentManager(experiment_id, 1)
    worker = ExperimentWorker(experiment_id)

    time.sleep(1)

    worker.ready()
    print(f"worker is ready")

    manager.wait_all_workers()
    manager.start()
    worker.wait_for_start()
    manager.stop()
    worker.wait_for_end()

    worker.cleanup()
    manager.cleanup()