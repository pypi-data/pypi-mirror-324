import os
import subprocess

try:
    import uv

    print("uv found")
except ImportError:
    print("uv not found")


def find_uv():
    # this path seems to work on vercel
    cmd = os.path.abspath(os.path.join(__file__, "../../bin/uv"))
    if os.path.exists(cmd):
        return cmd
    else:
        # this should be the uv way
        return uv.find_uv_bin()


uvcmd = os.fsdecode(find_uv())


# see:
#  https://github.com/astral-sh/uv/pull/6663
#  https://github.com/astral-sh/uv/issues/6641
# uv 0.3.5 added support for custom environments
# marker values for uv pip compile
# Note that this file/configuration is only respected
# when the --universal flag is passed to uv pip compile
uv_toml = """
environments = [
    "platform_system == 'Emscripten'"
]
"""

with open("/tmp/pycafe-server-uv.toml", "w") as f:
    f.write(uv_toml)

os.environ["UV_CONFIG_FILE"] = "/tmp/pycafe-server-uv.toml"


def _run_resolve(
    requirements, constraints, overrides, python_version: str, universal: bool = False
):
    import tempfile

    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # write the requirements file
        input = os.path.join(temp_dir, "requirements.txt")
        output = os.path.join(temp_dir, "requirements-resolved.txt")
        constraints_path = os.path.join(temp_dir, "constraints.txt")
        overrides_path = os.path.join(temp_dir, "overrides.txt")
        with open(input, "w") as f:
            f.write(requirements)
        with open(constraints_path, "w") as f:
            f.write(constraints)
        with open(overrides_path, "w") as f:
            f.write(overrides)

        # uv cannot install all minor versions of Python, just use the major.minor version
        python_version = ".".join(python_version.split(".")[:2])
        # run uv python install manually, see
        #  https://github.com/py-cafe/app/pull/252
        #  https://github.com/astral-sh/uv/issues/8039

        # don't expose potentially sensitive environment variables to build scripts run by uv
        sanitized_env = {
            k: v
            for k, v in os.environ.items()
            if k.startswith("UV_") or k in ["PATH", "LANG", "PWD"]
        }

        subprocess.run(
            [
                uvcmd,
                "python",
                "install",
                python_version,
            ],
            check=True,
            capture_output=True,
            env=sanitized_env,
        )
        # run uv pip compile
        subprocess.run(
            [
                uvcmd,
                "pip",
                "compile",
                input,
                "-o",
                output,
                "-q",
                "--no-header",
                "-c",
                constraints_path,
                "--override",
                overrides_path,
                "--python-version",
                python_version,
            ]
            + (["--universal"] if universal else []),
            check=True,
            capture_output=True,
            env=sanitized_env,
        )
        # read the output file
        with open(output, "r") as f:
            output = f.read()
            print("resolved", output)
        return output
