from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow import current
from .app_utils import start_app
from .supervisord_utils import SupervisorClient, SupervisorClientException
import os

DEFAULT_WAIT_TIME_SECONDS_FOR_PROCESS_TO_START = 10


class WorkstationAppDeployDecorator(StepDecorator):
    """
    Specifies that this step is used to deploy an instance of the app.
    Requires that self.app_name, self.app_port, self.entrypoint and self.deployDir is set.

    Parameters
    ----------
    app_port : int
        Number of GPUs to use.
    app_name : str
        Name of the app to deploy.
    """

    name = "app_deploy"
    defaults = {"app_port": 8080, "app_name": "app"}

    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        if any([deco.name == "kubernetes" for deco in decos]):
            raise MetaflowException(
                "Step *{step}* is marked for execution both on Kubernetes and "
                "Nvidia. Please use one or the other.".format(step=step)
            )

        app_port = self.attributes["app_port"]
        app_name = self.attributes["app_name"]

        # Currently this decorator is expected to only execute on workstation.
        if app_port is None or app_port < 6000 or app_port > 6002:
            raise MetaflowException(
                "AppDeployDecorator requires app_port to be between 6000 and 6002."
            )

        if app_name is None:
            raise MetaflowException("AppDeployDecorator requires app_name to be set.")

    def task_post_step(
        self, step_name, flow, graph, retry_count, max_user_code_retries
    ):
        entrypoint = getattr(flow, "entrypoint", None)
        wait_time_for_app_start = getattr(
            flow,
            "wait_time_for_app_start",
            DEFAULT_WAIT_TIME_SECONDS_FOR_PROCESS_TO_START,
        )

        if entrypoint is None or not isinstance(entrypoint, str):
            raise MetaflowException(
                f"@app_deploy requires entrypoint to be set to a string. The current value of entrypoint {entrypoint} is not valid."
            )

        launch_dir = getattr(flow, "launch_dir", None)
        if launch_dir is None or launch_dir == "":
            raise MetaflowException("@app_deploy requires launch_dir to be set.")
        elif not isinstance(launch_dir, str) or not os.path.exists(launch_dir):
            raise MetaflowException(
                f"@app_deploy requires launch_dir to be set to a valid directory. The current value of launch_dir {launch_dir} is not valid."
            )

        try:
            supervisor_client = SupervisorClient(
                wait_time_seconds_for_app_start=wait_time_for_app_start
            )

            # First, let's deploy the app.
            start_app(
                port=self.attributes["app_port"], name=self.attributes["app_name"]
            )

            # Now, let's add the app to supervisor.
            supervisor_client.start_process_with_supervisord(
                self.attributes["app_name"],
                entrypoint,
                launch_dir,
            )
        except SupervisorClientException as e:
            raise MetaflowException(str(e))
        except Exception as e:
            raise MetaflowException(
                f"Failed to start {self.attributes['app_name']}! Cause: {str(e)}"
            ) from e
