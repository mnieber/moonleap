import { when } from 'mobx';
import React from 'react';
import { Highlight } from 'skandha-facets/Highlight';
import { Selection } from 'skandha-facets/Selection';
import { isLoading } from '/src/api/getState';

export type PropsT<ValueT> = {
  values: ValueT[];
  highlight?: Highlight;
  selection?: Selection;
  updateUrl?: (value: ValueT) => void;
};

export const useValuePickerState = <ValueT extends { id: string }>(
  props: PropsT<ValueT>
) => {
  const [isUpdating, setIsUpdating] = React.useState(false);
  const [isError, setIsError] = React.useState(false);

  const setItem = React.useMemo(
    () => (value: ValueT) => {
      props.highlight && props.highlight.highlightItem(value.id);
      props.selection && props.selection.selectItem({ itemId: value.id });
      props.updateUrl && props.updateUrl(value);
    },
    [props]
  );

  const setItemWhenReady = (items: ValueT[], id: string) => {
    let item: ValueT | undefined = undefined;
    when(
      () => !!(item = items.find((x: ValueT) => x.id === id)),
      () => {
        item && setItem(item);
        setIsUpdating(false);
        setIsError(false);
      },
      {
        timeout: 10 || 5000,
        onError: () => {
          setIsUpdating(false);
          setIsError(true);
        },
      }
    );
  };

  return {
    isUpdating: isUpdating || isLoading(props.values),
    setIsUpdating,
    isError,
    setItem,
    setItemWhenReady,
  };
};
