<script setup>
import { ref, watch } from 'vue';
import DatePicker from 'primevue/datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Checkbox from 'primevue/checkbox';
import $ from 'jquery';

const addLoading = ref(false);
const date = ref(null);
const jmlFile = ref('');
const courtFile = ref('');
const styleOfCause = ref('');
const addProgress = ref(0);
const addTotal = ref(0);
const progressPercentage = ref(0);
let calendars = ref([{"name":"Backend Not Running Yet.", key:"test"}]);
let watchEnder;
const selectedCalendars = ref(["Calendar(jneria@jml.ca)"]);
let lawyerCalendars = [];

function loadCalendars() {
    $.ajax({
        url:'http://localhost:8000/',
        type:'GET',
        success:function() {
            calendars.value = [{"name":"Retrieving calendars...", key:"test"}]
        }
    })
    
    $.ajax({
        url:'http://localhost:8000/calendars',
        type:'GET',
        success:function(val) {
            calendars.value = [];
            for (let i = 0; i < val.calendarList.length; i++) {
                calendars.value.push({name:val.calendarList[i], key:i})
            }
            
            console.log("Adding form's calendars's value is: " + calendars.value);
        }
    })
}
loadCalendars();

function addEvent(msg) {
    $.ajax({
        url:'http://localhost:8000/log',
        type:'post',
        contentType: 'application/json',
        data: JSON.stringify({
            isDeleteEvent: false,
            message: msg
        }),
        success:function() {
            // getLogs()   this CAN send emit to log page to reload logs (optional)
        }
    });
}

function formSubmit(e){
    var start = new Date().getTime();
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
    // $.ajax({
    //     url:"http://127.0.0.1:8000/calendars/init",
    //     type:"get",
    //     async:false,
    //     succes:function(e) {
            $.ajax({
                url: 'http://127.0.0.1:8000/initiateAdd',
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify({
                    date: formattedDate,
                    calendars: selectedCalendars.value,
                }),
                success:function(e){
                        console.log("Response from /initiateAdd:", e);
                        if (!e.validCalendars) {
                            console.error("validCalendars is undefined.");
                        }
                        addLoading.value = true;
                        watchEnder = watch(progressPercentage, (newVal, oldVal) => {
                            if(addProgress.value==addTotal.value) {
                                console.log("Adding function complete")
                                addLoading.value = false;
                                watchEnder();
                                let funcDuration = ((new Date().getTime()- start) / 1000).toFixed(1);
                                console.log("Add function took: " + funcDuration);
                                addEvent("Adding courtFileNum: " + courtFile.value+"(" + formattedDate + ") to " + e.validCalendars + " took " + funcDuration + " seconds");
                            }
                        },);
                        e.validCalendars.forEach(function (e){
                            if(lawyerCalendars.includes(e)){
                                addTotal.value+=14
                            } else {
                                addTotal.value+=64
                            }
                        })
                        const eventDictKeys = Object.keys(e.eventDict);
                        console.log(e.eventDict);
                        for (let j = 0; j < e.validCalendars.length; j++) {
                            addEvent("Added due dates (and reminder dates) for " + styleOfCause.value + " [courtFileNum: " + courtFile.value + "(" + formattedDate + ")] for the calendar: " + e.validCalendars[j])
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
                                    console.log(e.validCalendars[j] + " is not a lawyer.")
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
                                } else {
                                    console.log(e.validCalendars[j] + " is a lawyer.")
                                }
                            } 
                        }
                    }
                });
    //     }
    // });
    
};

function startAdd() {
    $.ajax({
       url: 'http://127.0.0.1:8000/initiateAdd',
       type: 'post',
       contentType: 'application/json',
       data: JSON.stringify({
           date: formattedDate,
           calendars: selectedCalendars.value,
       }),
      success:function(e){
            console.log("Response from /initiateAdd:", e);
            if (!e.validCalendars) {
                console.error("validCalendars is undefined.");
            }
            addLoading.value = true;
            watchEnder = watch(progressPercentage, (newVal, oldVal) => {
                if(addProgress.value==addTotal.value) {
                    console.log("Adding function complete")
                    addLoading.value = false;
                    watchEnder();
                    let funcDuration = ((new Date().getTime()- start) / 1000).toFixed(1);
                    console.log("Add function took: " + funcDuration);
                    addEvent("Adding courtFileNum: " + courtFile.value+"(" + formattedDate + ") to " + e.validCalendars + " took " + funcDuration + " seconds");
                }
            },);
            e.validCalendars.forEach(function (e){
                if(lawyerCalendars.includes(e)){
                    addTotal.value+=14
                } else {
                    addTotal.value+=64
                }
            })
            const eventDictKeys = Object.keys(e.eventDict);
            console.log(e.eventDict);
            for (let j = 0; j < e.validCalendars.length; j++) {
                addEvent("Added due dates (and reminder dates) for " + styleOfCause.value + " [courtFileNum: " + courtFile.value + "(" + formattedDate + ")] for the calendar: " + e.validCalendars[j])
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
                        console.log(e.validCalendars[j] + " is not a lawyer.")
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
                    } else {
                        console.log(e.validCalendars[j] + " is a lawyer.")
                    }
                } 
            }
        }
    });
}
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
        
        <button :disabled="addLoading" class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea mt-3 disabled:bg-azalea disabled:cursor-not-allowed" type="submit">Add item</button>
        <div class="mt-2">Progress: {{ addProgress }}/{{ addTotal }}</div>
        <ProgressBar :value="progressPercentage" :class="'custom-progress-bar'"></ProgressBar> <!--progressPercentage-->
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

.p-progressbar {
    border: 2px solid #fb607f !important;
    background-color: #272526 !important;
    width: 186px;
    height: 25px;
}

.p-progressbar-value {
    background-color: #fb607f !important;
    width: 186px;
    transition: width 0.005s ease; /* Smooth transition */
}




</style>