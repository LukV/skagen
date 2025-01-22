<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12" md="8" lg="6">
                <!-- Extracted Topics as Chips -->
                <template v-if="isExtractingTopics">
                    <v-chip class="me-2 mb-4 text-caption" rounded>
                        <v-progress-circular indeterminate :size="10" :width="2" />&nbsp;Loading...
                    </v-chip>
                </template>

                <!-- 2) If we do have topics, show them -->
                <template v-else-if="hasExtractedTopics">
                    <transition name="fade">
                        <div>
                            <v-chip v-for="(topic, index) in claim.extracted_topics" :key="index"
                                class="me-2 mb-4 text-caption" rounded>
                                {{ topic }}
                            </v-chip>
                        </div>
                    </transition>
                </template>

                <!-- 3) Fallback if the pipeline is done (or in unknown state) but no topics found -->
                <template v-else>
                    <div class="text-caption font-weight-medium mb-1">
                        CLAIM
                    </div>
                </template>

                <!-- Title -->
                <div>
                    <transition name="fade">
                        <h2 class="text-h6 mb-4 font-weight-medium">
                            {{ claim?.content }}
                            <small class="text-caption text-secondary" style="font-size: 0.75rem;">
                                <v-icon size="small">mdi-clock-outline</v-icon>
                                {{ formattedDate(claim?.date_created) }}
                            </small>
                        </h2>
                    </transition>
                </div>

                <!-- Classification/Status Box -->
                <div v-if="claim?.status">
                    <!-- If the claim is completed, show classification -->
                    <div v-if="claimState === 'COMPLETED'">
                        <transition name="fade">
                            <div v-if="validation[0]?.classification"
                                :class="getClassification(validation[0]?.classification).boxClass"
                                class="custom-box pa-4">
                                {{ getClassification(validation[0]?.classification).classification }}
                            </div>
                        </transition>
                    </div>

                    <!-- If the claim is in progress (pending/processing), show pipeline messages -->
                    <div v-else-if="claimState === 'IN_PROGRESS'">
                        <transition name="fade">
                            <div class="custom-box pa-4">
                                <v-icon size="small" color="on-primary">mdi-information-outline</v-icon>&nbsp;
                                <div v-if="currentPipelineMessage">
                                    <i>
                                        {{ currentPipelineMessage.title }}
                                        <span v-if="currentPipelineMessage.comment">
                                            {{ currentPipelineMessage.comment }}
                                        </span>
                                    </i>
                                </div>
                                <div v-else>
                                    <i class="thinking-label">Thinking...</i>
                                </div>
                            </div>
                        </transition>
                    </div>

                    <!-- Handle the FAILED state -->
                    <div v-else-if="claimState === 'FAILED'">
                        <div v-if="errors.length">
                            <v-alert type="error" class="mt-4">
                            <div v-for="(error, index) in errors" :key="index">
                                Error: {{ error }}
                            </div>
                            </v-alert>
                        </div>
                        <div v-else>
                            <v-alert type="error" class="mt-4">
                                Validation failed: {{ claim.status }}
                            </v-alert>
                        </div>
                    </div>

                    <!-- Otherwise show a warning if the status is not recognized -->
                    <div v-else>
                        <v-alert type="warning" class="mt-4">
                            Validation could not be completed: {{ claim.status }}
                        </v-alert>
                    </div>
                </div>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" md="11" xl="10">
                <!-- Sources Section (only if completed) -->
                <transition name="fade">
                    <div v-if="claimState === 'COMPLETED'">
                        <h4 class="text-h8 mb-2">
                            <v-icon size="small">mdi-text</v-icon>
                            Sources
                        </h4>
                        <div class="d-flex flex-row overflow-auto source-scroller">
                            <v-card v-for="(source, index) in validation[0]?.sources" :key="index"
                                class="pa-4 me-4 mb-4" outlined style="min-width: 300px; max-width: 300px;">
                                <v-row no-gutters>
                                    <v-col cols="auto">
                                        <div class="source-index text-caption mt-1">
                                            {{ index + 1 }}
                                        </div>
                                    </v-col>
                                    <v-col>
                                        <p class="text-secondary">
                                            {{ source.citation }}
                                            <v-btn icon size="xs" variant="plain" color="primary"
                                                :href="`/articles/${source.work_id}`" rel="noopener"
                                                style="text-transform:none !important; letter-spacing: 0 !important;">
                                                View article
                                            </v-btn>
                                        </p>
                                    </v-col>
                                </v-row>
                            </v-card>
                        </div>
                    </div>
                </transition>

                <!-- Claim balloon -->
                <transition name="fade">
                    <div v-if="claimState === 'COMPLETED'" class="mt-8 claim-balloon">
                        <v-row class="d-flex justify-end">
                            <v-col cols="auto">
                                <v-sheet rounded="xl" class="mx-auto pa-4" color="secondary" :min-width="200"
                                    :max-width="450">
                                    {{ claim?.content }}
                                </v-sheet>
                            </v-col>
                        </v-row>
                    </div>
                </transition>

                <!-- Summary (only if completed) -->
                <transition name="fade">
                    <div v-if="claimState === 'COMPLETED'" class="mt-8">
                        <v-row>
                            <v-col cols="auto">
                                <div class="logo-container">
                                    <v-icon color="black">mdi-epsilon</v-icon>
                                </div>
                            </v-col>
                            <v-col>
                                <MarkdownRenderer :markdown="validation[0]?.motivation || 'No content available.'" />
                            </v-col>
                        </v-row>
                    </div>
                </transition>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import apiClient from "@/utils/apiClient";
