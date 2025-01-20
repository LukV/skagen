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
              <div class="mb-2">
                {{ article?.llm_phrase }}
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
          <v-tabs-window-item :value="1">
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
          <v-tabs-window-item :value="2">
            <MarkdownRenderer :markdown="article?.llm_extended_summary || 'No content available.'" />
          </v-tabs-window-item>
          <v-tabs-window-item :value="3">
            <v-row>
              <!-- Explanation Section -->
              <v-col cols="12" sm="5">
                <v-card outlined class="pa-4" variant="text">
                  <v-card-text>
                    <h3 class="text-h6 font-weight-bold mb-4">Open access to research</h3>
                    <p class="mb-4">
                      The display and download links will take you to our partner's site. 
                      CORE is a global open-access platform for academic research articles. 
                      It aggregates research outputs from repositories and journals, providing 
                      free access to millions of scholarly articles to support knowledge sharing 
                      and collaboration.
                    </p>
                    <p>
                      Use the "Display" button to view the full article on the CORE
                      website, or the "Download" button to get a copy of the article in PDF format.
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Buttons Section -->
              <v-col cols="12" sm="7">
                <v-card outlined class="pa-4">
                  <v-card-text>
                    <h3 class="text-h6 font-weight-bold mb-4">Access the full article</h3>
                    <p class="mb-2">
                      Below are two options for accessing the article:
                    </p>
                    <ul style="margin-left:10px">
                      <li class="mb-2">
                        <strong>Display Full Article</strong>: Opens the article in your
                        browser on CORE's platform.
                      </li>
                      <li class="mb-6">
                        <strong>Download Full Article</strong>: Downloads a PDF copy of
                        the article directly to your device.
                      </li>
                    </ul>
                    <v-btn
                      :href="getLink('display')"
                      target="_blank"
                      color="primary"
                      class="my-6"
                      prepend-icon="mdi-eye"
                      block
                    >
                      Display Full Article
                    </v-btn>
                    <v-btn
                      :href="getLink('download')"
                      target="_blank"
                      color="success"
                      class="my-6"
                      prepend-icon="mdi-download"
                      block
                    >
                      Download Full Article
                    </v-btn>
                  </v-card-text>
                </v-card>
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

    getLink(type) {
      return this.article?.links?.find((link) => link.type === type)?.url || "#";
    },

    async fetchUnsplashImage() {
      console.log(this.parsedKeywords[0]);
      const ACCESS_KEY = "868xzuHP2hq46VZlNfkov2cUrpAYYZ8-LTzUCVzU2Kw"; 
      const query = this.parsedKeywords[0];
      const maxWidth = 400; // 4:3 aspect ratio
      const maxHeight = 300;

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
