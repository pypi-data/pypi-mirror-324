import subprocess
from .settings import get_option
from .log import exception

def execute(command: str, capture: bool = False, allow_single_quotes: bool = False) -> str | None:
    """
    Execute the given code.

    :param code: The code to execute.
    :param capture: Whether to capture the output or simply print it.
    :return: The output of the code if capture is True.
    """
    if not capture:
        try:
            subprocess.run(command, shell=True).check_returncode()
        except subprocess.CalledProcessError as e:
            exception(f"Error executing command `{command}`", e)
            raise e
        return

    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        proc.wait()
        stdout, stderr = proc.communicate()
        error_output = stderr.decode()
        return_code = proc.returncode
        if return_code != 0:
            exception("Error executing command", RuntimeError(error_output))
            raise RuntimeError(f"Error executing command `{command}`: {error_output}")
        return stdout.decode()

def nix_exec(command: str, capture: bool = False, packages: list[str] | None = None) -> str:
    if '"' in command:
        raise ValueError("Double quotes are not allowed in nix_exec")
    packages = packages or []
    packages += ["bash"]
    packages_str = " ".join(packages)
    return execute(f"nix-shell --packages {packages_str} --quiet --run \"{command}\"", capture=capture) or ''