import MarkdownRenderer from "@/components/MarkdownRenderer.vue";

export default {
    components: {
        MarkdownRenderer,
    },
    props: {
        id: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            claim: null,
            validation: [],
            sseSource: null,
            pipelineQueue: [],
            currentPipelineMessage: null,
            isProcessingQueue: false,
            displayDuration: 3000,
            errors: []
        };
    },

    computed: {
        claimState() {
            if (!this.claim || this.claim.status === "Loading...") return "LOADING";
            if (["Pending", "Processing"].includes(this.claim.status)) return "IN_PROGRESS";
            if (["Skipped", "Failed"].includes(this.claim.status)) return "FAILED";
            if (this.claim.status === "Completed") return "COMPLETED";
            return "UNKNOWN";
        },
        hasExtractedTopics() {
            return (
                this.claim?.extracted_topics &&
                this.claim.extracted_topics.length > 0
            );
        },
        isExtractingTopics() {
            // If we’re in progress and no topics yet, we show spinner
            return (
                this.claimState === "IN_PROGRESS" &&
                !this.hasExtractedTopics
            );
        },
    },

    watch: {
        id: {
            immediate: true, // Fetch data on initial load
            handler(newId) {
                this.fetchClaimData(newId);
            },
        },
        'claim.status': {
            handler(newStatus, oldStatus) {
                if (oldStatus === 'Processing' && newStatus === 'Completed') {
                    this.$store.dispatch('fetchHypotheses');
                }
            },
        },
    },

    methods: {
        async fetchClaimData() {
            try {
                const claimResponse = await apiClient.get(`/claims/${this.id}`);
                this.claim = { ...this.claim, ...claimResponse.data };

                // Based on the claim’s status, either start SSE, trigger the pipeline,
                // or fetch validations if already completed
                if (this.claim.status === "Pending") {
                    await this.triggerValidationPipeline();
                } else if (this.claim.status === "Processing") {
                    this.startSSE();
                } else if (this.claim.status === "Completed") {
                    await this.fetchValidations();
                }
                // Handle other statuses if needed (Failed, Skipped, etc.)

            } catch (error) {
                console.error("Error fetching claim data:", error);
            }
        },

        async triggerValidationPipeline() {
            try {
                this.startSSE();
                // Trigger the pipeline on the server
                await apiClient.post(`/claims/${this.id}/validations`);
                // We can locally mark it as "Processing" for UI
                this.claim.status = "Processing";
            } catch (error) {
                console.error("Error starting validation pipeline:", error);
            }
        },

        startSSE() {
            this.stopSSE();
            const sseUrl = `${apiClient.defaults.baseURL}/sse/progress/${this.id}`;
            this.sseSource = new EventSource(sseUrl);

            // Make onmessage async so we can `await this.fetchClaimData()`
            this.sseSource.onmessage = async (event) => {
                const data = JSON.parse(event.data);

                if (data.id !== this.id) return; // ignore others

                // Handle errors in the SSE message
                if (data.error) {
                    this.errors.push(data.error);
                    console.error("Pipeline error:", data.error);
                    this.stopSSE();
                    await this.fetchClaimData();
                    return;
                }

                // Update partial data or progress message
                this.pipelineQueue.push(data);
                this.processPipelineQueue();

                if (data.step === "ExtractingTopics" && data.comment) {
                    this.processExtractedTopics(data.comment);
                    data.comment = '';
                }

                // If final SSE step arrives, do a final fetch
                if (data.step === "EvaluatingHypothesis" && data.comment) {
                    // The pipeline is finished. 
                    this.stopSSE();
                    // **Re-fetch** so the claim now has the final topics
                    await this.fetchClaimData();
                }
            };

            this.sseSource.onerror = (err) => {
                console.error("SSE error:", err);
                this.stopSSE();
            };
        },

        stopSSE() {
            if (this.sseSource) {
                this.sseSource.close();
                this.sseSource = null;
            }
        },

        processExtractedTopics(comment) {
            const match = comment.match(/Extracted topics: \[(.*?)\]/);
            if (match) {
                const topics = match[1]
                    .split(",")
                    .map((topic) =>
                        topic
                            .trim()
                            .replace(/^'|'$/g, "") // remove surrounding single quotes
                            .replace(/\b\w/g, (char) => char.toUpperCase()) // capitalize each word
                    );
                this.claim.extracted_topics = topics;
            }
        },

        processPipelineQueue() {
            if (this.isProcessingQueue) return;
            this.isProcessingQueue = true;

            const displayNext = () => {
                if (!this.pipelineQueue.length) {
                    this.isProcessingQueue = false;
                    this.currentPipelineMessage = null;
                    return;
                }
                // Take the next message
                this.currentPipelineMessage = this.pipelineQueue.shift();

                // Display it for `displayDuration` ms
                setTimeout(() => {
                    this.currentPipelineMessage = null;
                    displayNext();
                }, this.displayDuration);
            };

            displayNext();
        },

        async fetchValidations() {
            try {
                const validationResponse = await apiClient.get(`/claims/${this.id}/validations`);
                this.validation = validationResponse.data;
            } catch (error) {
                console.error("Error fetching validation data:", error);
            }
        },

        formattedDate(date) {
            if (!date) return "";
            const now = new Date();
            const givenDate = new Date(date);
            const diffInMs = now - givenDate;
            const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
            const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
            const isSameDay = now.toDateString() === givenDate.toDateString();

            if (diffInMinutes < 5) {
                return "just now";
            } else if (diffInMinutes < 60) {
                return `${diffInMinutes} minutes ago`;
            } else if (isSameDay) {
                return `${diffInHours} hours ago`;
            } else if (
                now.getDate() - givenDate.getDate() === 1 &&
                now.getMonth() === givenDate.getMonth() &&
                now.getFullYear() === givenDate.getFullYear()
            ) {
                return "yesterday";
            } else {
                return givenDate.toLocaleDateString();
            }
        },

        getClassification(label) {
            switch (label) {
                case "A":
                    return {
                        boxClass: "green-box",
                        classification: "Evidence agrees with the hypothesis.",
                    };
                case "B":
                    return {
                        boxClass: "blue-box",
                        classification:
                            "Partially Supported: Some evidence agrees; others are neutral or contradictory.",
                    };
                case "C":
                    return {
                        boxClass: "orange-box",
                        classification: "Inconclusive: Evidence is neutral or conflicting.",
                    };
                case "D":
                    return {
                        boxClass: "red-box",
                        classification: "Refuted: Evidence disagrees with the hypothesis.",
                    };
                default:
                    return {
                        boxClass: "",
                        classification: "No classification available.",
                    };
            }
        },
    },

    created() {
        // If user navigated with some local claimContent
        const claimContent = this.$router.options.history.state?.claimContent;
        if (claimContent) {
            this.claim = { content: claimContent, status: "Loading..." };
        }
        this.fetchClaimData();
    },

    beforeUnmount() {
        this.stopSSE();
    },
};
</script>

