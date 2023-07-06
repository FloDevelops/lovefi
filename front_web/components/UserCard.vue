<script setup lang="ts">
  const supabase = useSupabaseAuthClient();

  const login = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
    });
    if (error) {
      console.error(error);
    }
  };

  const logout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error(error);
      return;
    }
    await navigateTo('/login');
  };

  const user = useSupabaseUser();
  if (user.value) {
    console.log('UserCard component: user is logged in', user.value);
  }
  const name = computed(
    () => user?.value!.user_metadata.full_name
  );
  const profile = computed(
    () => user?.value!.user_metadata.avatar_url
  );    
</script>

<template>
  <div
    v-if="user"
    class="rounded p-3 flex items-center space-x-3 bg-white"
  >
    <img
      class="rounded-full w-12 h-12 border-2 border-blue-400"
      :src="profile"
    />
    <div class="text-right">
      <div class="font-medium">{{ name }}</div>
      <button
        class="text-sm underline text-slate-500" @click="logout"
      >
        Log out
      </button>
    </div>
  </div>
  <div v-else>
    <button
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      @click="login"
    >
      Login
    </button>
  </div>
</template>