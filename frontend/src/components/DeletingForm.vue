<script setup>
import { ref, watch } from 'vue';
import $ from 'jquery';
import Checkbox from 'primevue/checkbox';
import Popover from 'primevue/popover';

let deleteCalendars = ref([{"name":"Backend Not Running Yet.", key:"test"}]);
let deleteCalendarsRemaining = ref([]);
let selectedDeleteCalendars = ref(["Calendar(jneria@jml.ca)"]); //Need to have Jana selected by default
const lawyerCalendars = ref([]);
const loading = ref(false);
const deleteLoading = ref(false);
$.ajax({
    url:'http://127.0.0.1:8000/lawyerCalendars/update',
    type:'get',
    async:false,
    success:function(e){
        lawyerCalendars.value = e
        console.log("Updated lawyer calendars...")
    }
})

function loadCalendars() {
    $.ajax({
        url:'http://localhost:8000/',
        type:'GET',
        success:function() {
            deleteCalendars.value = [{"name":"Retrieving calendars...", key:"test"}]
        }
    })
    
    $.ajax({
        url:'http://localhost:8000/calendars',
        type:'GET',
        success:function(val) {
            deleteCalendars.value = [];
            for (let i = 0; i < val.calendarList.length; i++) {
                if (lawyerCalendars.value.includes(val.calendarList[i])){
                    deleteCalendars.value.push({name:val.calendarList[i], key:i+1})
                } else {
                    if(val.calendarList[i]!="Calendar(jneria@jml.ca)"){
                        deleteCalendarsRemaining.value.push({name:val.calendarList[i], key:i+1})
                    }
                }
                // if (val[i]==) if val[i](calendarname) == Jana's calendar, add to selectedDeleteCalendars and check her checkbox.
            }
        console.log(deleteCalendars.value)
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
            isDeleteEvent: true,
            message: msg
        }),
        success:function() {
            // getLogs()   this CAN send emit to log page to reload logs (optional)
        }
    });
}

const courtFile = ref('');
const deleteProgress = ref(0);
const deleteTotal = ref(0);
const progressPercentage = ref(0);
let watchEnder;
const displayDeleteDict = ref([]);
function formSubmit(e){
    var start = new Date().getTime();
    deleteProgress.value = 0;
    deleteTotal.value = 0;
    progressPercentage.value = 0;
    e.preventDefault();
    console.log("Delete events with caseFileNum: " + courtFile.value)
    loading.value = true;
    // $.ajax({
    //     url:"http://127.0.0.1:8000/calendars/init",
    //     type:"get",
    //     succes:function(e) {
            $.ajax({
                url: 'http://127.0.0.1:8000/initDelete',
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify({
                    caseNum: courtFile.value,
                    calendars: selectedDeleteCalendars.value,
                }),
                success:function(e){
                    loading.value = false;
                    let deleteDictKeys = Object.keys(e.deleteDict) //deleteDict = {"calendar_name":[item1.entryID,item2.entryID,item3.entryID],"calendar2_name":[item1.entryID,item2.entryID]} the number represents how many items to delete.
                    deleteLoading.value=true;
                        watchEnder = watch(progressPercentage, (newVal, oldVal) => {
                    if(deleteProgress.value==deleteTotal.value) {
                        console.log("Delete function complete")
                        deleteLoading.value = false;
                        watchEnder();
                        let funcDuration = ((new Date().getTime()- start) / 1000).toFixed(1);
                        console.log("Delete function took: " + funcDuration);
                        addEvent("Deleting (" + courtFile.value + ") events from " + e.validCalendars + " took " + funcDuration + " seconds");
                    }
                },);
                    for (let i = 0; i < deleteDictKeys.length; i++){
                        deleteTotal.value+=e.deleteDict[deleteDictKeys[i]].length;
                        displayDeleteDict.value.push({"name":deleteDictKeys[i],"value":e.deleteDict[deleteDictKeys[i]].length,"key":i})
                        // display how many events found for each calendar here. (maybe update text file and reflect it on web app)
                        addEvent("Found " + e.deleteDict[deleteDictKeys[i]].length.toString() + " in " + deleteDictKeys[i]);        
                    }
                    if (deleteTotal.value==0) deleteLoading.value=false;
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
                                    progressPercentage.value = Math.round(deleteProgress.value/deleteTotal.value*100)
                                }
                            });
                        }
                    }
                    addEvent("Removed events with courtFileNum: " + courtFile.value + " for the calendars: " + deleteDictKeys);
                },
                error:function(e) {
                    alert("Received error: " + e + " please try again.");
                }
            });
    //     }
    // });
};

