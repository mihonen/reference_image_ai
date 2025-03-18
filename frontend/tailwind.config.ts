import type { Config } from 'tailwindcss'
import defaultTheme from 'tailwindcss/defaultTheme'

export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        brand: {
          '50': '#fcf3f7',
          '100': '#fae9f1',
          '200': '#f8d2e4',
          '300': '#f3aecb',
          '400': '#ea7caa',
          '500': '#e0548a',
          '600': '#ce3669',
          '700': '#b22450',
          '800': '#932143',
          '900': '#7b203b',
          '950': '#4b0c1e',
        },
        brand2: {
            '50': '#fef4f2',
            '100': '#fde7e3',
            '200': '#fcd3cc',
            '300': '#f9b3a8',
            '400': '#f38776',
            '500': '#ea6954',
            '600': '#d5452d',
            '700': '#b33622',
            '800': '#943020',
            '900': '#7b2e21',
            '950': '#43140c',
        },
      },
      fontFamily: {
        'standard': ['Quicksand', 'sans-serif'] 
      }

    }
  }
}