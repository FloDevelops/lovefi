import { queryByCollection } from "../../lib/firestore";


export default defineEventHandler(async (event) => {
  try {
    // const userId = event.context.user.id;
    // to continue...

    const transactions = await queryByCollection('transactions dev');
    return transactions;

  } catch (error) {
    console.log(error)
    return 'api/alpha/transactions.ts: error';
  }
})
