import traceback
from argparse import ArgumentParser

from moonleap.entrypoint import gen, parse_args
from moonleap.entrypoint.check_args import check_args
from moonleap.session.create_session import create_session


class NeverException(Exception):
    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    args = parse_args(parser)
    check_args(parser, args)

    session = create_session(args)

    if args.action == "gen":
        try:
            gen(args, session)
        except NeverException as e:
            session.report("Error: " + str(e))
            if args.stacktrace:
                traceback.print_exc()
        finally:
            pass
