/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    extend: {
      colors: {
        'dark-white': '#52525b', // Very light gray, off-white
        'dark-gray': '#121212', //very dark gray

        //pink palette
        'brink-pink': '#fb607f',
        'sweet-pink': '#faa1af',
        'rose-bud': '#fab0ba',
        'cupid': '#fcbec8',
        'chantilly': '#faccd6',
        'azalea': '#fadbe1',
        'light-pink': '#f9e6ea',
      },
    },
  },
  plugins: [],
}

