/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        void: 'var(--void)',
        field: 'var(--field)',
        lift: 'var(--lift)',
        recess: 'var(--recess)',
        cream: 'var(--cream)',
        acid: 'var(--acid)',
        risk: {
          critical: 'var(--r-critical)',
          high: 'var(--r-high)',
          medium: 'var(--r-medium)',
          low: 'var(--r-low)',
          unknown: 'var(--r-unknown)',
        },
      },
      fontFamily: {
        display: ['Bebas Neue', 'sans-serif'],
        serif: ['Cormorant Garamond', 'serif'],
        ui: ['Syne', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '4px',
        sm: '2px',
        none: '0px',
      },
      letterSpacing: {
        tactical: '0.12em',
        wide: '0.08em',
        loose: '0.14em',
      },
      fontSize: {
        10: '10px',
        11: '11px',
        96: '96px',
      },
    },
  },
  plugins: [],
};