function startDelete() {
    
}

const op = ref();
const toggle = (event) => {
    op.value.toggle(event);
}
</script>

<template>
    <head>
        <link href="./output.css" rel="stylesheet">
    </head> 
    <form v-on:submit.prevent="formSubmit">
        <h1 class="text-3xl font-bold">Deleting</h1>
        <div class="container">
            <div class="subContainer">
                <div class="courtFileNumInput">
                    <h2>Court File No.</h2>
                    <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[2px] !border-brink-pink text-dark-gray !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-rose-bud" required />
                </div>
                <div class="mt-3">
                    <button :disabled="deleteLoading" class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea disabled:bg-azalea disabled:cursor-not-allowed" type="submit">Delete</button>
                    <Transition>
                        <div class="mt-2" v-if="!loading">Progress: {{ deleteProgress }}/{{ deleteTotal }}</div>
                    </Transition>

                    <Transition>
                        <div v-if="!loading"><ProgressBar :value="progressPercentage" :class="'custom-progress-bar'"></ProgressBar></div>
                    </Transition>
                    
                    <Transition>
                        <div class="mt-3" v-if="loading">Progress: <i class="pi pi-spin pi-spinner"></i></div>
                    </Transition>
                    

                    <!-- display for how many events are being deleted from whom -->
                    <h2>Deleting:</h2>
                    <Transition v-if="!deleteLoading">
                        <p>{ number } from { calendar }...</p>
                    </Transition>
                    <Transition v-if="deleteLoading">
                        <div>
                            <div v-for="entry of displayDeleteDict" :key="entry.key" class="flex items-center gap-2">
                                <p :for="entry.key">{ {{ entry.value }} } from { {{ entry.name }} }</p>
                            </div>
                        </div>
                    </Transition>
                </div>
            </div>

            <div class="calendars">
                <h2 class="mt-2">Choose which calendar(s)</h2>
                <div class="card flex justify-left">
                    <div class="flex flex-col gap-2" id="calendarList">
                        <div :key="0" class="flex items-center gap-2">
                            <Checkbox  class="deleteCalendarCheckbox" v-model="selectedDeleteCalendars" :inputId="0" name="deleteCalendar" :value="'Calendar(jneria@jml.ca)'" />
                            <label :for="0">Calendar(jneria@jml.ca)</label> <!-- Jana's checkbox (starts off as checked) -->
                        </div>
                        <div v-for="deleteCalendar of deleteCalendars" :key="deleteCalendar.key" class="flex items-center gap-2">
                            <Checkbox class="deleteCalendarCheckbox" v-model="selectedDeleteCalendars" :inputId="deleteCalendar.key" name="deleteCalendar" :value="deleteCalendar.name" />
                            <label :for="deleteCalendar.key">{{ deleteCalendar.name }}</label>
                        </div>
                    </div>
                </div>
                
                <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="button" v-on:click="toggle" style="display:flex;align-items: center;gap:5px;">
                    <i class="pi pi-bars"></i> Other calendar(s)
                </button>
                <Popover ref="op">
                    <div class="flex flex-col gap-2" id="calendarListRemaining">
                        <div v-for="deleteCalendar of deleteCalendarsRemaining" :key="deleteCalendar.key" class="flex items-center gap-2">
                            <Checkbox class="deleteCalendarCheckbox" v-model="selectedDeleteCalendars" :inputId="deleteCalendar.key" name="deleteCalendar" :value="deleteCalendar.name" />
                            <label :for="deleteCalendar.key">{{ deleteCalendar.name }}</label>
                        </div>
                    </div>
                </Popover>
            </div>
        </div>

        
    </form>
</template>

<style scoped>

h2 {
    margin-top: 10px;
    color: #fadbe1;
}

.container {
  display: flex;
  box-sizing: border-box;
  gap: 300px;
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
    transition: width 0.05s ease; /* Smooth transition */
}

p {
    color: #fadbe1;
}

</style>