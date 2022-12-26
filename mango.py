#!/usr/bin/python3

from program.command import MangoCommand
from server.pull import pull
from server.push import push
from client.tests import run_test, local_test
from client.init import init_tests, add_test
import sys

commands = {
    MangoCommand("pull", ["category"], pull),
    MangoCommand("init", [], init_tests),
    MangoCommand("add", ["category", "name"], add_test),
    MangoCommand("test", ["category"], run_test),
    MangoCommand("local", ["category"], local_test),
    MangoCommand("push", [], push),
}

if len(sys.argv) < 2:
    print('Usage: mango <command> [args]')
    print('Available commands:')
    for command in commands:
        print(f'  - {command.name} {" ".join([f"<{arg}>" for arg in command.args])}')
    exit(1)

for command in commands:
    if command.name == sys.argv[1]:
        if len(sys.argv) - 2 == len(command.args):
            command.action(*sys.argv[2:])
        else:
            print(f'Usage: mango {command.name} {" ".join([f"<{arg}>" for arg in command.args])}')
        break
