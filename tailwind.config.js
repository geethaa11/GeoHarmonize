/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#101B2D",
          800: "#14213D",
          700: "#1B2A45",
          600: "#26385A"
        },
        paper: {
          DEFAULT: "#F4F5F1",
          dim: "#E9EBE4"
        },
        seal: {
          DEFAULT: "#B08D3E",
          light: "#D9B876",
          dark: "#8A6C2D"
        },
        contour: {
          DEFAULT: "#3E7C7C",
          light: "#6FA8A8"
        },
        alert: "#B5533C"
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["IBM Plex Sans", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"]
      },
      backgroundImage: {
        contours: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Cg fill='none' stroke='%23101B2D' stroke-opacity='0.04' stroke-width='1'%3E%3Ccircle cx='100' cy='100' r='30'/%3E%3Ccircle cx='100' cy='100' r='55'/%3E%3Ccircle cx='100' cy='100' r='80'/%3E%3Ccircle cx='100' cy='100' r='105'/%3E%3C/g%3E%3C/svg%3E\")"
      }
    },
  },
  plugins: [],
}
