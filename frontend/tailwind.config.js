/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    extend: {
      colors: {
        'dark-white': '#52525b', // Very light gray, off-white
        'dark-gray': '#121212',
      },
    },
  },
  plugins: [],
}

