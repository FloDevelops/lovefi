export default defineEventHandler((event) => {
  console.log(`New request: ${getRequestURL(event)}`);
  // console.log(`Event: ${event}`);
  // console.log(`Request: ${Object.keys(event.node.req)}`);
  // console.log(`UserId: ${event.context.user.id}`);
})
