/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/jsx', // Prefix for your API calls
        destination: 'http://localhost:8000/jsx', // Your FastAPI backend
      },
      {
        source: '/html', // Prefix for your API calls
        destination: 'http://localhost:8000/html', // Your FastAPI backend
      },
    ];
  },
};

module.exports = nextConfig;
