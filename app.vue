<script setup lang="ts">
useHead({
  title: 'LoveFi',
  meta: [
    { name: 'description', content: 'Financial Independance for you and your loved ones.' }
  ],
  bodyAttrs: {
    class: 'test'
  },
  script: [ { innerHTML: 'console.log(\'Hello world\')' } ]
})
</script>


<template>
    <theHeader />
  <div>
    <NuxtPage />
  </div>
</template>
