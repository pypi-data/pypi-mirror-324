from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow import current
from .app_utils import start_app
from .supervisord_utils import SupervisorClient, SupervisorClientException
import os
import random
import string
import tempfile
import sys

DEFAULT_WAIT_TIME_SECONDS_FOR_PROCESS_TO_START = 10
BASE_DIR_FOR_APP_ASSETS = "/home/ob-workspace/.appdaemon/apps/"


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

        # We always need to have some environment defined through the flow to deploy and app.
        # Which means either step decorators like @pypi / @conda must be defined.
        # or flow level decorators like @conda_base / @pypi_base.
        if not any([deco.name == "pypi" or deco.name == "conda" for deco in decos]):
            flow_decorators = flow._flow_decorators.keys()
            if (
                "conda_base" not in flow_decorators
                and "pypi_base" not in flow_decorators
            ):
                raise MetaflowException(
                    "@app_deploy requires either step decorators like @pypi / @conda or flow level decorators like @conda_base / @pypi_base to be defined."
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

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_user_code_retries,
        ubf_context,
        inputs,
    ):
        os.makedirs(BASE_DIR_FOR_APP_ASSETS, exist_ok=True)
        # First we want to create a directory where the user's app directory and artifacts can be stored.
        with tempfile.TemporaryDirectory(
            prefix=BASE_DIR_FOR_APP_ASSETS, delete=False
        ) as temp_dir:
            launch_temp_dir = temp_dir

        # Expose this to the user, so that they can use it write their artifacts.
        setattr(flow, "deploy_dir", launch_temp_dir)

        # Make sure to record deploy_dir so that the user cannot accidentally override it.
        self._deploy_dir = launch_temp_dir

    def task_post_step(
        self, step_name, flow, graph, retry_count, max_user_code_retries
    ):
        deploy_dir = self._deploy_dir

        flow_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

        # By default, we assume that the layout of the flow directory is:
        # flow_dir/
        # - deployer_flow.py
        # - my_custom_app/
        #   - __main__.py
        #   - other_files
        #   - other_dirs/
        # This can be overridden by the user by setting the app_dir attribute.
        app_location = getattr(
            flow, "app_dir", os.path.join(flow_directory, self.attributes["app_name"])
        )

        if not os.path.exists(app_location):
            raise MetaflowException(f"App directory {app_location} does not exist.")

        wait_time_for_app_start = getattr(
            flow,
            "wait_time_for_app_start",
            DEFAULT_WAIT_TIME_SECONDS_FOR_PROCESS_TO_START,
        )

        # By default we assume that the user has a __main__.py file in their app directory.
        # They can always override this behavior.
        user_provided_entrypoint = getattr(flow, "entrypoint", None)

        if user_provided_entrypoint is not None and not isinstance(
            user_provided_entrypoint, str
        ):
            raise MetaflowException(
                f"@app_deploy requires entrypoint to be set to a string. The current value of entrypoint {user_provided_entrypoint} is not valid."
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
                self.attributes["app_port"],
                user_provided_entrypoint,
                deploy_dir,
                app_location,
            )
        except SupervisorClientException as e:
            raise MetaflowException(str(e))
        except Exception as e:
            raise MetaflowException(
                f"Failed to start {self.attributes['app_name']}! Cause: {str(e)}"
            ) from e
