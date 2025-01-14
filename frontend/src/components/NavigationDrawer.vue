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

        <v-list>
            <v-list-item v-for="[icon, text] in main_links" :key="icon" :prepend-icon="icon" :title="text"
                link></v-list-item>
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
              @click="toggleTheme"
              hide-details
            ></v-switch>
        </template>
    </v-navigation-drawer>
</template>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

function toggleTheme () {
  theme.global.name.value = theme.global.current.value.dark ? 'lightTheme' : 'darkTheme'
}
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
        main_links: [
            ["mdi-bookshelf", "Research"],
            ["mdi-alpha-c-circle", "Claims"],
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