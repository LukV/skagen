<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12" md="8" lg="6">
                <!-- Extracted Topics as Chips -->
                <div class="extracted-topics mb-4">
                    <v-chip v-for="(topic, index) in claim?.extracted_topics" :key="index" class="me-2 text-caption" rounded>
                        {{ topic }}
                    </v-chip>
                </div>
                <div>
                    <h2 class="text-h6 mb-4 font-weight-medium">
                        {{ claim?.content }}
                        <small class="text-caption text-secondary" style="font-size: 0.75rem;">
                            <v-icon size="small">mdi-clock-outline</v-icon>
                            {{ formattedDate(claim?.date_created) }}
                        </small>
                    </h2>
                </div>

                <div v-if="validation[0]?.classification" :class="getClassification(validation[0]?.classification).boxClass" class="custom-box text-caption pa-4">
                    {{ getClassification(validation[0]?.classification).classification }}
                </div>

            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" md="10">

                <!-- Sources with Horizontal Scrolling -->
                <div>
                    <h4 class="text-h8 mb-2">
                        <v-icon size="small">mdi-text</v-icon>
                        Sources
                    </h4>
                    <div class="d-flex flex-row overflow-auto source-scroller">
                        <v-card v-for="(source, index) in validation[0]?.sources" :key="index" class="pa-4 me-4 mb-4"
                            outlined style="min-width: 250px; max-width: 250px;">
                            <v-row no-gutters>
                                <v-col cols="auto">
                                    <div class="text-caption source-index">{{ index + 1 }}</div>
                                </v-col>
                                <v-col>
                                    <p class="text-subtitle-2">{{ source.title }}</p>
                                    <p class="text-caption text-secondary">{{ source.citation }}</p>
                                </v-col>
                            </v-row>
                        </v-card>
                    </div>
                </div>

                <!-- Claim balloon -->
                <div class="mt-8 claim-balloon">
                    <v-row class="d-flex justify-end">
                        <v-col cols="auto">
                            <v-sheet rounded="xl" class="mx-auto pa-4" color="secondary" :min-width="200"
                                :max-width="450">{{ claim?.content }}</v-sheet>
                        </v-col>
                    </v-row>
                </div>

                <!-- Summary -->
                <div class="mt-8">
                    <v-row>
                        <v-col cols="auto">
                            <div class="logo-container">
                                <v-icon color="black">
                                    mdi-epsilon
                                </v-icon>
                            </div>
                        </v-col>
                        <v-col>
                            <p>{{ validation[0]?.motivation }}</p>
                        </v-col>
                    </v-row>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import apiClient from "@/utils/apiClient";

export default {
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
        };
    },
    methods: {
        async fetchClaimData() {
            try {
                const claimResponse = await apiClient.get(`/claims/${this.id}`);
                this.claim = claimResponse.data;

                const validationResponse = await apiClient.get(`/claims/${this.id}/validations`);
                this.validation = validationResponse.data;
            } catch (error) {
                console.error("Error fetching claim data:", error);
            }
        },
        formattedDate(date) {
            if (!date) return "";
            const now = new Date();
            const givenDate = new Date(date);
            const diffInMilliseconds = now - givenDate;
            const diffInMinutes = Math.floor(diffInMilliseconds / (1000 * 60));
            const diffInHours = Math.floor(diffInMilliseconds / (1000 * 60 * 60));
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
                        classification: "Evidence agrees with the hypothesis",
                    };
                case "B":
                    return {
                        boxClass: "blue-box",
                        classification: "Partially Supported: Some evidence agrees; others are neutral or contradictory.",
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
        this.fetchClaimData();
    },
};
</script>

<style scoped>
.custom-box {
    border-left-width: 8px;
    border-left-style: solid;
    border-radius: 4px;
    display: flex;
    align-items: center;
    font-size: 1rem;
}

/* Green Box */
.green-box {
    background-color: #d7f3e3;
    /* Soft green */
    border-left-color: #1b5e20;
    /* Strong green */
    color: #1b5e20;
}

/* Blue Box */
.blue-box {
    background-color: rgb(var(--v-theme-secondary)) !important;
    border-left-color: #1a4f8a;
    /* Strong blue */
    color: rgb(var(--v-theme-on-secondary)) !important;
}

/* Orange Box */
.orange-box {
    background-color: #fdebd3;
    /* Soft orange */
    border-left-color: #e65100;
    /* Strong orange */
    color: #e65100;
}

/* Red Box */
.red-box {
    background-color: #f9d7d7;
    /* Soft red */
    border-left-color: #b71c1c;
    /* Strong red */
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
</style>