class TypeRegistry:
    def __init__(self, graphql_api):
        self.item_by_name = {}
        self.item_list_by_name = {}

        for query in graphql_api.queries:
            for named_item in query.named_items_provided:
                self.register_item(named_item.typ)
            for named_item_list in query.named_item_lists_provided:
                self.register_item_list(named_item_list.typ)

        for mutation in graphql_api.mutations:
            for item in mutation.items_posted:
                self.register_item(item)
            for named_item in mutation.named_items_returned:
                self.register_item(named_item.typ)
            for named_item_list in mutation.named_item_lists_returned:
                self.register_item_list(named_item_list.typ)

    def get_item_by_name(self, item_name):
        return self.item_by_name.get(item_name)

    def get_item_list_by_name(self, item_name):
        return self.item_list_by_name.get(item_name)

    def get_item_types(self):
        return [x.item_type for x in self.item_by_name.values()]

    def get_items(self):
        return [x for x in self.item_by_name.values()]

    def get_items_that_provide_item(self, item_name):
        return [
            x
            for x in self.get_items()
            if item_name in [i.item_name for i in x.items_provided]
        ]

    def get_items_that_provide_item_list(self, item_name):
        return [
            x
            for x in self.get_items()
            if item_name in [i.item.item_name for i in x.item_lists_provided]
        ]

    def register_item(self, item):
        x = self.item_by_name.get(item.item_name)
        if x:
            if x.id != item.id:
                raise ValueError(
                    f"A different Item with name {item.item_name} already exists"
                )
        else:
            self.item_by_name[item.item_name] = item
            for i in item.items_provided:
                self.register_item(i)
            for i in item.item_lists_provided:
                self.register_item_list(i)

    def register_item_list(self, item_list):
        x = self.item_list_by_name.get(item_list.item_name)
        if x:
            if x.id != item_list.id:
                raise ValueError(
                    f"A different Item with name {item_list.item_name} already exists"
                )
        else:
            self.item_list_by_name[item_list.item_name] = item_list
            self.register_item(item_list.item)
