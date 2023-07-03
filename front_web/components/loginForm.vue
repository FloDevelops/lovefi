<script>
  import Clerk from "@clerk/clerk-js";

  const config = useRuntimeConfig()
  const publishableKey = config.public.clerkPublishableKey;

  const clerk = new Clerk(publishableKey);
  await clerk.load({
    // Set load options here...
  });
</script>