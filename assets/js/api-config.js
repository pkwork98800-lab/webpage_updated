// Central place to configure where the Flask backend lives.
//
// Your setup: frontend on GitHub Pages, backend on PythonAnywhere.
// These are two DIFFERENT domains, so window.location.origin (the GitHub
// Pages URL) is NOT the backend - it must be hardcoded below. Without this,
// the contact form silently tries to POST to the GitHub Pages domain itself,
// which has no server and returns 405 Method Not Allowed.
const PRODUCTION_API_BASE_URL = 'https://kevinpk.pythonanywhere.com';

const API_BASE_URL = (function () {
    const isLocal = ['localhost', '127.0.0.1', ''].includes(window.location.hostname);
    if (isLocal) {
        return 'http://localhost:5000';
    }
    return PRODUCTION_API_BASE_URL;
})();

