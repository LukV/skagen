<template>
    <div class="home-page">
        <h1>Your claim, grounded in <br /> open research</h1>

        <!-- Multiline Hypothesis Input Section -->
        <div class="input-container">
            <textarea 
                placeholder="Write your hypotheses here..." 
                rows="3"
                v-model="claim"
                @keyup.enter="handleEnter"></textarea>
            <button @click="submitClaim">
                <span>&#8594;</span>
            </button>
        </div>

        <!-- Suggested Hypotheses -->
        <div class="suggestions">
            <p>Or try these:</p>
            <ul>
                <li>➜ Social media increase polarization</li>
                <li>➜ Solar panels require more energy to produce than they generate in their lifetime.</li>
            </ul>
        </div>

        <!-- Quote Section -->
        <div class="quote">
            <blockquote>
                <em>
                    "... how can you have an opinion if you are not informed? If everybody always lies
                    to you, the consequence is not that you believe the lies, but rather that nobody
                    believes anything any longer. ... And a people that no longer can believe anything
                    cannot make up its mind. It is deprived not only of its capacity to act but also
                    of its capacity to think and to judge. And with such a people you can then do
                    what you please."
                </em>
                <span>– Hannah Arendt (1974)</span>
            </blockquote>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    name: 'HomeView',
    data() {
        return {
            claim: '',
        };
    },
    methods: {
        ...mapActions(['setClaim']),
        submitClaim() {
            if (this.claim.trim()) {
                this.setClaim(this.claim); // Save to Vuex and localStorage
                this.$router.push('/claim');
            }
        },
        handleEnter(event) {
            if (!event.shiftKey) {
                event.preventDefault();
                this.submitClaim();
            }
        },
    },
};
</script>

<style scoped>
.home-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    text-align: center;
    font-family: Inter, sans-serif;
    color: #333;
}

h1 {
    font-family: var(--font-heading, sans-serif) !important;
    font-weight: var(--font-weight-bold, 500);
    font-size: 2.5rem;
}

/* Input Section */
.input-container {
    position: relative;
    width: 100%;
    max-width: 570px;
    margin-bottom: 2rem;
}

textarea {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 10px;
    resize: none;
    box-sizing: border-box;
    outline: none;
}

button {
    position: absolute;
    bottom: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
}

/* Suggestions */
.suggestions {
    width: 100%;
    max-width: 570px;
    text-align: left;
    margin-bottom: 2rem;
}

.suggestions p {
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.suggestions ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.suggestions li {
    font-size: 1rem;
    margin: 0.3rem 0;
}

/* Quote Section */
.quote {
    width: 100%;
    max-width: 570px;
    text-align: left;
    font-size: 1rem;
    line-height: 1.5;
    color: #555;
}

blockquote {
    border-left: 4px solid #ccc;
    padding-left: 1rem;
    margin: 0;
    font-style: italic;
}

blockquote span {
    display: block;
    margin-top: 0.5rem;
    font-weight: 600;
}
</style>