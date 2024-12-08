<template>
    <button
      :class="[
        'base-button',
        `base-button--${variant}`,
        `base-button--${size}`,
        { 'base-button--icon-only': isIconOnly, 'base-button--no-border': noBorder, 'base-button--rounded': rounded }
      ]"
      :disabled="disabled"
    >
      <slot />
    </button>
  </template>
  
  <script>
  export default {
    name: "BaseButton",
    props: {
      variant: { type: String, default: "primary" }, // e.g., "primary", "secondary"
      size: { type: String, default: "md" }, // e.g., "sm", "md", "lg"
      disabled: { type: Boolean, default: false },
      isIconOnly: { type: Boolean, default: false }, // Icon-only button
      noBorder: { type: Boolean, default: false }, // Icon-only without border
      rounded: { type: Boolean, default: false }, // Fully rounded button
    },
  };
  </script>
  
  <style scoped>
  /* Base styles for the button */
  .base-button {
    font-family: var(--font-base, "Inter", sans-serif);
    font-size: var(--font-size-base);
    padding: var(--spacing-sm, 10px) var(--spacing-md, 20px);
    border: 2px solid transparent;
    border-radius: 4px;
    cursor: pointer;
    font-weight: var(--font-weight-bold, 600);
    transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.2s ease, transform 0.1s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  
  /* Disabled state */
  .base-button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  /* Primary variant */
  .base-button--primary {
    background-color: var(--color-primary);
    color: var(--color-text-light);
  }
  
  .base-button--primary:hover {
    background-color: rgba(103, 80, 164, 0.8);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  .base-button--primary:active {
    background-color: rgb(83, 64, 128);
    transform: scale(0.98);
  }
  
  /* Secondary variant */
  .base-button--secondary {
    background-color: var(--color-background, #fff);
    color: var(--color-primary, #6750a4);
    border: 1px solid var(--color-primary, #6750a4);
  }
  
  .base-button--secondary:hover {
    background-color: rgba(103, 80, 164, 0.1);
  }
  
  .base-button--secondary:active {
    background-color: rgba(103, 80, 164, 0.2);
    transform: scale(0.98);
  }
  
  /* Icon-only buttons */
  .base-button--icon-only {
    padding: 0;
    justify-content: center;
  }
  
  /* Icon-only buttons without border */
  .base-button--no-border {
    border: none;
    background: none;
  }
  
  .base-button--no-border:hover {
    background-color: rgba(103, 80, 164, 0.1);
  }
  
  .base-button--no-border:active {
    background-color: rgba(103, 80, 164, 0.2);
  }
  
  /* Rounded button */
  .base-button--rounded {
    border-radius: 50px;
  }
  
  /* Sizes */
  .base-button--sm {
    padding: var(--spacing-xs, 5px) var(--spacing-sm, 10px);
    font-size: 12px;
  }
  
  .base-button--md {
    padding: var(--spacing-sm, 10px) var(--spacing-md, 20px);
  }
  
  .base-button--lg {
    padding: var(--spacing-md, 15px) var(--spacing-lg, 30px);
    font-size: 18px;
  }
  </style>
  