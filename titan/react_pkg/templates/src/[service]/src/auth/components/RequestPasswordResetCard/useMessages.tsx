import type { RoutesT as AuthRoutesT } from '/src/auth/routeTable';
import { RouterLink } from '/src/routes/components';
import { getRouteFns } from '/src/routes/routeTable';

export const useMessages = () => {
  const routes = getRouteFns<AuthRoutesT>();

  const haveYouFoundYourPassword = (
    <div>
      If you've found your password then you can{' '}
      <RouterLink
        key="_signIn"
        dataCy="linkToSignIn"
        to={routes.signIn()}
        className="ml-1"
      >
        sign in
      </RouterLink>
      .
    </div>
  );

  return {
    messages: {
      haveYouFoundYourPassword,
      divYourPasswordHasBeenReset:
        "You've requested a password reset. " +
        'Please check your email for further instructions.',
    },
  };
};
