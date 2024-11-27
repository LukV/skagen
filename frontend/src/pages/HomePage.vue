<template>
    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
        <v-container class="py-6" max-width="lg">
            <v-row justify="center">
                <v-col cols="6" class="text-center">
                    <h1 class="mb-6">From academia to your world</h1>
                    <p class="mb-8">
                        Skågen bridges academia with professionals and the naturally curious, blending intellectual
                        rigour with social engagement. Dive into the convergence of ideas, disciplines and perspectives.
                    </p>
                    <v-btn variant="flat" color="secondary">Sign in to explore</v-btn>
                </v-col>
            </v-row>
    <!-- Row 1 -->
    <v-row class="mb-12" justify="center">
      <!-- Text Section -->
      <v-col cols="12" md="6">
        <h2>Build your case with thought-provoking ideas</h2>
        <p class="body-text">
          Explore summarized content from philosophy, technology and beyond - reviewed and validated by the original researchers. Access to cutting-edge field-specific research without needing to dig through academic journals.
        </p>
        <v-btn variant="flat" color="secondary" class="cta-button">
          For professionals and enthusiasts
          <v-icon end>mdi-arrow-right</v-icon>
        </v-btn>
      </v-col>
      <!-- Image Section -->
      <v-col cols="12" md="6" class="d-flex justify-center">
        <v-img src="https://via.placeholder.com/400x300" alt="Placeholder image" max-width="100%" />
      </v-col>
    </v-row>

    <!-- Row 2 -->
    <v-row justify="center">
      <!-- Image Section -->
      <v-col cols="12" md="6" class="d-flex justify-center">
        <v-img src="https://via.placeholder.com/400x300" alt="Placeholder image" max-width="100%" />
      </v-col>
      <!-- Text Section -->
      <v-col cols="12" md="6">
        <h2>Engage with experts and peers</h2>
        <p class="body-text">
          Learn first-hand how your ideas shape lives and professions. Citation-based interactions replace claps with meaningful acknowledgments. We encourage cites from professionals, bloggers, and peers.
        </p>
        <v-btn variant="flat" color="secondary" class="cta-button">
          For researchers and scholars
          <v-icon end>mdi-arrow-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
    </v-main>
</template>

<style scoped>
h1 {
    font-weight: 600;
    font-family: "Poppins", sans-serif;
    font-size: 28px;
    color: var(--clr-header-text);
}

p {
    color: var(--clr-subtext);
}
</style>