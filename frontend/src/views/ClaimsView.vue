<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12" md="8" lg="6">
                <!-- Extracted Topics as Chips -->
            <div class="extracted-topics mb-4">
                <v-chip
                    v-for="(topic, index) in claim.extracted_topics"
                    class="me-2 text-caption"
                    rounded
                >
                    {{ topic }}
                </v-chip>
            </div>
                <div>
                    <h2 class="text-h6 mb-4 font-weight-medium">
                        {{ claim.content }}
                        <small class="text-caption text-secondary" style="font-size: 0.75rem;">
                            <v-icon size="small">mdi-clock-outline</v-icon>
                            {{ formattedDate(claim.date_created) }}
                        </small>
                    </h2>
                </div>
                
                <div v-if="validation[0].label" :class="getBoxClass(validation[0].label)" class="custom-box pa-4">
                    {{ validation[0].label }}
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
                        <v-card v-for="(source, index) in validation[0].sources" :key="index" class="pa-4 me-4 mb-4"
                            outlined style="min-width: 250px; max-width: 250px;">
                            <v-row no-gutters align="top">
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
                    <v-row  class="d-flex justify-end">
                        <v-col cols="auto">
                            <v-sheet rounded="xl" class="mx-auto pa-4" color="secondary" :min-width="200" 
                                :max-width="450">{{ claim.content }}</v-sheet>
                        </v-col>
                    </v-row>
                </div>

                <!-- Summary -->
                <div class="mt-8">
                    <v-row dense align="top">
                        <v-col cols="auto">
                            <div class="logo-container">
                                <v-icon color="black">
                                    mdi-epsilon
                                </v-icon>
                            </div>
                        </v-col>
                        <v-col>
                            <p>{{ validation[0].summary }}</p>
                            <ul class="ml-4">
                                <li class="my-2" v-for="(thought, index) in validation[0].chain_of_thought" :key="index">
                                    {{ thought }}
                                </li>
                            </ul>
                        </v-col>
                    </v-row>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    props: {
        id: {
            type: String,
            required: false,
        },
    },

    data() {
        return {
            claim: {
                id: "H01JH8DDDAGV9793JW56BCZ198G",
                content: "Smoking bans in public places lead to a reduction in smoking rates.",
                user_id: "U01JG8NBAGDXPDPMPJV86F2H0WJ",
                status: "Completed",
                extracted_topics: ["Public Health", "Smoking", "Legislation"],
                extracted_terms: ["Smoking bans", "public places", "reduction in smoking rates"],
                extracted_entities: [],
                query_type: "research-based",
                date_created: "2025-01-10T15:30:35",
                date_updated: "2025-01-10T15:31:12",
            },
            validation: [
                {
                    id: "V01JH8DEGNT7H4GR0XQF83WQZVR",
                    hypothesis_id: "H01JH8DDDAGV9793JW56BCZ198G",
                    label: "This hypothesis is partially supported.",
                    summary:
                        "Research provides mixed evidence on the impact of smoking bans in public places on smoking rates. Some studies suggest that such bans can influence social norms and reduce smoking behavior, and have a significant effect on workers' perceived health and exposure to smoke. However, other studies report high levels of non-compliance among smokers, and limited impact on certain smoking-related hospitalizations. The effectiveness of smoking bans also appears to depend on public support and social acceptance.",
                    motivation:
                        "The user's hypothesis is partially supported because while some studies suggest that smoking bans can reduce smoking behavior and exposure to smoke, others report high levels of non-compliance and limited impact on smoking-related hospitalizations. The effectiveness of smoking bans also appears to depend on factors such as public support and social acceptance.",
                    chain_of_thought: [
                        "Anderson et al. (2015) found that smoking bans in public places can influence social norms and reduce smoking behavior.",
                        "Eiser et al. (2009) reported that a majority of smokers did not comply with existing smoking restrictions, suggesting that bans alone may not be sufficient to reduce smoking rates.",
                        "Ho et al. (2016) found that smoking bans were not associated with reductions in certain smoking-related hospitalizations, suggesting that the impact of bans on smoking rates may be limited.",
                        "Lucifora and Origo (n.d., 2010) found that comprehensive smoking bans had a significant effect on workers' perceived health and exposure to smoke, but also noted some unintended effects such as mental distress.",
                        "Connolly (2012) and Harris et al. (2012) suggested that public support is crucial for the effectiveness of smoking bans.",
                        "de Vries et al. (2017) found that social acceptance of smoking restrictions increased over time, even in a country where smoking restrictions have been implemented and reversed several times.",
                    ],
                    sources: [
                        {
                            title:
                                "Legislative Smoking Bans for Reducing Exposure to Secondhand Smoke and Smoking Prevalence: Opportunities for Georgians",
                            citation: "Anderson, J., Coughlin, S. S., Smith, S. A. (2015)",
                        },
                        {
                            title: "Predicting smokers' non-compliance with smoking restrictions in public places",
                            citation: "Eiser, J., Lazuras, L., Rodafinos, A. (2009)",
                        },
                        {
                            title:
                                "A Nationwide Assessment of the Association of Smoking Bans and Cigarette Taxes With Hospitalizations for Acute Myocardial Infarction, Heart Failure, and Pneumonia",
                            citation:
                                "Ho, V., Krumholz, H. M., Ku-Goto, M., Mandawat, A., Ross, J. S., Short, M., Steiner, C. A. (2016)",
                        },
                        {
                            title: "The Effect of Comprehensive Smoking Bans in European Workplaces",
                            citation: "Lucifora, C., Origo, F. (n.d., 2010)",
                        },
                        {
                            title: "How Society Treats Smoking",
                            citation: "Connolly, G. N. (2012)",
                        },
                        {
                            title: "Outdoor Smoke-Free Policies in Maine",
                            citation: "Harris, D. E., Mayberry, S., Roy, S. (2012)",
                        },
                        {
                            title:
                                "Social Acceptance of Smoking Restrictions During 10 Years of Policy Implementation, Reversal, and Reenactment in the Netherlands: Findings From a National Population Survey",
                            citation:
                                "de Vries, H., Hummel, K., Monshouwer, K., Nagelhout, G. E., Willemsen, M. C. (2017)",
                        },
                    ],
                    date_created: "2025-01-10T15:31:12",
                    date_updated: null,
                },
            ],
        };
    },
    methods: {
        formattedDate(date) {
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
                return givenDate.toLocaleDateString(); // Formats as "MM/DD/YYYY" or equivalent in the user's locale
            }
        },
        getBoxClass(label) {
            console.log(label);
            switch (label) {
                case "supported":
                    return "green-box";
                case "This hypothesis is partially supported.":
                    return "blue-box";
                case "conflicting":
                    return "orange-box";
                case "unsupported":
                    return "red-box";
                default:
                    return "";
            }
        },
    },
    filters: {
        capitalize(value) {
            if (!value) return "";
            return value.charAt(0).toUpperCase() + value.slice(1);
        },
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