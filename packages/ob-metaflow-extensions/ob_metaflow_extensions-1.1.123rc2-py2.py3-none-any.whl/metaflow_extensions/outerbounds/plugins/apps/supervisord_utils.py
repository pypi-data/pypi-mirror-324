import argparse
import os
import configparser
import tempfile
import sys
import subprocess
from pathlib import Path
import shutil
from enum import Enum
import time


class SupervisorClientException(Exception):
    pass


class SupervisorClient:
    class SupervisodProcessCodes(Enum):
        STOPPED = 0
        STARTING = 10
        RUNNING = 20
        BACKOFF = 30
        STOPPING = 40
        EXITED = 100
        FATAL = 200
        UNKNOWN = 1000

    def __init__(self, wait_time_seconds_for_app_start: int):
        self.supervisor_conf_loc = os.environ.get("SUPERVISOR_CONF_PATH")

        self.wait_time_seconds_for_app_start = wait_time_seconds_for_app_start
        if self.supervisor_conf_loc is None or not os.path.exists(
            self.supervisor_conf_loc
        ):
            raise SupervisorClientException(
                "This workstation does not support deploying apps! Please reach out to Outerbounds for support."
            )

        self.metaflow_envs_persistent_path = os.environ.get(
            "SUPERVISOR_PYTHON_ENVS_PATH"
        )
        if self.metaflow_envs_persistent_path is None:
            raise SupervisorClientException(
                "This workstation does not support deploying apps! Please reach out to Outerbounds for support."
            )

        # Check if supervisorctl is installed
        if not shutil.which("supervisorctl"):
            raise SupervisorClientException(
                "This workstation does not support deploying apps! Please reach out to Outerbounds for support."
            )

    def _stop_existing_app_at_port(self, app_port):
        supervisor_config = configparser.ConfigParser()
        supervisor_config.read(self.supervisor_conf_loc)

        for program in supervisor_config.sections():
            if "obp_app_port" in supervisor_config[program]:
                if supervisor_config[program]["obp_app_port"].strip() == str(app_port):
                    res = subprocess.run(
                        ["supervisorctl", "stop", program],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )

                    del supervisor_config[program]

        with tempfile.NamedTemporaryFile(
            "w", dir=os.path.dirname(self.supervisor_conf_loc), delete=False
        ) as f:
            supervisor_config.write(f)
            tmp_file = f.name

        os.rename(tmp_file, self.supervisor_conf_loc)

    def start_process_with_supervisord(
        self,
        app_name,
        app_port,
        user_provided_entrypoint,
        deploy_dir=None,
        app_dir=None,
    ):
        """
        Add a new program entry to supervisor configuration.

        Args:
            app_name: The name of the app to start.
            entrypoint: The entrypoint to start the app with.
            directory: The directory to run the app in.
            deploy_dir: The directory to copy the app to and deploy from.
            app_dir: The directory to copy the app from.
        """

        entrypoint = user_provided_entrypoint
        deploy_dir_for_port = "/home/ob-workspace/.appdaemon/apps/6000"
        launch_directory = (
            "/home/ob-workspace/.appdaemon/apps"
            if entrypoint is None
            else "/home/ob-workspace/.appdaemon"
        )

        # Step 1: Stop any existing apps that are running on the same port.
        self._stop_existing_app_at_port(app_port)

        if user_provided_entrypoint is None:
            # Step 2: Copy the app_dir to the deploy_dir.
            recursive_copy(app_dir, deploy_dir)

            # Step 3: Copy the entire deploy_dir to the port specific directory.
            if os.path.exists(deploy_dir_for_port):
                shutil.rmtree(deploy_dir_for_port)

            os.makedirs(deploy_dir_for_port)
            recursive_copy(deploy_dir, deploy_dir_for_port)

            # Apply default value
            entrypoint = f"-m {str(app_port)}"

        shutil.rmtree(deploy_dir)

        persistent_path_for_executable = (
            self.persist_metaflow_generated_python_environment()
        )

        command = f"{persistent_path_for_executable} {entrypoint}"

        entry = {
            "command": command,
            "directory": launch_directory,
            "autostart": "true",
            "autorestart": "true",
            "obp_app_port": app_port,  # Record the app port for internal reference. This is not used by supervisor.
        }

        supervisor_config = configparser.ConfigParser()
        supervisor_config.read(self.supervisor_conf_loc)

        supervisor_config[f"program:{app_name}"] = entry

        with tempfile.NamedTemporaryFile(
            "w", dir=os.path.dirname(self.supervisor_conf_loc), delete=False
        ) as f:
            supervisor_config.write(f)
            tmp_file = f.name

        os.rename(tmp_file, self.supervisor_conf_loc)

        # Execute supervisorctl reload
        # Capture the exit code
        exit_code = subprocess.run(
            ["supervisorctl", "reload"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        if exit_code != 0:
            print("Failed to reload supervisor configuration!", file=sys.stderr)
            return

        print(
            f"Waiting for {self.wait_time_seconds_for_app_start} seconds for {app_name} to start..."
        )
        time.sleep(self.wait_time_seconds_for_app_start)
        status = self._get_launched_prcoess_status(app_name)

        if status not in [
            self.SupervisodProcessCodes.RUNNING,
            self.SupervisodProcessCodes.STARTING,
        ]:
            raise SupervisorClientException(
                f"Failed to start {app_name}! Try running {command} manually to debug."
            )

    def _get_launched_prcoess_status(self, app_name):
        status_cmd_output = subprocess.run(
            ["supervisorctl", "status", app_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8")

        status_cmd_output_parts = [
            x.strip() for x in status_cmd_output.split(" ") if x.strip()
        ]

        status_str = status_cmd_output_parts[1]

        if status_str == "RUNNING":
            return self.SupervisodProcessCodes.RUNNING
        elif status_str == "STOPPED":
            return self.SupervisodProcessCodes.STOPPED
        elif status_str == "STARTING":
            return self.SupervisodProcessCodes.STARTING
        elif status_str == "BACKOFF":
            return self.SupervisodProcessCodes.BACKOFF
        elif status_str == "STOPPING":
            return self.SupervisodProcessCodes.STOPPING
        elif status_str == "EXITED":
            return self.SupervisodProcessCodes.EXITED
        elif status_str == "FATAL":
            return self.SupervisodProcessCodes.FATAL
        else:
            return self.SupervisodProcessCodes.UNKNOWN

    # By default, an environment generated by metaflow will end up in a path like: /root/micromamba/envs/metaflow/linux-64/02699a4d2d50cfc/bin/python
    # However, on a workstation these environments are not persisted, so we need to copy them over to /home/ob-workspace
    def persist_metaflow_generated_python_environment(self):
        current_executable = sys.executable
        environment_path = Path(current_executable).parent.parent

        persistent_path_for_this_environment = os.path.join(
            self.metaflow_envs_persistent_path,
            environment_path.parent.name,
            environment_path.name,
        )

        final_executable_path = os.path.join(
            persistent_path_for_this_environment,
            Path(current_executable).parent.name,
            Path(current_executable).name,
        )

        if os.path.exists(final_executable_path):
            return final_executable_path

        os.makedirs(persistent_path_for_this_environment, exist_ok=True)

        recursive_copy(environment_path, persistent_path_for_this_environment)

        return final_executable_path


def recursive_copy(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
