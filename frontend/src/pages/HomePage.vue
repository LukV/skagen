<template>
  <v-main class="d-flex align-center justify-center" color="background">
    <v-container class="py-12" max-width="lg">
      <!-- Row 1 -->
      <v-row justify="center">
        <!-- Adjusted cols to make Text Block 1 full width on mobile and smaller on larger screens -->
        <v-col cols="12" sm="6" class="text-center">
          <h1 class="mb-6">From academia to your world</h1>
          <p class="mb-6">
            Skågen bridges academia with professionals and the naturally curious, blending intellectual
            rigour with social engagement. Dive into the convergence of ideas, disciplines and perspectives.
          </p>
          <v-btn variant="flat" color="primary" rounded="0">Sign in to explore</v-btn>
        </v-col>
      </v-row>

      <!-- Row 2 -->
      <v-row class="mb-5 align-center" justify="center">
        <!-- Image Section -->
        <v-col cols="12" sm="6" class="d-flex justify-center" order-md="2">
          <v-img src="@/assets/images/illustration-1.png" alt="Illustration 1" max-height="300px" />
        </v-col>
        <!-- Text Section -->
        <v-col cols="12" sm="6" class="d-flex flex-column justify-center align-center" order-md="1">
          <h2 class="mb-4">Build your case with thought-provoking ideas</h2>
          <p class="body-text mb-6">
            Explore summarized content from philosophy, technology, and beyond—reviewed and validated by
            the original researchers. Access cutting-edge, field-specific research without sifting through
            academic journals.
          </p>
          <v-btn variant="flat" color="primary" rounded="0" class="btn-70">
            For enthousiasts and professionals
            <v-icon end>mdi-arrow-right</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <!-- Row 3 -->
      <v-row class="align-center" justify="center">
        <!-- Image Section -->
        <v-col cols="12" sm="6" class="d-flex justify-center">
          <v-img src="@/assets/images/illustration-2.png" alt="Illustration 2" max-height="300px" />
        </v-col>
        <!-- Text Section -->
        <v-col cols="12" sm="6" class="d-flex flex-column justify-center align-center">
          <h2 class="mb-4">Engage with experts and peers</h2>
          <p class="body-text mb-6">
            Learn firsthand how your ideas shape lives and professions. Citation-based interactions replace
            claps with meaningful acknowledgments. We encourage citations from professionals, bloggers, and
            peers.
          </p>
          <v-btn variant="flat" color="primary" rounded="0" class="btn-50">
            For researchers and scholars
            <v-icon end>mdi-arrow-right</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-divider class="my-12"></v-divider>

      <!-- Row 4 -->
      <v-row class="mb-5 align-center" justify="center">
        <!-- Image Section -->
        <v-col cols="12" sm="6" class="d-flex justify-center" order-md="2">
          <v-img src="@/assets/images/illustration-3.png" alt="Illustration 3" max-height="300px" />
        </v-col>
        <!-- Text Section -->
        <v-col cols="12" sm="6" class="d-flex flex-column justify-center align-center" order-md="1">
          <h2 class="mb-4">Skågen is just getting started</h2>
          <p class="body-text mb-6">
            This journey begins in March 25. As one of our first members, your support and ideas will help shape this idea 
            into a space for the better good. Join us to be part and follow our progress as we grow together. We aim for 100+ 
            researchers and 500+ papers in 1 or 2 years.
          </p>
        </v-col>
      </v-row>
      
    </v-container>
  </v-main>
</template>

<style scoped>
h1 {
  font-weight: 400;
  font-family: "Poppins", sans-serif;
  font-size: 58px;
  line-height: 1;
  color: var(--clr-header-text);
}
.btn-50 {
  width: 50%;
}
.btn-70 {
  width: 70%;
}
</style>
