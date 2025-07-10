<template>
  <div class="settings">
    <h2>Settings</h2>
    <form @submit.prevent="updateSettings">
      <div>
        <label for="n_chunks">Number of Chunks (1-10):</label>
        <input
          id="n_chunks"
          type="number"
          min="1"
          max="10"
          v-model.number="settings.n_chunks"
          required
        />
      </div>
      <div>
        <label for="developer">Developer Mode:</label>
        <input
          id="developer"
          type="checkbox"
          v-model="settings.developer"
        />
      </div>
      <button type="submit" :disabled="loading">Update</button>
    </form>
    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script>
export default {
  name: "Settings",
  data() {
    return {
      settings: {
        n_chunks: 5,
        developer: false,
      },
      loading: false,
      message: "",
    };
  },
  methods: {
    async fetchSettings() {
      this.loading = true;
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/settings`);
        if (!response.ok) throw new Error("Failed to fetch settings");
        const data = await response.json();
        this.settings.n_chunks = data.n_chunks;
        this.settings.developer = data.developer;
      } catch (error) {
        this.message = "Error loading settings.";
      } finally {
        this.loading = false;
      }
    },
    async updateSettings() {
      this.loading = true;
      this.message = "";
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/settings`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.settings),
        });
        if (!response.ok) throw new Error("Failed to update settings");
        const data = await response.json();
        this.settings.n_chunks = data.n_chunks;
        this.settings.developer = data.developer;
        this.message = "Settings updated successfully!";
      } catch (error) {
        this.message = "Error updating settings.";
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchSettings();
  },
};
</script>

<style scoped>
.settings {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1.5rem;
  max-width: 400px;
  margin: 2rem auto;
  background: #fafafa;
  color: #000; /* Make all text black */
}
.settings h2 {
  margin-bottom: 1rem;
}
.settings form > div {
  margin-bottom: 1rem;
}
.settings label {
  margin-right: 0.5rem;
  color: #000; /* Ensure label text is black */
}
.settings .message {
  margin-top: 1rem;
  color: #000; /* Make message text black */
}
</style>