<style scoped>
.custom-box {
    border-left: 8px solid rgb(var(--v-theme-primary));
    border-radius: 4px;
    display: flex;
    align-items: center;
    font-size: 1rem;
    background-color: rgb(var(--v-theme-secondary));
    color: rgb(var(--v-theme-on-secondary));
}

/* Green Box */
.green-box {
    background-color: #d7f3e3;
    border-left-color: #1b5e20;
    color: #1b5e20;
}

/* Blue Box */
.blue-box {
    background-color: rgb(var(--v-theme-secondary)) !important;
    border-left-color: #1a4f8a;
    color: rgb(var(--v-theme-on-secondary)) !important;
}

/* Orange Box */
.orange-box {
    background-color: #fdebd3;
    border-left-color: #e65100;
    color: #e65100;
}

/* Red Box */
.red-box {
    background-color: #f9d7d7;
    border-left-color: #b71c1c;
    color: #b71c1c;
}

.text-h6,
.text-caption,
.text-subtitle-2 {
    line-height: 1.2;
}

.source-index {
    background-color: rgb(var(--v-theme-secondary));
    border-radius: 50%;
    width: 15px;
    height: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: rgb(var(--v-theme-on-secondary));
    margin-right: 8px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
    opacity: 1;
}

.thinking-label {
    animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {

    0%,
    100% {
        opacity: 0.7;
        filter: brightness(100%);
    }

    50% {
        opacity: 1;
        filter: brightness(120%);
    }
}
</style>