import argparse
import os
import subprocess
import sys
from config.constants import (
    DOCKER_REPO,
    MODULE_REPO,
    TARGET_COMMIT,
)


def run_module():
    WEB3_PRIVATE_KEY = os.environ.get("WEB3_PRIVATE_KEY")

    if not WEB3_PRIVATE_KEY:
        print(
            "❌ Error: No `WEB3_PRIVATE_KEY` configured ",
            file=sys.stderr,
            flush=True,
        )
        print("\t👉 /.env")

    # Remove the following print and sys.exit statements and create the module job.
    print(
        "❌ Error: No job configured. Implement the module's job before running the module.",
        file=sys.stderr,
        flush=True,
    )
    print("1. Implement job for module")
    print("\t👉 /src/run_inference.py")
    print("2. Delete this code block")
    print("\t👉 /scripts/run_module.py")
    sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Run the Lilypad module with specified input."
    )

    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        default=None,
        help="The input to be processed by the Lilypad module.",
    )

    parser.add_argument(
        "--local",
        action="store_true",
        help="Run the Lilypad module Docker image locally.",
    )

    args = parser.parse_args()

    if args.input is None:
        args.input = input("Enter your input: ").strip()

    local = args.local

    output_dir = os.path.abspath("./outputs")

    command = (
        [
            "docker",
            "run",
            "-e",
            f"INPUT={args.input}",
            "-v",
            f"{output_dir}:/outputs",
            f"{DOCKER_REPO}:latest",
        ]
        if local
        else [
            "lilypad",
            "run",
            # "--network",
            # "demonet",
            f"{MODULE_REPO}:{TARGET_COMMIT}",
            "--web3-private-key",
            WEB3_PRIVATE_KEY,
            "-i",
            f'input="{args.input}"',
        ]
    )

    try:
        print("Executing Lilypad module...")
        result = subprocess.run(command, check=True, text=True)
        print("✅ Lilypad module executed successfully.")
        print(f"👉 {output_dir}/result.json")
        return result
    except subprocess.CalledProcessError as error:
        print(
            f"❌ Error: Module execution failed. {error}",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)


if __name__ == "__main__":
    run_module()
