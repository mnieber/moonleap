def container_item_name(container):
    return (
        container.item_list.item_name
        if container.item_list
        else container.item.item_name
        if container.item
        else ""
    )
