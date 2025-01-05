import vine from '@vinejs/vine'

const email = vine.string().email().normalizeEmail()

export const registerValidator = vine.compile(
  vine.object({
    email,
    password: vine.string().minLength(8),
  })
)
export const loginValidator = vine.compile(
  vine.object({
    email,
    password: vine.string(),
  })
)
