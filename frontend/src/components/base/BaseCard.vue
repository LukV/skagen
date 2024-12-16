<template>
    <div class="base-card">
        <!-- Slot content goes here -->
        <slot />
    </div>
</template>

<script>
export default {
    name: 'BaseCard'
};
</script>

<style>
.base-card {
    display: flex;
    min-width: 220px;
    background-color: var(--color-background-darker);
    border-radius: 8px;
    gap: 8px;
    padding: var(--spacing-md);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.number {
  font-weight: var(--font-weight-bold);
  font-size: 0.65rem;
  color: var(--color-background); /* White text for contrast */
  background-color: #6e6e6e; /* Darkish-gray background */
  border-radius: 50%; /* Makes it a perfect circle */
  width: 16px; /* Fixed width */
  height: 16px; /* Fixed height to match width */
  min-width: 16px;
  display: flex; /* Align content in the center */
  align-items: center; /* Vertically center text */
  justify-content: center; /* Horizontally center text */
  text-align: center;
  line-height: 1; /* Fixes vertical text alignment */
}

.source {
    font-size: 0.875rem;
    color: var(--color-text);
    line-height: 1.4;
}

.source a {
    color: var(--color-link);
    text-decoration: underline;
    margin-left: var(--spacing-xs);
    font-size: 0.8rem;
}
</style>