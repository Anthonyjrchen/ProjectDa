import './assets/main.css'

import './index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import Drawer from 'primevue/drawer'
import ProgressBar from 'primevue/progressbar'
import 'primeicons/primeicons.css'  // Import PrimeIcons styles


const app = createApp(App)
app.config.errorHandler = () => null;
app.config.warnHandler = () => null;
app.component('Drawer', Drawer) 
app.component('ProgressBar', ProgressBar) 
app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
    },
    ripple: true
});
app.mount('#app')
