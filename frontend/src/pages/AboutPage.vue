<template>
  <v-main>
    <!-- Hero Section -->
    <v-container fluid class="pa-0">
      <v-img :src="require('@/assets/images/skagen_vesterbrofotograferne.jpg')"
        class="d-flex align-center justify-center" contain>
        <h1 class="display-2 hero-title text-center">
          Ideas that ripple
        </h1>

        <div class="caption-container">
          <span class="caption">Photo: Vesterbrofotograferne</span>
        </div>
      </v-img>
    </v-container>

    <!-- Main Content -->
    <v-container>
      <!-- Introduction -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h2 class="mt-6">Skågen Bright Minds Service </h2>
          <p class="drop-cap">
            Tis a paradox of our times: we have more access to more information than ever before... Yet depth and
            understanding seem to elude us. We scroll endlessly through feeds, engage in <strong>algorithmically
            optimized debates</strong>, and consume content in split seconds. The questions that truly matter — questions
            about ethics, technology, and our humanity — drown in shallowness.
          </p>
          <p>
            At Skågen we have a - granted naive - intention to bring depth back. We aim to help bridge academia and your
            world. Be a place where knowledge becomes accessible <strong>without losing its complexity</strong>. A platform where ideas find
            their way to professionals, curious individuals, and anyone seeking answers beyond the surface.
          </p>
        </v-col>
      </v-row>

      <v-divider class="mb-6"></v-divider>

      <!-- The Spirit of Our Time -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h2>Why do we care</h2>
          <p>
            In a world where technology and commerce dominate, Skågen offers a counterbalance. Our time is marked by
            four profound challenges: 
          </p>
        </v-col>
      </v-row>

      <!-- Challenges Sections -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h3>1. The Overabundance of the Shallow</h3>
          <p class="drop-cap">
            We are overwhelmed with content designed to grab our attention, not to enrich our minds. Social media has
            created an economy of shallowness, where engagement matters more than substance. Young people report rising
            rates of depression, as highlighted by studies from the Center for Humane Technology. We like, share, and
            scroll—but we do not learn.
          </p>

          <h3>2. Truth in Decline</h3>
          <p class="drop-cap">
            Fake news, political propaganda, and commercial manipulation have created a society where truth feels like a
            fluid concept. A study by the European Digital Media Observatory shows that false information spreads six
            times faster than corrections. This isn’t just a problem of misinformation; it’s a problem of trust.
          </p>

          <h3>3. Your Data Is Not Your Own</h3>
          <p class="drop-cap">
            The digital world has transformed us from users to products. The Cambridge Analytica scandal and countless
            data breaches are just the tip of the iceberg. Our personal data has become a commodity, and even our
            contributions — knowledge, creativity — are locked in data silos.
          </p>

          <h3>4. AI: Partner or Parasite?</h3>
          <p class="drop-cap">
            AI can be an ally, but it can also make us complacent in our thinking. It demands a healthy dose of
            skepticism and a strategic approach to collaboration. AI should never replace human but can serve as 
            a catalyst for insight. You're critical on media coverage as well are you not, or your neighbour's 
            take on the state of things.
          </p>
        </v-col>
      </v-row>

      <v-divider class="mb-6"></v-divider>

      <!-- How Skågen Works -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h2>How Skågen Works</h2>
          <p>Our features are simple:
          </p>

          <h3>1. Cite This: Meaningful Interactions</h3>
          <p>
            On Skågen, claps are replaced by citations. When you appreciate an article, you can show how it inspired or
            influenced you. This goes beyond superficial recognition; it provides researchers with direct feedback on
            the impact of their work.
          </p>

          <h3>2. AI, But With Limits</h3>
          <p>
            We use AI to summarize complex academic papers into accessible texts, but encourage human oversight. Our
            AI summaries are evaluated, reviewed and in the best case approved by the original authors. No algorithm can replace
            nuance, but it can pave the way to understanding.
          </p>

          <h3>3. Your Data, Your Control</h3>
          <p>
            With Solid pods, your data remains yours. This means you not only have access to your information but also
            decide who gets to see it. In a world where privacy feels like a luxury, at Skågen, it’s a core value.
          </p>

          <h3>4. Openness Through Connection</h3>
          <p>
            Thanks to the ActivityPub protocol, Skågen integrates seamlessly with platforms like Mastodon. This ensures
            that knowledge doesn’t stay locked in but flows freely across a decentralized network.
          </p>
        </v-col>
      </v-row>

      <!-- Who Is Skågen For? -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h2>Who Is Skågen For?</h2>
          <p>
            Skågen is for researchers, professionals, and curious minds:
          </p>

          <h3>For Researchers</h3>
          <p>
            Skågen offers a platform beyond academic journals. Reach new audiences, understand how your work is used,
            and see the real-world impact of your research.
          </p>

          <h3>For Professionals</h3>
          <p>
            Whether you work in technology, healthcare, or education, Skågen delivers cutting-edge insights—without the
            barriers of dense academic texts.
          </p>

          <h3>For Curious Minds</h3>
          <p>
            Skågen is a place for those who want to understand, debate, and learn. No academic background is
            required—only an open mind.
          </p>
        </v-col>
      </v-row>

      <v-divider class="mb-6"></v-divider>

      <!-- Our Vision -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h2>It's politics</h2>
          <p class="drop-cap">
            Skågen is no platform; it’s an initiative. Our core values are clear:
          </p>
          <ul class="ml-6 mb-6">
            <li><strong>Progressive:</strong> Oppose over Obey. Connect over Divide.</li>
            <li><strong>Privacy First:</strong> Your data remains your property, stored in personal vaults.</li>
            <li><strong>Anti Big Tech:</strong> Innovation comes from tinkering, not from cust cotting mania and investor relations.</li>
          </ul>
          <p>
            We believe knowledge is political. It’s a force that can unite, inspire, and transform.
          </p>
        </v-col>
      </v-row>

      <!-- About the Founder -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h2>About me</h2>
          <p class="drop-cap">
            "Skågen is a Brussels-based initiative, led by me, Luk Verhelst. As a data engineer, I see the enormous
            potential of academic research—but also the barriers preventing it from reaching our daily lives. As a
            father, I worry about the impact of shallow social media on future generations. Skågen is my attempt to turn
            the tide — to bring depth and awareness back into a world that desperately needs it."
          </p>
        </v-col>
      </v-row>

      

    </v-container>
  </v-main>
</template>

<script>
export default {
  name: 'AboutPage',
  methods: {
    goToSignUp() {
      // Navigate to the sign-up page
      this.$router.push({ name: 'SignUp' });
    },
  },
};
</script>

<style scoped>
h1,
h2,
h3,
p {
  margin-bottom: 20px;
}

h1 {
  font-weight: 400;
  font-family: "Poppins", sans-serif;
  font-size: 58px;
  line-height: 1;
  color: var(--clr-header-text);
}

.hero-title {
  color: white;
}

/* Caption styling */
.caption-container {
  position: absolute;
  bottom: 8px;
  left: 16px;
}

.caption {
  color: white;
  font-size: 0.8em;
}

/* Apply a serif font to the main content */
.v-main {
  font-family: 'Georgia', serif;
}

/* Drop Cap styling */
.drop-cap::first-letter {
  font-size: 3em;
  float: left;
  line-height: 1;
  margin-right: 0.1em;
  font-weight: bold;
}

/* Background color for surface */
.v-main {
  background-color: var(--v-theme-surface);
}
</style>
