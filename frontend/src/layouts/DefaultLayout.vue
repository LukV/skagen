<template>
    <div>
        <AppHeader />
        <main>
            <router-view />
        </main>
    </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';

export default {
  components: {
    AppHeader,
  },
};
</script>