import { observer } from 'mobx-react-lite';
import React from 'react';
import { useMessages } from './useMessages';
import { AuthFrame } from '/src/auth/components/AuthFrame';
import { RequestPasswordResetForm } from '/src/auth/components/RequestPasswordResetForm';
import { useRequestPasswordReset } from '/src/auth/endpoints';
import { States } from '/src/auth/endpoints/states';
import { useAuthStateContext } from '/src/auth/hooks';

export const RequestPasswordResetPage = observer(() => {
  const { messages } = useMessages();
  const authState = useAuthStateContext(true);
  const requestPasswordReset = useRequestPasswordReset(authState).mutateAsync;

  return (
    <AuthFrame header="Reset your password" id="RequestPasswordResetPage">
      {authState.state === States.REQUEST_PASSWORD_RESET_SUCCEEDED && (
        <div>{messages.divYourPasswordHasBeenReset}</div>
      )}
      {authState.state !== States.REQUEST_PASSWORD_RESET_SUCCEEDED && (
        <RequestPasswordResetForm
          requestPasswordReset={(email: string) => {
            return requestPasswordReset({ email });
          }}
          errors={authState.errors}
          className="mb-4"
        />
      )}
      <div>{messages.haveYouFoundYourPassword}</div>
    </AuthFrame>
  );
});
