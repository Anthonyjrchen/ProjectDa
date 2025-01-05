<script setup>
import { ref, watch } from 'vue';
import Textarea from 'primevue/textarea';
import $ from 'jquery';
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

const confirm = useConfirm();
const toast = useToast();

const confirm1 = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to proceed?',
        icon: 'pi pi-exclamation-triangle',
        rejectProps: {
            label: 'Cancel',
            severity: 'secondary',
            outlined: true
        },
        acceptProps: {
            label: 'Clear'
        },
        accept: () => {
            toast.add({ severity: 'info', summary: 'Cleared', detail: 'Logs cleared.', life: 3000 });
        },
        reject: () => {
            toast.add({ severity: 'error', summary: 'Cancelled', detail: 'Did not clear logs.', life: 3000 });
        }
    });
};
</script>

<template>
    <div class="grid">
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1 class="m-0">
                    Adding Log 
                </h1>
            </div>
            <Textarea v-model="holidaysText" rows="20" cols="20"></Textarea>
        </div>
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1 class="m-0">
                    Deleting Log
                </h1>
            </div>
            <Textarea v-model="ignoredCalendersText" rows="20" cols="20"></Textarea>
        </div>
    </div>
    <div class="buttonWrap">
        <Toast />
        <ConfirmDialog class="pt-5"></ConfirmDialog>
        <button class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea" @click="confirm1($event)" label="Clear">Clear</button>
    </div>
</template>

<style scoped>
.grid {
    display: flex;
    gap: 20px;
    width: 79.5vw;
    height: 90vh;
   }

.col {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
}

h1 {
    font-size: x-large;
    margin-bottom: 10px; /* Adds some space below the header */
}

textarea {
    resize: none;
    width: 100%;
    height: 100%;
}

.buttonWrap {
    display: flex;
    gap: 10px;
    position: absolute;
    right: 50px; /* Adjust to position horizontally */
    bottom: 20px; /* Adjust for vertical positioning */
}


</style>