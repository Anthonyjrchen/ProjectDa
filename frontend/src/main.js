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

import ConfirmationService from 'primevue/confirmationservice'
import DialogService from 'primevue/dialogservice'
import ToastService from 'primevue/toastservice';

import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import Button from 'primevue/button';


const app = createApp(App)


app.use(ConfirmationService);
app.use(ToastService);
app.use(DialogService);
app.config.errorHandler = () => null;
app.config.warnHandler = () => null;
app.component('Drawer', Drawer) 
app.component('ProgressBar', ProgressBar) 
app.component('Toast', Toast);
app.component('ConfirmDialog', ConfirmDialog);
app.component('Button', Button);
app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
    },
    ripple: true
});
app.mount('#app')
