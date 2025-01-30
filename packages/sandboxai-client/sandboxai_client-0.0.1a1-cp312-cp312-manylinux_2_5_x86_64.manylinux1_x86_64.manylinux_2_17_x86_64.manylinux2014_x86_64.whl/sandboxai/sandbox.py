from dataclasses import dataclass

from sandboxai.client.v1 import HttpClient
from sandboxai.api import v1 as v1Api
from sandboxai import embedded

from logging import getLogger

from threading import Lock

log = getLogger(__name__)

DEFAULT_IMAGE = "substratusai/sandboxai-box:v0.1.0"

# Prevent multiple Sandbox() instances from attempting to start the
# embedded server at the same time.
embedded_mutex = Lock()


@dataclass
class IPythonCellResult:
    output: str


@dataclass
class ShellCommandResult:
    output: str


class Sandbox:
    def __init__(
        self,
        base_url: str = "",
        embedded: bool = False,
        lazy_start: bool = False,
        image: str = DEFAULT_IMAGE,
        env: dict = None,
    ):
        """
        Initialize a Sandbox instance.
        """
        self.id = ""
        self.image = image
        self.env = env
        if embedded:
            self.__launch_embdedded_server()
        else:
            if not base_url:
                raise ValueError("base_url or embedded must be specified")
            self.base_url = base_url

        self.client = HttpClient(self.base_url)

        if lazy_start == False:
            self.start()

    def __enter__(self):
        """
        Enter the context manager. Ensures the sandbox is started.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager. Stops the sandbox.
        """
        self.stop()
        return False  # Don't suppress any exceptions

    def start(self) -> None:
        response = self.client.create_sandbox(
            v1Api.Sandbox(image=self.image, env=self.env)
        )
        self.id = response.id
        self.image = response.image

    def run_ipython_cell(self, input: str) -> IPythonCellResult:
        """
        Runs an ipython cell in the sandbox.
        """
        if not self.id:
            self.start()

        log.debug(f"Running ipython cell with input: {input}")
        response = self.client.run_ipython_cell(self.id, v1Api.RunIPythonCellRequest(code=input, split_output=False))  # type: ignore
        log.debug(f"IPython cell returned the output: {response.output}")
        result = IPythonCellResult(output=response.output or "")
        return result

    def run_shell_command(self, command: str) -> ShellCommandResult:
        """
        Runs a shell command in the sandbox.
        """
        if not self.id:
            self.start()

        log.debug(f"Running shell command with input: {command}")
        response = self.client.run_shell_command(self.id, v1Api.RunShellCommandRequest(command=command, split_output=False))  # type: ignore
        log.debug(f"Shell command returned the output: {response.output}")
        result = ShellCommandResult(output=response.output or "")
        return result

    def stop(self) -> None:
        if self.id:
            self.client.delete_sandbox(self.id)
            self.id = ""
            self.image = ""

    def __launch_embdedded_server(self):
        global embedded_mutex
        with embedded_mutex:
            if not embedded.is_running():
                log.info("Starting embedded server...")
                embedded.start_server()
                self.base_url = embedded.get_base_url()
            else:
                base_url = embedded.get_base_url()
                log.info(f"Embedded server is already running at {base_url}.")
                self.base_url = base_url
