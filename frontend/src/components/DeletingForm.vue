<script setup>
import { ref } from 'vue';
import $ from 'jquery';
import Checkbox from 'primevue/checkbox';
let deleteCalendars = ref([]);
let selectedDeleteCalendars = ref([]);
const allowedCalendars = ["Calendar(David Volk)","Calendar(Megaila Rose)","Calendar(Vanessa S. Werden)","Tyler Galbraith","Test 1(eventhandlertest2@outlook.com)","Test 2(eventhandlertest2@outlook.com)","Calendar(eventhandlertest2@outlook.com)"] //Add names here that you want to be able to delete from.
$.ajax({
    url:'http://localhost:8000/calendars',
    type:'GET',
    success:function(val) {
        deleteCalendars.value = [];
        for (let i = 0; i < val.length; i++) {
            // add if statement to look for only David, Vanessa, Megaila, and Tyler?
            if (allowedCalendars.includes(val[i])){
                deleteCalendars.value.push({name:val[i], key:i})
            }
        }
    console.log(deleteCalendars.value)
    }
})


const courtFile = ref('');
const deleteProgress = ref(0);
const deleteTotal = ref(0);
function formSubmit(e){
    deleteProgress.value = 0;
    deleteTotal.value = 0;
    e.preventDefault();
    console.log("Delete events with caseFileNum: " + courtFile.value)
    $.ajax({
        url: 'http://127.0.0.1:8000/initDelete',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            caseNum: courtFile.value,
            calendars: selectedDeleteCalendars.value,
        }),
        success:function(e){
            let deleteDictKeys = Object.keys(e.deleteDict) //deleteDict = {"calendar_name":128,"calendar2_name":64}
            for (let i = 0; i < deleteDictKeys.length; i++){
                deleteTotal.value+=e.deleteDict[deleteDictKeys[i]].length;
            }

            for (let i = 0; i < deleteDictKeys.length; i++){
                for (var j = e.deleteDict[deleteDictKeys[i]].length-1; j >= 0 ; j--){
                    $.ajax({
                        url: 'http://127.0.0.1:8000/delete',
                        type: 'post',
                        contentType: 'application/json',
                        data: JSON.stringify({
                            calendar: deleteDictKeys[i],
                            curItem: e.deleteDict[deleteDictKeys[i]][j].toString(),
                        }),
                        success:function(e){
                            deleteProgress.value+=1
                            
                        }
                    });
                }
            }
        }
    });
};
</script>

<template>
    <head>
        <link href="./output.css" rel="stylesheet">
    </head> 
    <form v-on:submit.prevent="formSubmit">
        <h1 class="text-3xl font-bold">Deleting</h1>
        <div class="container">
            <div class="courtFileNumInput">
                <h2>Court File No.</h2>
                <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[1px] !border-brink-pink text-dark-gray !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-rose-bud" required />
            </div>

            <div class="calendars">
                <h2 class="mt-2">Choose which calendar/s</h2>
                <div class="card flex justify-left">
                    <div class="flex flex-col gap-2" id="calendarList">
                        <div v-for="deleteCalendar of deleteCalendars" :key="deleteCalendar.key" class="flex items-center gap-2">
                            <Checkbox class="deleteCalendarCheckbox" v-model="selectedDeleteCalendars" :inputId="deleteCalendar.key" name="deleteCalendar" :value="deleteCalendar.name" />
                            <label :for="deleteCalendar.key">{{ deleteCalendar.name }}</label>
                        </div>
                    </div> 
                </div>
            </div>
        </div>

        <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="submit">Delete</button>
        <div>{{ deleteProgress }}/{{ deleteTotal }}</div>
    </form>

    <div class="p-0.5">
        <router-link to="/">
            <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="submit">Go to Add</button>
        </router-link>
    </div>

</template>

<style scoped>

h2 {
    margin-top: 10px;
    color: #fadbe1;
}

.container {
  display: flex;
  box-sizing: border-box;
  gap: 16px;
}

</style>