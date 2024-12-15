<template>
    <div class="menu-view mx-xl my-md">
        <h2>Welcome to Skågen.</h2>
        <AuthStatus :collapsed="false" />
    </div>
</template>

<script>
import AuthStatus from '@/components/shared/AuthStatus.vue';

export default {
    name: 'MobileMenu',
    components: { AuthStatus }
};
</script>

<style scope>
h2 {
    text-align: center;
}
</style>