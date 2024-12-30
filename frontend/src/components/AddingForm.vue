<script setup>
import { ref } from 'vue';
import DatePicker from 'primevue/datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Checkbox from 'primevue/checkbox';
import $ from 'jquery';
const date = ref(null);
const eventName = ref('');

let categories = ref([]);

const selectedCategories = ref([]);

$.ajax({
    url:'http://localhost:8000/calendars',
    type:'GET',
    success:function(val) {
        // categories=ref([
        //     {name:val[0], key:"A"},
        //     {name:val[1], key:"B"},
        //     {name:val[2], key:"C"},
        // ])
        categories.value = [];
        for (let i = 0; i < val.length; i++) {
            categories.value.push({name:val[i], key:i})
        }
    console.log(val)
    }
})

// document.getElementById("eventForm").addEventListener("submit", formSubmit(e));

function formSubmit(e){
    // console.log(date.value.toLocaleDateString())
    const formattedDate = date.value.toISOString().split('T')[0];
    e.preventDefault();
    $.ajax({
        url: 'http://127.0.0.1:8000/add',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            date: formattedDate,
            eventName: eventName.value,
            categories: selectedCategories.value,
        }),
        success:function(e){
            console.log(e)
        }
    });
};
</script>

<template>
    <form id="eventForm" v-on:submit.prevent="formSubmit">
        <h1>Adding</h1>
        <h2>Date of event</h2>
        <DatePicker v-model="date" class="datepicker" name="date" showIcon fluid iconDisplay="input" dateFormat="dd/mm/yy"></DatePicker>
        <h2>Name of event</h2>
        <input type="text" name="eventName" v-model="eventName" required />
        <h2>Choose which calendar/s</h2>
        <div class="card flex justify-center">
            <div class="flex flex-col gap-4" id="calendarList">
                <div v-for="category of categories" :key="category.key" class="flex items-center gap-2">
                    <Checkbox class="calendarCheckbox" v-model="selectedCategories" :inputId="category.key" name="category" :value="category.name" />
                    <label :for="category.key">{{ category.name }}</label>
                </div>
            </div> 
        </div>
        <div>{{ selectedCategories }}</div>
        <button class="submit" type="submit">Add item</button>
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

.submit {
    margin-top: 10px;
}
</style>