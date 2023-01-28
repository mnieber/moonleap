import UIkit from 'src/frames/styles/uikit';
import { cn } from 'src/utils/classnames';
import './Icon.scss';

export type PropsT = {
  name: string;
  className?: any;
};

export const Icon = (props: PropsT) => {
  return (
    UIkit && (
      <div
        className={cn('Icon', '!mr-2', props.className)}
        data-uk-icon={`icon: ${props.name}; ratio: 1`}
      ></div>
    )
  );
};