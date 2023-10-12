<template>
  <header>

    <div class="flex justify-between">
      <div class="flex-1">
        <nuxt-link to="/">LoveFi</nuxt-link> |
        <nuxt-link to="/login">Login</nuxt-link> |
        <nuxt-link to="/transactions">Transactions</nuxt-link> | 
        <nuxt-link to="/accounts">Accounts</nuxt-link>
      </div>
      <div class="flex-0 grow-0">
        <UserCard />
      </div>
    </div>

  </header>
</template>
