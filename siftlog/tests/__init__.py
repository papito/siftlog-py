import inspect


def print_method_name():
    print(
        "\n\n===>",
        inspect.stack()[1].frame.f_code.co_name,
        "()\n=====================================\n",
    )
