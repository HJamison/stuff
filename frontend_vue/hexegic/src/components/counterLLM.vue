<template>
    <div>
        <p>LLM Calls Left: {{ counterLLM }}</p>
    </div>
</template>

<script> // i want to fetch the number of LLM calls left from the backend and display it in this component
export default {
    name: "counterLLM",
    data() {
        return {
            counterLLM: 0,
            intervalId: null,
        };
    },
    methods: {
        async fetchcounterLLM() {
            try {
                const response = await fetch(`${import.meta.env.VITE_API_URL}/health/n_llm_calls_left`);
                const data = await response.json();
                this.counterLLM = data.calls_left;
            } catch (error) {
                console.error('Failed to fetch counterLLM:', error);
            }
        },
    },
    mounted() {
        this.fetchcounterLLM();
        this.intervalId = setInterval(this.fetchcounterLLM, 10000); // Poll every 10 seconds
    },
    beforeUnmount() {
        clearInterval(this.intervalId);
    },
};
</script>