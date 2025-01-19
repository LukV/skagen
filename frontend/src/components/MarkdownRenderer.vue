<template>
    <div v-html="renderedMarkdown" class="my-md"></div>
  </template>
  
<script>
import { marked } from "marked";

export default {
    name: "MarkdownRenderer",
    props: {
        markdown: {
            type: String,
            required: true,
        },
    },
    computed: {
        renderedMarkdown() {
            const sanitizedMarkdown = this.formatMarkdown(this.markdown || "");
            return marked(sanitizedMarkdown, { breaks: true });
        },
    },
    methods: {
        formatMarkdown(markdown) {
            // Ensure each list item starts on a new line
            return markdown.replace(/- /g, "\n- ").trim();
        },
    }
};
</script>

<style>
.my-md ul {
    list-style-type: disc;
    padding-left: 10px !important;
}

.my-md p {
    margin-bottom: 12px;
}
</style>