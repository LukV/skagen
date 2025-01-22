<template>
    <v-navigation-drawer :model-value="drawer" @update:model-value="$emit('update:drawer', $event)">
        <div class="d-flex justify-space-between align-center py-2 px-4">
            <div class="logo-container">
                <v-icon color="black">
                    mdi-epsilon
                </v-icon>
            </div>
            <h1 class="mb-0">Hypothesis</h1>
            <v-btn variant="plain" icon @click="createNewThread">
                <v-icon>mdi-square-edit-outline</v-icon>
            </v-btn>
        </div>

        <v-list v-model:opened="open" density="compact">
            <template v-slot:activator="{ props }">
                <v-list-item v-bind="props" prepend-icon="mdi-bookshelf" title="Research"></v-list-item>
            </template>
            
        </v-list>

        <v-list v-model:opened="open">
      <v-list-item prepend-icon="mdi-bookshelf" title="Research"></v-list-item>

      <v-list-group value="Claims">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-alpha-c-circle"
            title="Claims"
          ></v-list-item>
        </template>
                <v-list-item
                    v-for="(claim, index) in claims"
                    :key="index"
                    :subtitle="claim.content"
                    @click="navigateToClaim(claim.id)"
                    link
                >
                </v-list-item>
      </v-list-group>
    </v-list>

        <template v-slot:append>
            <v-divider></v-divider>

            <v-list>
                <v-list-item v-for="(link, index) in bottom_links" :key="index">
                    <v-list-item-title>
                        <a :href="link.url" target="_blank">{{ link.title }}</a>
                    </v-list-item-title>
                </v-list-item>
            </v-list>

            <v-divider></v-divider>

            <v-switch
              label="Dark mode"
              class="px-4"
              color="primary"
              v-model="darkMode"
              hide-details
            ></v-switch>
        </template>
    </v-navigation-drawer>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useStore } from 'vuex'
import { useTheme } from 'vuetify'

const theme = useTheme()
const store = useStore()
const darkMode = ref(false)
const claims = computed(() => store.getters.getHypotheses)

// Load claims on mount
onMounted(() => {
    store.dispatch('fetchHypotheses');
});

// Load user preference from localStorage on mount
onMounted(() => {
    const savedTheme = localStorage.getItem('darkMode')
    if (savedTheme !== null) {
        darkMode.value = JSON.parse(savedTheme)
    } else {
        // Default to system preference or light theme
        darkMode.value = theme.global.current.value.dark
    }
})

// Watch darkMode for changes and update theme accordingly
watch(darkMode, (newValue) => {
    theme.global.name.value = newValue ? 'darkTheme' : 'lightTheme'
    localStorage.setItem('darkMode', JSON.stringify(newValue))
})
</script>

<script>
export default {
    props: {
        drawer: {
            type: Boolean,
            required: true,
        },
    },
    emits: ['update:drawer'],
    data: () => ({
        open: ['Users'],
        admins: [
            ['Management', 'mdi-account-multiple-outline'],
            ['Settings', 'mdi-cog-outline'],
        ],
        cruds: [
            ['Create', 'mdi-plus-outline'],
            ['Read', 'mdi-file-outline'],
            ['Update', 'mdi-update'],
            ['Delete', 'mdi-delete'],
        ],
        bottom_links: [
            { title: "About", url: "https://vuetifyjs.com" },
            { title: "Blog", url: "https://vuejs.org" },
            { title: "Contact", url: "https://vuejs.org" },
        ],
    }),
    methods: {
        createNewThread() {
            this.$router.push("/new");
        },
        navigateToClaim(id) {
            this.$router.push(`/claims/${id}`);
        }
    },
};
</script>


<style scoped>
a {
    color: inherit;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>