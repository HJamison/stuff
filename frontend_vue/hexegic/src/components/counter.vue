<template>
    <div>
        <p>API Calls Left: {{ counter }}</p>
    </div>
</template>

<script>
export default {
    name: "Counter",
    data() {
        return {
            counter: 0,
            intervalId: null,
        };
    },
    methods: {
        async fetchCounter() {
            try {
                const response = await fetch(`${import.meta.env.VITE_API_URL}/health/n_api_calls_left`);
                const data = await response.json();
                this.counter = data.calls_left;
            } catch (error) {
                console.error('Failed to fetch counter:', error);
            }
        },
    },
    mounted() {
        this.fetchCounter();
        this.intervalId = setInterval(this.fetchCounter, 100000); // Poll every 10 seconds
    },
    beforeUnmount() {
        clearInterval(this.intervalId);
    },
};
</script>