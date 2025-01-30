# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ak']

package_data = \
{'': ['*']}

install_requires = \
['colored>=2.2.4,<3.0.0', 'terminaltables>=3.1.10,<4.0.0']

setup_kwargs = {
    'name': 'akconfig',
    'version': '0.1.8',
    'description': 'A configuration management for global variables in python projects.',
    'long_description': '# akconfig\n\nA configuration management for global variables in python projects.\nakconfig is a small python class that takes global variables and lets you manipulate them quickly. the advantage can be that you still need manipulations that are to be changed via arguments, or via environment variables. when executing the example file basic.py, it quickly becomes obvious what this is intended for.\n\nsource: https://github.com/dapkdapk/akconfig<br />\npypi.org: https://pypi.org/project/akconfig/\n\n## get help\n\n```\npoetry run python examples/basic.py --help\nUsage: basic [OPTIONS]\n\nOptions:\n  -c, --config <TEXT TEXT>...  Config parameters are: VAR_A, VAR_B, VAR_C,\n                               VAR_D, VAR_E, VAR_F, VAR_G, VAR_H, VARS_MASK\n  -f, --force-env-vars         Set argument if you want force environment\n                               variables\n  --help                       Show this message and exit.\n```\n\n## example basic\n\n`$ poetry run python ./examples/basic.py`\n\n```\nimport click\nfrom ak.config import AKConfig\n\n"""\nThese are global variables\n"""\nVAR_A = "HELLO WORLD"\nVAR_B = 100\nVAR_C = 3.14\nVAR_D = True\nVAR_E = {"a": "b", "c": "d"}\nVAR_F = ["a", "b", "c", "d"]\nVAR_G = ("a", "b", "c", "d")\nVAR_H = "SECRET"\nVAR_I = r"^\\sTest.*"\nVAR_J = "Some text SECRET should be masked"\nVARS_MASK = ["VAR_H"]\n\n\n@click.command()\n@click.option(\n    "-c",\n    "--config",\n    multiple=True,\n    type=(str, str),\n    help="Config parameters are: {}".format(", ".join(AKConfig.GetGlobals(globals()))),\n)\n@click.option(\n    "-f",\n    "--force-env-vars",\n    is_flag=True,\n    help="Set argument if you want force environment variables",\n)\n@click.option(\n    "-u",\n    "--uncolored-print",\n    is_flag=True,\n    help="Set argument and output is not colored",\n)\ndef main(config, force_env_vars, uncolored_print):\n    cfg = AKConfig(\n        global_vars=globals(),\n        config_args=config,\n        mask_keys=VARS_MASK,\n        force_env_vars=force_env_vars,\n        uncolored=uncolored_print,\n    )\n\n    cfg.print_config()\n\nif __name__ == "__main__":\n    main()\n```\n\n#### output:\n\n```\n+AKCONFIG VARIABLES+----------------------------------+\n| NAME             | VALUE                            |\n+------------------+----------------------------------+\n| VAR_A (str)      | HELLO WORLD                      |\n| VAR_B (int)      | 100                              |\n| VAR_C (float)    | 3.14                             |\n| VAR_D (bool)     | True                             |\n| VAR_E (dict)     | {\'a\': \'b\', \'c\': \'d\'}             |\n| VAR_F (list)     | [\'a\', \'b\', \'d\', \'c\']             |\n| VAR_G (tuple)    | (\'a\', \'b\', \'c\', \'d\')             |\n| VAR_H (str)      | *****                            |\n| VAR_I (str)      | ^\\sTest.*                        |\n| VAR_J (str)      | Some text ***** should be masked |\n| VARS_MASK (list) | [\'VAR_H\']                        |\n+------------------+----------------------------------+\n| Date             | 2025-01-28 01:41:14.481035       |\n+------------------+----------------------------------+\n```\n\n### example click arguments\n\n`poetry run python ./examples/click_args.py -b World -c false`\n\n```\nimport click\nfrom ak.config import AKConfig\n\nVAR_TEST_A = "Hello"\n\n\n@click.command()\n@click.option("-b", "--test-b", envvar="VAR_TEST_B", default="you")\n@click.option("-c", "--test-c", envvar="VAR_TEST_C", default=True, type=click.BOOL)\ndef main(test_b, test_c):\n    cfg = AKConfig(globals(), None, None)\n    result = cfg.get_arg_envvar("test_a", "test_b")\n    print(cfg.VAR_TEST_A, cfg.VAR_TEST_B, cfg.VAR_TEST_C, result)\n\n    cfg.print_config()\n\n\nif __name__ == "__main__":\n    main()\n```\n\n#### output:\n\n```\nHello World False [{\'name\': \'VAR_TEST_B\', \'value\': \'World\', \'default\': \'you\', \'global_env\': None, \'type\': STRING}]\n+AKCONFIG VARIABLES-+----------------------------+\n| NAME              | VALUE                      |\n+-------------------+----------------------------+\n| VAR_TEST_A (str)  | Hello                      |\n| VAR_TEST_B (str)  | World                      |\n| VAR_TEST_C (bool) | False                      |\n+-------------------+----------------------------+\n| Date              | 2025-01-28 01:34:05.127236 |\n+-------------------+----------------------------+\n```',
    'author': 'dapk',
    'author_email': 'dapk@gmx.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
