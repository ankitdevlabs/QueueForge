import fire

from queueforge.bootstrap.console import QueueForgeCliCommand


class Command:
    @property
    def queueforge(self):
        return QueueForgeCliCommand()


def main():
    fire.Fire(Command)


if __name__ == "__main__":
    main()
