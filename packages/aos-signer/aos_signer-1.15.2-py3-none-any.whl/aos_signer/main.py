#
#  Copyright (c) 2018-2024 Renesas Inc.
#  Copyright (c) 2018-2024 EPAM Systems Inc.
#
# pylint: disable=W0611
import argparse
import sys
from pathlib import Path

from aos_signer.signer.commands import (
    bootstrap_service_folder,
    sign_service,
    upload_service,
    validate_service_config,
)
from aos_signer.signer.common import print_error
from aos_signer.signer.errors import SignerError

try:
    from importlib.metadata import PackageNotFoundError, version  # noqa: WPS433
except ImportError:
    from importlib_metadata import (  # noqa: WPS433, WPS440, F401
        PackageNotFoundError,
        version,
    )

_COMMAND_INIT = 'init'
_COMMAND_SIGN = 'sign'
_COMMAND_UPLOAD = 'upload'
_COMMAND_VALIDATE = 'validate'
_COMMAND_GO = 'go'
DEFAULT_CONFIG_PATH = 'meta/config.yaml'


def _parse_args():
    """User arguments parser.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog='aos-signer',
        description='This tool will help you to prepare, sign and upload service to Aos Cloud',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    sub_parser = parser.add_subparsers(title='Commands')

    init = sub_parser.add_parser(
        _COMMAND_INIT,
        help="Generate required folders and configuration file. If you don't know where to start type aos-signer init",
    )
    init.set_defaults(func=run_init_signer)

    validate = sub_parser.add_parser(
        _COMMAND_VALIDATE,
        help='Validate config file.',
    )
    validate.set_defaults(func=run_validate)

    sign = sub_parser.add_parser(
        _COMMAND_SIGN,
        help='Sign Service. Read config and create signed archive ready to be uploaded.',
    )
    sign.set_defaults(func=run_sign)

    upload = sub_parser.add_parser(
        _COMMAND_UPLOAD,
        help='Upload Service to the Cloud.'
             'Address, security credentials and service UID is taken from config.yaml in meta folder.',  # noqa: WPS318
    )
    upload.set_defaults(func=run_upload_service)

    go = sub_parser.add_parser(
        _COMMAND_GO,
        help='Sign and upload Service to the Cloud.'
             'Address, security credentials and service UID are taken from config.yaml in meta folder.',  # noqa: WPS318
    )
    go.set_defaults(func=run_go)

    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'%(prog)s {version("aos-signer")}',  # noqa: WPS323,WPS237
    )

    return parser


def run_init_signer(args):
    bootstrap_service_folder()


def run_validate(args):
    validate_service_config(Path(DEFAULT_CONFIG_PATH))


def run_upload_service(args):
    upload_service(Path(DEFAULT_CONFIG_PATH))


def run_sign(args):
    sign_service(Path(DEFAULT_CONFIG_PATH), 'src', '.')


def run_go(args):
    config_path = Path(DEFAULT_CONFIG_PATH)
    sign_service(config_path, 'src', '.')
    upload_service(config_path)


def main():
    parser = _parse_args()
    args = parser.parse_args()
    try:
        if not hasattr(args, 'func'):  # noqa: WPS421
            args.func = run_sign
        args.func(args)
    except SignerError as se:
        print_error('Process failed with error: ')
        se.print_message()
        sys.exit(1)
    except Exception as sce:
        print_error('[red]Process failed with error: [/red]')
        print_error(str(sce))
        sys.exit(1)


if __name__ == '__main__':
    main()
