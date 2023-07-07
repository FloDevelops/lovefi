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
</template>