<template>
  <div class="claim-view">
    <!-- Block 1: Title -->
    <section class="block block-title">
      <h1>Social media increase polarization</h1>
    </section>

    <!-- Block 2: Warning -->
    <section class="block block-warning">
      <div class="warning">
        <svg class="warning-icon" width="24" height="24" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="#FFA500" stroke-width="2" fill="none" />
          <line x1="12" y1="8" x2="12" y2="14" stroke="#FFA500" stroke-width="2" />
          <circle cx="12" cy="17" r="1" fill="#FFA500" />
        </svg>
        <span>This topic has conflicting evidence.</span>
      </div>
    </section>

    <!-- Block 3: Content -->
    <section class="block block-content">
      <p>
        Social media's role in increasing polarization is a topic of ongoing debate among researchers. Studies suggest that:
      </p>
      <ul>
        <li><strong>Echo Chambers:</strong> Algorithms often create echo chambers, reinforcing existing beliefs and potentially increasing polarization.</li>
        <li><strong>Diverse Exposure:</strong> Conversely, some studies argue that social media exposes users to a broader range of views, which can decrease polarization for certain groups.</li>
        <li><strong>Demographics Matter:</strong> The effects vary based on factors like age, location, and the platform used.</li>
      </ul>
    </section>

    <!-- Block 4: Sources -->
    <section class="block block-sources">
      <h2>Sources</h2>
      <ul>
        <li>Sunstein, C. R. (2018). "Republic: Divided by Social Media."</li>
        <li>
          Guess, A., Lyons, B., & Nyhan, B. (2018). The Limited Impact of Echo Chambers on Political Polarization. <a href="#">Link to article</a>
        </li>
        <li>
          Bakshy, E., Messing, S., & Adamic, L. A. (2015). Exposure to Ideologically Diverse News and Opinion on Facebook. <a href="#">Link to article</a>
        </li>
      </ul>
    </section>

    <!-- Block 5: Textarea -->
    <section class="block block-followup">
      <label for="followup">Ask follow up...</label>
      <textarea id="followup" placeholder="Ask follow up..."></textarea>
      <button class="submit-button">
        <svg width="24" height="24" viewBox="0 0 24 24">
          <path d="M2 12h20M14 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" />
        </svg>
      </button>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ClaimView',
};
</script>

<style scoped>
/* General Layout */
.claim-view {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-gap: 16px;
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
  box-sizing: border-box;
}

.block {
  padding: 1rem;
}

/* Block Styling */
.block-title {
  grid-column: span 3;
  text-align: left;
}

.block-warning {
  grid-column: span 2;
  display: flex;
  align-items: center;
  background-color: #fffaf0;
  border: 1px solid #ffa500;
}

.warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ffa500;
  font-weight: 600;
}

.warning-icon {
  flex-shrink: 0;
}

.block-content {
  grid-column: span 3;
}

.block-content ul {
  margin-top: 0.5rem;
  padding-left: 1.5rem;
}

.block-sources {
  grid-column: span 2;
}

.block-sources h2 {
  margin-bottom: 0.5rem;
}

.block-sources ul {
  padding-left: 1.5rem;
}

.block-sources a {
  color: #3366cc;
  text-decoration: underline;
}

.block-followup {
  grid-column: span 5;
  position: relative;
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.block-followup label {
  position: absolute;
  top: -10px;
  left: 10px;
  font-size: 0.9rem;
  background-color: #f9f9f9;
  padding: 0 0.5rem;
  color: #888;
}

.block-followup textarea {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  resize: none;
}

.block-followup .submit-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #888;
  padding: 0.5rem;
}

/* Responsive Layout */
@media (max-width: 600px) {
  .claim-view {
    grid-template-columns: 1fr;
  }
}
</style>