import { observer } from 'mobx-react-lite';
import { isNil } from 'ramda';
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';

export interface PickerValueT {
  value: any;
  label: string;
  __isNew__?: boolean;
}

export type PropsT<ValueT> = {
  isMulti: boolean;
  isCreatable: boolean;
  pickableValues: ValueT[];
  pickableValue: ValueT;
  labelFromValue: (value: any) => string;
  labelFromPickedValue?: (value: any) => string;
  [k: string]: any;
  className?: any;
};

export const ValuePicker = observer(
  <ValueT, ConcretePropsT extends PropsT<ValueT>>(
    props: ConcretePropsT
  ): JSX.Element => {
    const {
      isMulti,
      isCreatable,
      pickableValue,
      pickableValues,
      labelFromValue,
      labelFromPickedValue,
      ...others
    } = props;

    const toPickerValue = (pickableVal: any) => {
      return pickableVal.__isNew__
        ? pickableVal
        : {
            value: pickableVal,
            label: labelFromValue(pickableVal),
          };
    };

    const toPickedValue = (pickableVal: any) => {
      return pickableVal.__isNew__
        ? pickableVal
        : {
            value: pickableVal,
            label: (labelFromPickedValue ?? labelFromValue)(pickableVal),
          };
    };

    const options = pickableValues.map(toPickerValue);

    const pickerProps = {
      isMulti: isMulti,
      options,
      value: isNil(pickableValue)
        ? null
        : isMulti
        ? (pickableValue as any).map(toPickedValue)
        : toPickedValue(pickableValue),
      onKeyDown: (e: any) => {
        if (others.onKeyDown) {
          others.onKeyDown(e);
        }
      },
      ...others,
    };

    const picker = isCreatable ? (
      <CreatableSelect {...pickerProps} />
    ) : (
      <Select {...pickerProps} />
    );

    return (
      <div className={props.className} style={{ zIndex: others.zIndex }}>
        {picker}
      </div>
    );
  }
);
