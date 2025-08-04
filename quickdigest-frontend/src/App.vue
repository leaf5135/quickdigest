<template>
  <div class="app">
    <h1>QuickDigest</h1>

    <!-- Topic Selection -->
    <div class="topics">
      <button
        v-for="t in topics"
        :key="t"
        @click="selectTopic(t)"
        :class="{ active: topic === t }"
      >
        {{ t }}
      </button>
    </div>

    <!-- Spacer -->
    <div class="spacer"></div>

    <!-- Loading & Summaries -->
    <div v-if="loading">Loading summaries...</div>

    <div v-else>
      <div v-if="summaries.length === 0">Select a topic to see summaries</div>
      <div v-else class="summaries">
        <div v-for="item in summaries" :key="item.link" class="card">
          <h3><a :href="item.link" target="_blank">{{ item.title }}</a></h3>
          <p v-html="formatSummary(item.summary)"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// Topic list with proper display formatting
const topics = [
  "Business",
  "Entertainment",
  "General",
  "Health",
  "Science",
  "Sports",
  "Technology",
  "Gaming"
];

const topic = ref("");
const summaries = ref([]);
const loading = ref(false);

// Fetch summaries for selected topic
async function selectTopic(t) {
  topic.value = t;
  summaries.value = [];
  loading.value = true;

  try {
    const query = `?topic=${t.toLowerCase()}`;
    const res = await fetch(`/api/summaries${query}`);
    summaries.value = await res.json();
  } catch (err) {
    alert("Failed to fetch summaries");
  } finally {
    loading.value = false;
  }
}

// Format bullet point summaries for better readability
function formatSummary(text) {
  return text
    .replace(/•\s*/g, "• ")     // Normalize bullets
    .split(/• /g)               // Split on bullets
    .filter(Boolean)           // Remove empty entries
    .map(s => `• ${s.trim()}`)  // Add bullet back
    .join('<br><br>');          // Newline after each bullet
}
</script>

<style>
.app {
  max-width: 600px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
}

.topics {
  margin-bottom: 2rem;
}

.topics button {
  margin-right: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.topics button.active {
  font-weight: bold;
  background-color: #007acc;
  color: white;
}

.spacer {
  margin-bottom: 2rem;
}

.card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 4px;
}

.card p {
  white-space: pre-wrap;
  line-height: 1.5;
}
</style>
