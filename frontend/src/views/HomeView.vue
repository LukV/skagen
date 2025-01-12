<template>
  <v-container fluid class="d-flex align-center justify-center" style="height: 100vh;">
    <div style="max-width: 600px; width: 100%;">
      <h2 class="text-h5 mb-6 text-center">Your claim, grounded in open research</h2>

      <v-textarea clearable variant="outlined" placeholder="Write your claim here..." rows="3" auto-grow
        v-model="claim" class="custom-textarea" @keydown="handleKeydown">
        <template #append-inner>
          <v-btn icon variant="plain" class="bottom-right-icon" @click="submitClaim">
            <v-icon>mdi-arrow-right-thin</v-icon>
          </v-btn>
        </template>
      </v-textarea>
      <div>
        <p class="text-subtitle-1 mb-2">Or try these:</p>
        <div>
          <p class="ml-4 mb-2 clickable" @click="setClaim('Social media increase polarization')">
            ➜ Social media increase polarization
          </p>
          <p class="ml-4 clickable"
            @click="setClaim('Solar panels require more energy to produce than they generate in their lifetime.')">
            ➜ Solar panels require more energy to produce than they generate in their lifetime.
          </p>
        </div>
      </div>

      <v-divider class="my-6"></v-divider>

      <blockquote>
        <em>
          "... how can you have an opinion if you are not informed? If everybody always lies
          to you, the consequence is not that you believe the lies, but rather that nobody
          believes anything any longer. ... And a people that no longer can believe anything
          cannot make up its mind. It is deprived not only of its capacity to act but also
          of its capacity to think and to judge. And with such a people you can then do
          what you please."
        </em>
        <div class="text-right mt-2">– Hannah Arendt (1974)</div>
      </blockquote>
    </div>
  </v-container>
</template>

<script>
import apiClient from "@/utils/apiClient";

export default {
  name: "HomeView",
  data: () => ({
    claim: "",
  }),
  methods: {
    handleKeydown(event) {
      if (event.key === "Enter") {
        if (event.shiftKey) {
          return;
        }
        event.preventDefault();
        this.submitClaim();
      }
    },
    setClaim(claim) {
      this.claim = claim;
    },
    async submitClaim() {
      if (this.claim.trim()) {
        try {
          const response = await apiClient.post("/claims/", {
            content: this.claim,
          });
          const claimId = response.data.id;
          this.$router.push(`/claims/${claimId}`);
        } catch (error) {
          console.error("Error submitting claim:", error.response || error.message);
        }
      } else {
        console.log("Claim is empty");
      }
    },
  },
};
</script>

<style scoped>
.clickable {
  cursor: pointer;
  transition: color 0.3s;
}

.custom-textarea {
  position: relative;
}

.bottom-right-icon {
  position: absolute;
  bottom: 3px;
  right: 3px;
  color: var(--v-theme-on-surface);
}
</style>