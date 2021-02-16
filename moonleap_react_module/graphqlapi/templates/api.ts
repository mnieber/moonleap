import { always, flow } from 'lodash/fp';
import { doQuery } from 'src/utils/graphqlClient';

{% loop item_list in res.module.store.item_lists %}
export function get{{ item_list.item_name|plural|title }}() {
  const query = `query query{{ item_list.item_name|plural|title }} {
    {{ item_list.item_name|plural }} {
      {{ item_list.item_name }} {
        uuid
        name
      }
    }
  }`;
  const vars = {};
  return doQuery(query, vars).then((response) => {
    return {
      {{ item_list.item_name|plural }}: flow(
        always(response.{{ item_list.item_name|plural }}),
      )(),
    };
  });
}
{% endloop %}
