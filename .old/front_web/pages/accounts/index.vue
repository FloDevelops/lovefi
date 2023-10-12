<script setup>
  definePageMeta({
    middleware: 'auth'
  });

  const user = useSupabaseUser();
  console.log('user id is', user?.value.id);
</script>

<template>
  <h1>Accounts page</h1>


</template>