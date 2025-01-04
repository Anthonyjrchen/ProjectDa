<script setup>
import { ref, provide  } from 'vue';
import AddingForm from '../components/AddingForm.vue';
import CalendarView from '@/components/CalendarView.vue';
const date=ref('Your Mom');
function receiveEmit(e) {
  date.value = e.toISOString().split('T')[0];
  console.log("Received emit: " + e.toISOString().split('T')[0]);
}
provide('selectedDate', date);
</script>

<template>
  <main>
    <div class="container">
      <div class="addingForm">
        <AddingForm @dateChanged="receiveEmit"/>
      </div>

  
    

      <div class="calendarView">
        <CalendarView :selectedDate="date"/>
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
  margin: 20px;
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