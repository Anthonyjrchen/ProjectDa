<script setup>
import { ref } from 'vue';

let deleteCalendars = ref([]);

$.ajax({
    url:'http://localhost:8000/calendars',
    type:'GET',
    success:function(val) {
        deleteCalendars.value = [];
        for (let i = 0; i < val.length; i++) {
            // add if statement to look for only David, Vanessa, Megaila, and Tyler?
            deleteCalendars.value.push({name:val[i], key:i})
        }
    console.log(val)
    }
})

import $ from 'jquery';
const courtFile = ref('');
function formSubmit(e){
    e.preventDefault();
    console.log("Delete events with caseFileNum: " + courtFile.value)
    $.ajax({
        url: 'http://127.0.0.1:8000/delete',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            caseNum: courtFile.value,
        }),
        success:function(e){
            if("error" in e) {
                alert(e.error)
            } else {
                alert("Events with the courtFileNum: " + courtFile.value + " was deleted.")
            }
        }
    });
};
</script>

<template>
    <head>
        <link href="./output.css" rel="stylesheet">
    </head> 
    <form class="p-1.5" v-on:submit.prevent="formSubmit">
        <h1 class="text-3xl font-bold">Deleting</h1>
        <div class="container">
            <div class="courtFileNumInput">
                <h2>Court File No.</h2>
                <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[1px] !border-dark-white text-light-pink !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-dark-gray" required />
            </div>

            <div class="calendars">
                <h2 class="mt-2">Choose which calendar/s</h2>
                <div class="card flex justify-left">
                    <div class="flex flex-col gap-2" id="calendarList">
                        <div v-for="deleteCalendar of deleteCalendars" :key="deleteCalendar.key" class="flex items-center gap-2">
                            <Checkbox class="calendarCheckbox" :inputId="deleteCalendar.key" name="deleteCalendar" :value="deleteCalendar.name" />
                            <label :for="deleteCalendar.key">{{ deleteCalendar.name }}</label>
                        </div>
                    </div> 
                </div>
            </div>
        </div>

        <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="submit">Delete</button>
    </form>

    <div class="p-0.5">
        <router-link to="/home">
            <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="submit">Go to Add</button>
        </router-link>
    </div>

</template>

<style scoped>

h2 {
    color: #fadbe1;
}

.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

</style>