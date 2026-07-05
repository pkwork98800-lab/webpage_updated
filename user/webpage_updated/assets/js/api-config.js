// Central place to configure where the Flask backend lives.
//
// - When you open the site locally (double-click index.html, or run it on
//   127.0.0.1 / localhost with a simple static server) it will call your
//   local Flask server at http://localhost:5000.
// - When you deploy the frontend and backend together on the SAME domain
//   (e.g. Render, Railway, PythonAnywhere serving both the static files
//   and the Flask app) it automatically uses the current origin, so you
//   don't have to edit this file for production.
//
// If you deploy the frontend and backend on DIFFERENT domains (e.g.
// frontend on GitHub Pages/Netlify and backend on Render), replace the
// line below with your backend's public URL, for example:
//   const API_BASE_URL = 'https://your-backend-app.onrender.com';
const API_BASE_URL = (function () {
    const isLocal = ['localhost', '127.0.0.1', ''].includes(window.location.hostname);
    if (isLocal) {
        return 'http://localhost:5000';
    }
    return window.location.origin;
})();
