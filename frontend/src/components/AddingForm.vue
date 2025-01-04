<script setup>
import { ref } from 'vue';
import DatePicker from 'primevue/datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Checkbox from 'primevue/checkbox';
import $, { event } from 'jquery';

const date = ref(null);
const jmlFile = ref('');
const courtFile = ref('');
const styleOfCause = ref('');
const addProgress = ref(0);
const addTotal = ref(0);
const progressPercentage = ref(0);
let calendars = ref([{"name":"Backend Not Running Yet.", key:"test"}]);

const selectedCalendars = ref([]);
let lawyerCalendars = [];
$.ajax({
    url:'http://localhost:8000/calendars',
    type:'GET',
    success:function(val) {
        calendars.value = [];
        for (let i = 0; i < val.calendarList.length; i++) {
            calendars.value.push({name:val.calendarList[i], key:i})
        }
        console.log(val)
    }
})

function formSubmit(e){
    const formattedDate = date.value.toISOString().split('T')[0];
    e.preventDefault();
    addProgress.value=0;
    addTotal.value = 0;
    progressPercentage.value = 0;
    $.ajax({
        url:'http://127.0.0.1:8000/lawyerCalendars/update',
        type:'get',
        async:false,
        success:function(e){
            lawyerCalendars = e
            console.log("Updated lawyer calendars...")
        }
    })
    $.ajax({
       url: 'http://127.0.0.1:8000/initiateAdd',
       type: 'post',
       contentType: 'application/json',
       data: JSON.stringify({
           date: formattedDate,
           calendars: selectedCalendars.value,
       }),
      success:function(e){
            // return {
            // "splitDate":splitDate,
            // "eventDict":eventDict,
            // "validCalendars":validCalendars,
            // }  this is /initiateAdd 's return value.
            
            // for calendar in validCalendars:
            //  for eventKey in eventDictKeys:
            //      eventDates = eventDict[eventKey]
            //      addEvent(calendarDict[calendar],userEvent.courtFileNum, userEvent.jmlFileNum, userEvent.styleOfCause,eventDates.pop(0), eventKey) #add due dates (lawyers and paralegal and self) (targetFolder, courtFileNum, jmlFileNum, styleOfCause, eventDate, formName) is the format for calling addEvent
            //      for reminderDay in eventDates:
            //          addEventReminder(calendarDict[calendar],userEvent.courtFileNum, userEvent.jmlFileNum, userEvent.styleOfCause,reminderDay, eventKey) #add due dates and reminders (paralegal and self)        
            addTotal.value += 64*e.validCalendars.length;
            const eventDictKeys = Object.keys(e.eventDict);
            console.log(e.eventDict);
            for (let j = 0; j < e.validCalendars.length; j++) {
                for (let i = 0; i < eventDictKeys.length; i++) {
                    
                    var eventDates = e.eventDict[eventDictKeys[i]];
                    let plaintiffDefendant = eventDictKeys[i].substring(eventDictKeys[i].length - 3)=="(P)" || eventDictKeys[i].substring(eventDictKeys[i].length - 3)=="(D)"
                    let formName = eventDictKeys[i];
                    if (plaintiffDefendant) {
                        formName  = eventDictKeys[i].substring(0,eventDictKeys[i].length-3)
                    }
                    $.ajax({
                        url: 'http://127.0.0.1:8000/add',
                        type: 'post',
                        contentType: 'application/json',
                        data: JSON.stringify({
                            targetFolder: e.validCalendars[j],
                            courtFileNum: courtFile.value,
                            jmlFileNum: jmlFile.value,
                            styleOfCause: styleOfCause.value,
                            eventDate:eventDates[0],
                            formName:formName,
                            plaintiffDefendant:plaintiffDefendant,
                        }),
                        success(e){
                            addProgress.value++;
                            progressPercentage.value = Math.round(addProgress.value/addTotal.value*100)
                        }
                    })
                    if(!lawyerCalendars.includes(e.validCalendars[j])){
                        console.log(e.validCalendars[j] + " is a lawyer.")
                        for (let x = 1; x < eventDates.length; x++) {
                            $.ajax({
                                url: 'http://127.0.0.1:8000/add/reminder',
                                type: 'post',
                                contentType: 'application/json',
                                data: JSON.stringify({
                                    targetFolder: e.validCalendars[j],
                                    courtFileNum: courtFile.value,
                                    jmlFileNum: jmlFile.value,
                                    styleOfCause: styleOfCause.value,
                                    eventDate: eventDates[x],
                                    formName:formName,
                                    plaintiffDefendant:plaintiffDefendant,
                                }),
                                success(e){
                                    addProgress.value++;
                                    progressPercentage.value = Math.round(addProgress.value/addTotal.value*100)
                                }
                            })
                        }
                    }
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
    <form id="eventForm" v-on:submit.prevent="formSubmit">
        <h1 class="text-3xl font-bold">Adding</h1>

        <h2>JML File No.</h2>
            <input type="text" name="jmlFile" v-model="jmlFile" class="p-1.5 !border-[2px] !border-brink-pink text-dark-gray !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-rose-bud" required />
            
        <h2>Court File No.</h2>
        <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[2px] !border-brink-pink text-dark-gray !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-rose-bud" required />
        
        <h2>Style of Cause</h2>
        <input type="text" name="styleOfCause" v-model="styleOfCause" class="p-1.5 !border-[2px] !border-brink-pink text-dark-gray !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-rose-bud" required />
        
        <h2>Trial Date</h2>
        <!-- !!! figure out how to edit styles (primevue specific editing?) -->
        <DatePicker v-model="date" class="datepicker" name="date" fluid iconDisplay="input" dateFormat="dd/mm/yy" input-class="!border-[2px] !border-brink-pink !bg-rose-bud !text-dark-gray" calendar-class="rounded" @update:model-value="(value) => $emit('dateChanged', value)"></DatePicker>

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
        <div class="mt-2">Progress: {{ addProgress }}/{{ addTotal }}</div>
        <ProgressBar :value="progressPercentage" :class="'custom-progress-bar'"></ProgressBar>
    </form>
</template>

<style scoped>

h2 {
    margin-top: 10px;
    color: #fadbe1;
}

.p-datepicker {
    width: 187px;
    height: 40px;
}


.custom-progress-bar {
    background-color: #272526 !important;
    width: 186px;
    border: 2px solid #fb607f !important;
    padding: 10px;
}



</style>