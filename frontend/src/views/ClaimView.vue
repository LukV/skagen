<template>
  <div class="claim-view">
    <section class="claim-title">
      <div class="claim-label">CLAIM</div>
      <h1 class="claim-heading">
        {{claim}}
        <span class="claim-time">
          <ClockIcon class="icon-xs" /> 16h
        </span>
      </h1>
    </section>

    <!-- Block 2: 'Conflicting Evidence' warning block -->
    <section class="claim-evaluation warning-block">
      <span class="warning-icon">⚠</span>
      This topic has conflicting evidence.
    </section>

    <!-- Block 3: Sources (horizontally scrollable) -->
    <section class="sources">
      <div class="sources-scroller">
        <BaseCard>
          <div class="number">1</div>
          <div class="source">
            Sunstein, C. R. (2018). "Republic: Divided by Social Media."
          </div>
        </BaseCard>
        <BaseCard>
          <div class="number">2</div>
          <div class="source">
            Guess, A., Lyons, B., & Nyhan, B. (2018). The Limited Impact of Echo Chambers on Political Polarization.
            Nature Human Behaviour, 2(9), 723–729.
            <a href="#">Link to article</a>
          </div>
        </BaseCard>
        <BaseCard>
          <div class="number">3</div>
          <div class="source">
            Bakshy, E., Messing, S., & Adamic, L. A. (2015). Exposure to Ideologically Diverse News and Opinion on
            Facebook. Science, 348(6239), 1130–1132.
            <a href="#">Link to article</a>
          </div>
        </BaseCard>
      </div>
    </section>

    <!-- Block 4: Conversation UI -->
    <section class="conversation">
      <!-- user balloon aligned right -->
      <div class="user-text-balloon">
        {{claim}}
      </div>
      <!-- AI balloon aligned left -->
      <div class="ai-text-balloon">
        <p>Social media's role in increasing polarization is a topic of ongoing debate among researchers. Studies
          suggest that:</p>
        <ul>
          <li><b>Echo Chambers</b>: Algorithms often create echo chambers, reinforcing existing beliefs and potentially
            increasing polarization.</li>
          <li><b>Diverse Exposure</b>: Conversely, some studies argue that social media exposes users to a broader range
            of views, which can decrease polarization for certain groups.</li>
          <li><b>Demographics Matter</b>: The effects vary based on factors like age, location, and the platform used.
          </li>
        </ul>
        <div class="icons">:like: :unlike: :copy: :refresh:</div>
      </div>
    </section>

    <!-- Block 5: Follow-up (sticky footer) -->
    <section class="follow-up">
      <div class="input-container">
        <textarea placeholder="Ask follow-up..." rows="3"></textarea>
        <button>
          <span>&#8594;</span>
        </button>
      </div>
    </section>
  </div>
</template>

<script>
import BaseCard from '@/components/base/BaseCard.vue';
import { ClockIcon } from '@heroicons/vue/24/solid';
import { mapState } from 'vuex';

export default {
  name: 'ClaimView',
  components: { BaseCard, ClockIcon },
  computed: {
    ...mapState({
      claim: (state) => state.claim, 
    }),
  },
};
</script>

<style scoped>
.claim-view {
  max-width: 750px;
  margin: 0 auto;
  padding: var(--spacing-md);
}

/* Title Section */
.claim-title {
  margin-bottom: var(--spacing-md);
}

.claim-label {
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 700;
  margin-bottom: var(--spacing-xs);
}

.claim-heading {
  font-family: var(--font-heading);
  font-size: 2rem;
  align-items: baseline;
  line-height: 1.1;
  max-width: 450px;
}

.claim-time {
  font-size: 0.75rem;
  /* smallest font gray */
  color: var(--color-text-lightest);
  margin-left: var(--spacing-sm);
}

/* Warning Block */
.warning-block {
  background-color: #fff3e2;
  border-left: 5px solid var(--color-accent);
  padding: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  max-width: 450px;
}

.warning-icon {
  font-size: 1.25rem;
  color: var(--color-accent);
  margin-right: var(--spacing-xs);
}

/* Sources Section */
.sources {
  margin-bottom: var(--spacing-md);
}

.sources-scroller {
  display: flex;
  gap: var(--spacing-md);
  overflow-x: auto;
  /* horizontal scroll */
  scroll-behavior: smooth;
  padding-bottom: var(--spacing-md);
}

/* Conversation UI */
.conversation {
  margin-bottom: var(--spacing-md);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

/* User text balloon (align right) */
.user-text-balloon {
  align-self: flex-end;
  background-color: var(--color-primary-lightest);
  color: var(--color-text);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 18px;
  max-width: 60%;
  text-align: right;
}

/* AI text balloon (align left) */
.ai-text-balloon {
  align-self: flex-start;
  color: var(--color-text);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 8px;
  max-width: 70%;
}

/* Icons at the bottom of the AI balloon */
.icons {
  margin-top: var(--spacing-sm);
  display: flex;
  gap: var(--spacing-sm);
  color: var(--color-text-lighter);
}

/* Follow-up (sticky footer) */
.follow-up {
  position: sticky;
  bottom: 0;
  padding-top: var(--spacing-md);
  z-index: 10;
}

/* Input container styling from original snippet */
.input-container {
  position: relative;
  width: 100%;
  max-width: 570px;
  margin: 0 auto;
  /* center it */
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

@media (max-width: 600px) {
  .claim-view {
    max-width: 500px;
    padding: var(--spacing-sm);
  }

  .user-text-balloon,
  .ai-text-balloon {
    max-width: 100%;
  }
}
</style>