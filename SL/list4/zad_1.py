import os
import sys


def filter_env_vars(args):
    def sort_dict(dictionary):
        return {key: value for key, value in sorted(dictionary.items(), key=lambda item: item[1])}

    def includes_in_args(var):
        return any(arg in var[1] for arg in args)

    env_vars = dict(os.environ)
    filtered_env_vars = filter(lambda item: includes_in_args(item), env_vars.items()) if len(
        args) > 0 else env_vars
    # we_are_envs = {
    #     "obw1": "hello",
    #     "obw2": "there",
    #     "gg1": "general",
    #     "gg2": "Kenobi"
    # }
    # filtered_env_vars = filter(lambda item: includes_in_args(item), we_are_envs.items()) if len(
    #     args) > 0 else we_are_envs
    return sort_dict(dict(filtered_env_vars))


if __name__ == "__main__":
    #sys.argv[1:]
    print(filter_env_vars(sys.argv[1:]))

