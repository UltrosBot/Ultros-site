import argparse
import os
import subprocess


def run_migrations(args):
    print("Running migrations with Alembic")
    print("===============================\n")

    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    sp = subprocess.Popen(["alembic", "upgrade", "head"], env=env)
    sp.wait()


def create_migrations(args):
    print("Creating revision with Alembic")
    print("==============================\n")

    message = args.message

    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    sp = subprocess.Popen(["alembic", "revision", "--autogenerate", "-m", message], env=env)
    sp.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="tools.py"
    )

    subparsers = parser.add_subparsers()

    parser_run_migrations = subparsers.add_parser(
        "run-migrations", help="Run latest migrations"
    )
    parser_run_migrations.set_defaults(func=run_migrations)

    parser_create_migrations = subparsers.add_parser(
        "create-migrations", help="Create a migrations revision"
    )
    parser_create_migrations.add_argument(
        "message", help="Provide a summary message for the migration"
    )
    parser_create_migrations.set_defaults(func=create_migrations)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()