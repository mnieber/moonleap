from moonleap.utils.merge_into_config import merge_into_config


def get_flags(app_module):
    result = {}
    for flags in app_module.flags.merged:
        merge_into_config(result, flags.values)

    for tool in app_module.service.tools:
        for flags in tool.flags.merged:
            merge_into_config(result, flags.values)

    return result
