<script setup>
  definePageMeta({
    middleware: 'auth'
  });

  const user = useSupabaseUser();
  console.log('user id is', user?.value.id);

  const { data } = await useFetch('/api/alpha/transactions');
  const transactions = data.value;
  console.log(`${transactions.length} transactions found`);
</script>

<template>
  <h1>Transactions page</h1>

  <div id="transactions-container" class="grid grid-cols-1 gap-4">
    <div v-for="transaction in transactions" :key="transaction.id" class="flex justify-between">
      <p>{{ transaction.date }}</p>
      <p>{{ transaction.merchant_name }}</p>
      <p>{{ transaction.amount }}</p>
    </div>
  </div>

</template>