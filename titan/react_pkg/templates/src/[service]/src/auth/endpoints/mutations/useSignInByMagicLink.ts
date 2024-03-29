import { useObservableMutation } from '/src/api/ObservableMutation';
import { doQuery, setToken } from '/src/api/graphqlClient';
import { AuthState } from '/src/auth/AuthState';
import { invalidateLoadUserId } from '/src/auth/endpoints';
import { States } from '/src/auth/endpoints/states';
import { hasErrorCode, isError } from '/src/auth/endpoints/utils';
import { ObjT } from '/src/utils/types';

export type ArgsT = {
  magicLinkToken: string;
};

export function signInByMagicLink(args: ArgsT) {
  return doQuery(
    `mutation ($magicLinkToken: String!) {
      signInByMagicLink(
        magicLinkToken: $magicLinkToken
      ) {
        success,
        errors,
        token,
        refreshToken
      }
    }`,
    {
      magicLinkToken: args.magicLinkToken,
    }
  ).then((response: ObjT) => {
    if (
      hasErrorCode(
        ['signInByMagicLink', 'errors', 'magicLinkToken'],
        'NOT_FOUND'
      )(response)
    )
      return {
        success: false,
        errors: [States.MAGIC_LINK_TOKEN_NOT_FOUND],
      };

    if (
      hasErrorCode(
        ['signInByMagicLink', 'errors', 'magicLinkToken'],
        'ACCOUNT_UNKNOWN'
      )(response)
    )
      return {
        success: false,
        errors: [States.MAGIC_LINK_EMAIL_UNKNOWN],
      };

    if (isError(['signInByMagicLink', 'errors'])(response))
      return {
        success: false,
        errors: [States.SIGN_IN_BY_MAGIC_LINK_FAILED],
      };

    const token = response.signInByMagicLink.token;
    const refreshToken = response.signInByMagicLink.refreshToken;
    setToken(token, refreshToken);

    return {
      success: true,
    };
  });
}

export const useSignInByMagicLink = (authState?: AuthState) => {
  const queryName = 'signInByMagicLink';

  return useObservableMutation({
    mutationFn: signInByMagicLink,
    onMutate: () => {
      if (authState) authState.onUpdating(queryName);
    },
    onSuccess: (data: ObjT) => {
      if (authState) authState.onUpdated(queryName, data);
      invalidateLoadUserId({});
    },
    onError: (error: Error) => {
      if (authState) authState.onErrored(queryName, error.message);
    },
  });
};
