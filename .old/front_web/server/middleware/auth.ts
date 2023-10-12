import { serverSupabaseUser } from '#supabase/server'

export default defineEventHandler(async (event) => {
  // event.context.user = await serverSupabaseUser(event);
  event.context.user = {
    id: 'flo',
  }
})