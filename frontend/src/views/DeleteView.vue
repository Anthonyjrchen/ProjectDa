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

.addingForm {
  flex: 1; /* Takes up less space */
  padding: 16px;
}

.calendarView {
  flex: 5; /* Takes up more space */
  overflow: auto; /* Makes content scrollable if needed */
  min-width: 1000px;
}

@media (max-width: 1024px) {
  .calendarView {
    flex: 3; /* Reduces space given to calendarView on medium screens */
    max-width: 100px;
  }
}

@media (max-width: 768px) {
  .container {
    flex-direction: column; /* Stacks items vertically on smaller screens */
  }
  
  .addingForm, .calendarView {
    max-width: 100%; /* Each element takes full width */
  }
}

* {
  box-sizing: border-box; /* Ensure padding doesn't affect overall width */
}

</style>