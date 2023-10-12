export default defineNuxtRouteMiddleware((to, _from) => {
  const user = useSupabaseUser()

  if (!user.value) {
    console.log('auth middleware, user not logged in')
    return navigateTo('/login')
  }

  console.log('auth middleware, user logged in', user.value)
})
