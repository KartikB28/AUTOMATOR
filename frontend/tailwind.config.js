export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#0a0a0a',
          800: '#111111',
          700: '#1a1a1a',
          600: '#222222',
          500: '#2a2a2a',
          400: '#333333',
          300: '#444444',
        },
        accent: {
          DEFAULT: '#00ff88',
          dim: '#00cc6a',
          muted: 'rgba(0, 255, 136, 0.12)',
        },
        warn: '#ffaa00',
        danger: '#ff4444',
        info: '#4488ff',
        muted: '#666666',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    }
  },
  plugins: []
};
