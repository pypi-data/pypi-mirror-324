# akconfig

A configuration management for global variables in python projects.
akconfig is a small python class that takes global variables and lets you manipulate them quickly. the advantage can be that you still need manipulations that are to be changed via arguments, or via environment variables. when executing the example file basic.py, it quickly becomes obvious what this is intended for.

source: https://github.com/dapkdapk/akconfig<br />
pypi.org: https://pypi.org/project/akconfig/

## get help

```
poetry run python examples/basic.py --help
Usage: basic [OPTIONS]

Options:
  -c, --config <TEXT TEXT>...  Config parameters are: VAR_A, VAR_B, VAR_C,
                               VAR_D, VAR_E, VAR_F, VAR_G, VAR_H, VARS_MASK
  -f, --force-env-vars         Set argument if you want force environment
                               variables
  --help                       Show this message and exit.
```

## example basic

`$ poetry run python ./examples/basic.py`

```
import click
from ak.config import AKConfig

"""
These are global variables
"""
VAR_A = "HELLO WORLD"
VAR_B = 100
VAR_C = 3.14
VAR_D = True
VAR_E = {"a": "b", "c": "d"}
VAR_F = ["a", "b", "c", "d"]
VAR_G = ("a", "b", "c", "d")
VAR_H = "SECRET"
VAR_I = r"^\sTest.*"
VAR_J = "Some text SECRET should be masked"
VARS_MASK = ["VAR_H"]


@click.command()
@click.option(
    "-c",
    "--config",
    multiple=True,
    type=(str, str),
    help="Config parameters are: {}".format(", ".join(AKConfig.GetGlobals(globals()))),
)
@click.option(
    "-f",
    "--force-env-vars",
    is_flag=True,
    help="Set argument if you want force environment variables",
)
@click.option(
    "-u",
    "--uncolored-print",
    is_flag=True,
    help="Set argument and output is not colored",
)
def main(config, force_env_vars, uncolored_print):
    cfg = AKConfig(
        global_vars=globals(),
        config_args=config,
        mask_keys=VARS_MASK,
        force_env_vars=force_env_vars,
        uncolored=uncolored_print,
    )

    cfg.print_config()

if __name__ == "__main__":
    main()
```

#### output:

```
+AKCONFIG VARIABLES+----------------------------------+
| NAME             | VALUE                            |
+------------------+----------------------------------+
| VAR_A (str)      | HELLO WORLD                      |
| VAR_B (int)      | 100                              |
| VAR_C (float)    | 3.14                             |
| VAR_D (bool)     | True                             |
| VAR_E (dict)     | {'a': 'b', 'c': 'd'}             |
| VAR_F (list)     | ['a', 'b', 'd', 'c']             |
| VAR_G (tuple)    | ('a', 'b', 'c', 'd')             |
| VAR_H (str)      | *****                            |
| VAR_I (str)      | ^\sTest.*                        |
| VAR_J (str)      | Some text ***** should be masked |
| VARS_MASK (list) | ['VAR_H']                        |
+------------------+----------------------------------+
| Date             | 2025-01-28 01:41:14.481035       |
+------------------+----------------------------------+
```

### example click arguments

`VAR_TEST_A=Hi poetry run python ./examples/click_args.py -b World -c false`

```
import click
from ak.config import AKConfig

VAR_TEST_A = "Hello"


@click.command()
@click.option("-b", "--test-b", envvar="VAR_TEST_B", default="you")
@click.option("-c", "--test-c", envvar="VAR_TEST_C", default=True, type=click.BOOL)
def main(test_b, test_c):
    cfg = AKConfig(globals(), None, None)
    result = cfg.get_arg_envvar("test_a", "test_b")
    print(cfg.VAR_TEST_A, cfg.VAR_TEST_B, cfg.VAR_TEST_C, result)

    cfg.print_config()


if __name__ == "__main__":
    main()
```

#### output:

```
Hi World False [{'name': 'VAR_TEST_B', 'value': 'World', 'default': 'you', 'global_env': None, 'type': STRING}]
+AKCONFIG VARIABLES-+----------------------------+
| NAME              | VALUE                      |
+-------------------+----------------------------+
| VAR_TEST_A (str)  | Hi                         |
| VAR_TEST_B (str)  | World                      |
| VAR_TEST_C (bool) | False                      |
+-------------------+----------------------------+
| Date              | 2025-02-01 09:35:31.698357 |
+-------------------+----------------------------+
```