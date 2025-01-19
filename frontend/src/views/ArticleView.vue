<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <!-- Title Section -->
        <v-chip-group class="mt-4">
          <v-chip
            v-for="(keyword, index) in parsedKeywords"
            :key="index"
            rounded
            color="primary"
            class="ma-1"
          >
            {{ keyword }}
          </v-chip>
        </v-chip-group>
        <h2 class="text-h4 mt-6 mb-12 font-weight-normal">
          {{ article?.title }}
        </h2>

        <!-- Image and Quote Section -->
        <v-row class="mb-2">
          <v-col cols="12" md="6">
            <v-img class="rounded-sm" v-if="imageUrl" :src="imageUrl" :alt="imageAlt" cover>
              <template #placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </v-row>
              </template>
            </v-img>
            <small v-if="imageCredit" class="d-block mt-2">
              Photo by
              <a :href="imageCredit.url" target="_blank" rel="noopener">
                {{ imageCredit.name }}
              </a>
              on <a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash</a>
            </small>
          </v-col>

          <v-col cols="12" md="6">
              <div class="font-italic mb-2">
                "The hustle culture worships toil as an idol. But what is your why? Create not from exhaustion but from
                will to
                power—let your work affirm life, not enslave it." #Nietzsche #HustleCulture
              </div>
              <v-divider class="my-3"></v-divider>
              <p>
                By: <strong>{{ article?.authors_formatted }}</strong>
                <br />
                In: <strong>{{ article?.publisher }}</strong>
                <br />
                Published: <strong>{{ article?.year_published }}</strong>
              </p>
          </v-col>
        </v-row>

        <!-- Text Tabs Section -->
        <v-tabs
          v-model="tab"
          align-tabs="left"
          class="mb-6"
        >
          <v-tab :value="1">Layman's Terms</v-tab>
          <v-tab :value="2">Academic Breakdown</v-tab>
          <v-tab :value="3">Full Article</v-tab>
        </v-tabs>

        <v-tabs-window v-model="tab">
          <v-tabs-window-item v-for="n in 3" :key="n" :value="n">
            <v-row>
              <v-col cols="12">
                <span class="text-caption mt-1 mr-2">2 min read</span>
                <v-chip 
                  color="warning" 
                  class="text-caption px-5" 
                  prepend-icon="mdi-alert-circle"
                  rounded>
                    Unverified AI summary
                </v-chip>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="1">
                  <v-btn key="1" variant="text" border size="small" class="ma-1" icon="mdi-content-copy"></v-btn>
                  <v-btn key="2" variant="text" border size="small" class="ma-1" icon="mdi-share-variant-outline"></v-btn>
                  <v-btn key="3" variant="text" border size="small" class="ma-1" icon="mdi-download"></v-btn>
                  <v-btn key="4" size="small" class="ma-1" icon="mdi-bookmark"></v-btn>
              </v-col>
              <v-col cols="12" md="11">
                <MarkdownRenderer :markdown="article?.llm_summary || 'No content available.'" />
              </v-col>
            </v-row>
          </v-tabs-window-item>
        </v-tabs-window>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import apiClient from "@/utils/apiClient";
import MarkdownRenderer from "@/components/MarkdownRenderer.vue";


export default {
  name: "ArticleView",
  components: {
        MarkdownRenderer,
  },
  props: {
    id: {
        type: String,
        required: true,
    },
},
  data() {
    return {
      // Placeholder for fetched data from API
      article: {},
      tab: null,
      imageUrl: null,
      imageAlt: null,
      imageCredit: null,
      article: null,
    };
  },
  mounted() {
    this.fetchArticleData();
  },
  computed: {
    parsedKeywords() {
      if (!this.article?.llm_keywords) return [];
      try {
        // Remove curly braces and split by commas
        const keywords = this.article.llm_keywords
          .replace(/{|}/g, "") // Remove the curly braces
          .split(",") // Split the string into an array
          .map((keyword) => keyword.trim().replace(/^"|"$/g, "")); // Trim and remove quotes
        return keywords;
      } catch (error) {
        console.error("Error parsing llm_keywords:", error);
        return [];
      }
    },
  },
  methods: {
    async fetchArticleData() {
      try {
          const worksResponse = await apiClient.get(`/works/${this.id}`);
          this.article = worksResponse.data;

          if (this.parsedKeywords.length > 0) {
            this.fetchUnsplashImage();
          } else {
            console.warn("No keywords available for Unsplash query.");
          }
      } catch (error) {
          console.error("Error fetching article data:", error);
      }
    },

    async fetchUnsplashImage() {
      console.log(this.parsedKeywords[0]);
      const ACCESS_KEY = "868xzuHP2hq46VZlNfkov2cUrpAYYZ8-LTzUCVzU2Kw"; // Replace with your Unsplash Access Key
      const query = this.parsedKeywords[0];
      const maxWidth = 400; // Maximum width
      const maxHeight = 300; // Maximum height

      try {
        const response = await axios.get("https://api.unsplash.com/search/photos", {
          params: {
            query: query,
            per_page: 1,
          },
          headers: {
            Authorization: `Client-ID ${ACCESS_KEY}`,
          },
        });

        if (response.data.results.length > 0) {
          const image = response.data.results[0];
          this.imageUrl = `${image.urls.raw}&w=${maxWidth}&h=${maxHeight}&fit=crop`;
          this.imageAlt = image.alt_description || "Urban development";
          this.imageCredit = {
            name: image.user.name,
            url: image.user.links.html,
          };
        } else {
          console.error("No images found for the given query.");
        }
      } catch (error) {
        console.error("Error fetching image from Unsplash:", error);
      }
    },
  },
};
</script>

<style scoped>
.card-title {
  font-weight: 700;
}
</style>
