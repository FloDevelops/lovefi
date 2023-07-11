const config = useRuntimeConfig();
import { Configuration, PlaidApi, PlaidEnvironments } from 'plaid';

const configuration = new Configuration({
  basePath: PlaidEnvironments.development,
  baseOptions: {
    headers: {
      'PLAID-CLIENT-ID': config.plaidClientId,
      'PLAID-SECRET': config.plaidSecretDevelopment,
    },
  },
});

const client = new PlaidApi(configuration);