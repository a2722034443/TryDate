/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        pink: {
          heart: '#FF6B8A',
          soft: '#FFB3C6',
          pale: '#FFE4EC',
        },
        lilac: {
          DEFAULT: '#C9B8FF',
          deep: '#A394E8',
          pale: '#EDE8FF',
        },
        cream: '#FFF8F5',
        'text-main': '#2D2020',
        'text-sub': '#8C7B7B',
        mint: '#6DCFB6',
        amber: '#FFB347',
      },
      fontFamily: {
        sans: ['Nunito', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      boxShadow: {
        card: '0 8px 32px rgba(255, 107, 138, 0.12)',
        'card-hover': '0 16px 48px rgba(255, 107, 138, 0.2)',
        glow: '0 0 20px rgba(255, 107, 138, 0.4)',
      },
      backgroundImage: {
        'gradient-heart': 'linear-gradient(135deg, #FF6B8A 0%, #C9B8FF 100%)',
        'gradient-soft': 'linear-gradient(135deg, #FFE4EC 0%, #EDE8FF 100%)',
        'gradient-page': 'linear-gradient(180deg, #FFF8F5 0%, #FFE4EC 40%, #EDE8FF 100%)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'float-delayed': 'float 6s ease-in-out 2s infinite',
        'float-slow': 'float 8s ease-in-out 1s infinite',
        'pulse-heart': 'pulseHeart 1.5s ease-in-out infinite',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'fade-in': 'fadeIn 0.3s ease-out',
        'bounce-in': 'bounceIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-20px) rotate(5deg)' },
        },
        pulseHeart: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.15)' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(30px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        bounceIn: {
          from: { opacity: '0', transform: 'scale(0.6)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% center' },
          '100%': { backgroundPosition: '200% center' },
        },
      },
    },
  },
  plugins: [],
}
