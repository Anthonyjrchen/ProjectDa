<script setup>
import { ref } from 'vue';
import DatePicker from 'primevue/datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Checkbox from 'primevue/checkbox';
import $ from 'jquery';
const date = ref(null);
const eventName = ref('');

let calendars = ref([]);

const selectedCalendars = ref([]);

$.ajax({
    url:'http://localhost:8000/calendars',
    type:'GET',
    success:function(val) {
        calendars.value = [];
        for (let i = 0; i < val.length; i++) {
            calendars.value.push({name:val[i], key:i})
        }
    console.log(val)
    }
})

// document.getElementById("eventForm").addEventListener("submit", formSubmit(e));

function formSubmit(e){
    // console.log(date.value.toLocaleDateString())
    const formattedDate = date.value.toISOString().split('T')[0];
    e.preventDefault();
    console.log("Event Date is " + formattedDate);
    $.ajax({
        url: 'http://127.0.0.1:8000/add',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            date: formattedDate,
            eventName: eventName.value,
            calendars: selectedCalendars.value,
        }),
        success:function(e){
            if("error" in e) {
                alert(e.error)
            } else {
                alert("Event added successfully to the following calendars: " + e.validCalendars)
            }
        }
    });
};
</script>

<template>
    <head>
        <link href="./output.css" rel="stylesheet">
    </head>
    <form id="eventForm" v-on:submit.prevent="formSubmit">
        <h1 class="text-3xl font-bold">Adding</h1>

        <h2 class="mt-2">Date of event</h2>
        <DatePicker v-model="date" class="datepicker" name="date" showIcon fluid iconDisplay="input" dateFormat="dd/mm/yy"></DatePicker>
        
        <h2 class="mt-2">Name of event</h2>
        <input type="text" name="eventName" v-model="eventName" class="p-1.5 !border-[1px] !border-dark-white text-white !rounded-md focus:outline-none focus:ring-1 focus:ring-white" required />
        
        <h2 class="mt-2">Choose which calendar/s</h2>
        <div class="card flex justify-left">
            <div class="flex flex-col gap-2" id="calendarList">
                <div v-for="calendar of calendars" :key="calendar.key" class="flex items-center gap-2">
                    <Checkbox class="calendarCheckbox" v-model="selectedCalendars" :inputId="calendar.key" name="calendar" :value="calendar.name" />
                    <label :for="calendar.key">{{ calendar.name }}</label>
                </div>
            </div> 
        </div>
        <div>{{ selectedCategories }}</div>
        <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-dark-white mt-5" type="submit">Add item</button>
    </form>
</template>

<style scoped>

button {
    font-family: inherit;
}

.datepicker {
    width: 150px;
    height: 40px;
}

</style>