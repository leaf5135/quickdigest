<template>
  <div class="app">
    <h1>QuickDigest</h1>

    <div class="topics">
      <button
        v-for="t in topics"
        :key="t"
        @click="selectTopic(t)"
        :class="{active: topic === t}"
      >
        {{ t }}
      </button>
    </div>

    <div v-if="loading">Loading summaries...</div>

    <div v-else>
      <div v-if="summaries.length === 0">Select a topic to see summaries</div>
      <div v-else class="summaries">
        <div v-for="item in summaries" :key="item.link" class="card">
          <h3><a :href="item.link" target="_blank">{{ item.title }}</a></h3>
          <p>{{ item.summary }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const topics = [
  "All",           // Represents default/no specific topic
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

async function selectTopic(t) {
  topic.value = t;
  summaries.value = [];
  loading.value = true;

  try {
    const query = t === "All" ? "" : `?topic=${t.toLowerCase()}`;
    const res = await fetch(`/api/summaries${query}`);
    summaries.value = await res.json();
  } catch (err) {
    alert("Failed to fetch summaries");
  } finally {
    loading.value = false;
  }
}
</script>

<style>
.app {
  max-width: 600px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
}
.topics button {
  margin-right: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.topics button.active {
  font-weight: bold;
  background-color: #007acc;
  color: white;
}
.card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}
</style>
