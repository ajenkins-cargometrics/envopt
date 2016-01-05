""" Fork of docopt. """

import os
import re
import docopt


__all__ = ['envopt']


_env_var_prefix = ''


def _get_env_name_for_option(option_name):
    """
    Get the environment variable name corresponding to an option name, used for providing a default value.

    :param option_name: The long or short option name
    :return: The name of the corresponding environment variable name
    """
    normalized = option_name.lstrip('-').upper().replace('-', '_')
    return _env_var_prefix + normalized


class EnvOption(docopt.Option):
    @classmethod
    def parse(class_, option_description):
        """ Parse the options using virtually the same code as docopt.
            If an ENV variable exists with the same name as an option (suitably modified),
            use that value over the traditional default. """
        short, long, argcount, value, env = None, None, 0, False, None
        options, _, description = option_description.strip().partition('  ')
        options = options.replace(',', ' ').replace('=', ' ')
        for s in options.split():
            if s.startswith('--'):
                long = s
            elif s.startswith('-'):
                short = s
            else:
                argcount = 1

        env = _get_env_name_for_option(long or short)
        env_value = os.getenv(env)

        if argcount:
            matched = re.findall('\[default: (.*)\]', description, flags=re.I)
            value = matched[0] if matched else None
            # Replace value if the default exists as an ENV variable
            if env_value is not None:
                value = env_value
        else:
            # for switch arguments interpret env_value as a boolean
            if env_value is not None:
                # Anything other than 1, true, or yes is interpreted as False.  Maybe should be more strict?
                value = env_value.lower() in ['1', 'true', 'yes']

        return class_(short, long, argcount, value)


def envopt(doc, argv=None, help=True, version=None, options_first=False, env_prefix=''):
    global _env_var_prefix
    _env_var_prefix = env_prefix
    return docopt.docopt(doc, argv, help, version, options_first)


docopt.Option = EnvOption
envopt.__doc__ = docopt.docopt.__doc__.replace('docopt', 'envopt')
