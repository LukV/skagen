<template>
    <div>
        <AppHeader />
        <main>
            <router-view />
        </main>
        <footer>
            <p>Footer</p>
        </footer>
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