<script setup>
import { ref } from 'vue';
import DatePicker from 'primevue/datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Checkbox from 'primevue/checkbox';
import $ from 'jquery';

const date = ref(null);
const jmlFile = ref('');
const courtFile = ref('');
const styleOfCause = ref('');

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

function formSubmit(e){
    const formattedDate = date.value.toISOString().split('T')[0];
    e.preventDefault();
    $.ajax({
        url: 'http://127.0.0.1:8000/add',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            date: formattedDate,
            jmlFileNum: jmlFile.value,
            courtFileNum: courtFile.value,
            styleOfCause: styleOfCause.value,
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

        <h2>JML File No.</h2>
            <input type="text" name="jmlFile" v-model="jmlFile" class="p-1.5 !border-[1px] !border-sweet-pink text-light-pink !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-dark-gray" required />
            
        <h2>Court File No.</h2>
        <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[1px] !border-sweet-pink text-light-pink !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-dark-gray" required />
        
        <h2>Style of Cause</h2>
        <input type="text" name="styleOfCause" v-model="styleOfCause" class="p-1.5 !border-[1px] !border-sweet-pink text-light-pink !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-dark-gray" required />
        
        <h2>Trial Date</h2>
        <DatePicker v-model="date" class="datepicker" name="date" showIcon fluid iconDisplay="input" dateFormat="dd/mm/yy"></DatePicker>
        
        <h2 class="mt-2">Choose which calendar/s</h2>
        <div class="card flex justify-left">
            <div class="flex flex-col gap-2" id="calendarList">
                <div v-for="calendar of calendars" :key="calendar.key" class="flex items-center gap-2">
                    <Checkbox class="calendarCheckbox" v-model="selectedCalendars" :inputId="calendar.key" name="calendar" :value="calendar.name" />
                    <label :for="calendar.key">{{ calendar.name }}</label>
                </div>
            </div> 
        </div>
        
        <button class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="submit">Add item</button>
    </form>
</template>

<style scoped>

.datepicker {
    width: 150px;
    height: 40px;
}

h2 {
    margin-top: 10px;
    color: #fadbe1;
}
</style>