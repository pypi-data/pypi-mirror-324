"""For access to a few functions from the terminal."""

import logging
logging.getLogger().setLevel(logging.INFO)

from sluf.workflow.slurm import (
    run_jobs,
    check_tasks,
    feed_jobs,
    is_q_empty,
)

# import sys
# if __name__ == "__main__": # and sys.stdin.isatty():
import argh
parser = argh.ArghParser()
parser.add_commands(
    [
        run_jobs,
        check_tasks,
        feed_jobs,
        is_q_empty,
    ]
)
if __name__ == "__main__": # and sys.stdin.isatty():
    parser.dispatch()
