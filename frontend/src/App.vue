<script setup>
import { RouterLink, RouterView } from 'vue-router'
import 'primeflex/primeflex.css'

import logo from "./assets/images/DAhandlerTransparent.png"

</script>

<template>
  <!-- <div class="grid" style="width:100vw;height:100vh; background-color: grey">
      <div class="col-fixed" style="width:100px;">
          <div class="text-center p-3 border-round-sm font-bold" style="background-color: aqua;">100px</div>
      </div>
      <div class="col">
          <RouterView />
      </div>
  </div> -->

<div class="app-container">
  <div class="card flex justify-content-center">
    <Drawer visible :modal="false" :fullScreen="false" :position="'left'" :mask="false" :closable="false">
        <div class="flex flex-column h-full">
          <div class="flex align-items-center justify-content-between px-4 pt-3 flex-shrink-0">
            <span class="inline-flex align-items-center gap-2">
              <div class="w-auto h-auto">
                <img :src="logo" alt="logo" class="w-full h-full object-contain" />
              </div>
              <!-- <span class="font-semibold text-2xl pl-0">DAhandler</span> -->
            </span>
          </div>
          <div class="overflow-y-auto ">
            <ul class="list-none p-3 m-0 pt-0">
              <li>
                <ul class="list-none p-0 m-0 overflow-hidden">
                  <li>
                    <a v-ripple class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
                      <i class="pi pi-home mr-2 custom-icon"></i>
                      <!-- insert adding logo here-->
                      <span class="font-medium text-light-pink">Adding</span>
                    </a>
                  </li>
                  <div class="divider"></div>
                  <li>
                    <a
                      v-ripple
                      class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                    >
                      <i class="pi pi-bookmark mr-2 custom-icon"></i>
                      <!-- insert deleting logo here-->
                      <span class="font-medium text-light-pink">Deleting</span>
                    </a>
                  </li>
                  <div class="divider"></div>
                  <li>
                    <a v-ripple class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
                      <i class="pi pi-calendar mr-2 custom-icon"></i>
                      <span class="font-medium text-light-pink">Calendar</span>
                    </a>
                  </li>
                  <div class="divider"></div>
                  <li>
                    <a
                      v-ripple
                      class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                    >
                      <i class="pi pi-users mr-2 custom-icon"></i>
                      <span class="font-medium text-light-pink">Team</span>
                    </a>
                  </li>
                  <div class="divider"></div>
                </ul>
              </li>
            </ul>
          </div>
        </div>
    </Drawer>
    </div>


  <main class="main-content">
    <div class="grid">
        <RouterView />
    </div>
  </main>

</div>


</template>

<style>
.app-container {
  display: flex;
  height: 100vh; /* Full height */
  width: 100%;
}

.p-drawer {
  position: fixed; 
  top: 0;
  left: 0;
  width: 300px !important; 
  height: 100vh; 
  z-index: 9999; 
}

.p-drawer .p-drawer-content {
  position: static;
  padding: 0;
}

.p-drawer li {
  margin-top: 0;
  margin-bottom: 0;
  padding-top: 0px;
  padding-bottom: 0px;
}


.main-content {
  flex-grow: 1;
  padding: 1rem;
  margin-left: 350px;
  overflow: auto;
}

.p-drawer-header {
  display: none !important; /* Hides the X button */
}

.divider {
  border-bottom: 1px solid #faa1af;
  margin: 10px 0;
}

.custom-icon {
  color: #fb607f;
}

</style>
