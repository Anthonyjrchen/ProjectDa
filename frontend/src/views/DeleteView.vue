<script setup>

import DeletingForm from '@/components/DeletingForm.vue';

</script>

<template>
  <main>
    <div class="container">
      <div class="deletingForm">
        <DeletingForm />
      </div>

    </div>
  </main>
</template>

<style scoped>

.container {
  display: flex; /* Flexbox for side-by-side layout */
  gap: 16px; /* Add spacing between the divs */
  box-sizing: border-box; /* Ensures padding is included in width calculations */
}

* {
  box-sizing: border-box; /* Ensure padding doesn't affect overall width */
}

</style>