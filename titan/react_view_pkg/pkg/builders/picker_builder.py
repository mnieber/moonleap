from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder import Builder

on_change_template_str = chop0(
    """
    const onChange = (value: PickerValueT) => {
      if (value.__isNew__) {
        // Moonleap Todo: add {{ item }}
      } else if (value.value) {
        props.{{ item|plural }}Selection.selectItem({
          itemId: value.value.id
        });
      }
    };

"""
)

div_template_str = chop0(
    """
    <ValuePicker
        isMulti={false}
        isCreatable={true}
        pickableValues={ props.{{ item|plural }} }
        labelFromValue={(x: any) => x.name}
        pickableValue={props.{{ item|plural }}Highlight.item}
        onChange={onChange}
    />
"""
)


class PickerBuilder(Builder):
    def __post_init__(self):
        self.item_name = None

    def prepare(self):
        self.item_name = self.widget_spec.item_list.item.item_name
        append_uniq(self.output.default_props, f"{self.item_name}:selection")
        append_uniq(self.output.default_props, f"{self.item_name}:highlight")

    def build(self, div_attrs):
        handler_code = get_template_from_str(on_change_template_str).render(
            {
                "item": self.item_name,
            }
        )
        self.add_preamble([handler_code])

        div = get_template_from_str(div_template_str).render(
            {
                "item": self.item_name,
            }
        )
        self.add_lines([div])
