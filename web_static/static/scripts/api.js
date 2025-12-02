// Reusable JS API Client

const API_BASE = "http://127.0.0.1:5000/api/v1";

async function apiGet(endpoint) {
    // request api for endpoint
    const response = await fetch(`${API_BASE}${endpoint}`);
	if (!response.ok) {
	    throw new Error(`API GET error: ${response.status}`);
	}
	return await response.json();
}

async function apiPost(endpoint, data) {
    // post request to the api
    const response = await fetch(`${API_BASE}${endpoint}`, {
	method: "POST",
	headers: {"Content-Type": "application/json"},
	body: JSON.stringify(data)
    });

    if (!response.ok) {
	throw new Error(`API POST error: ${response.status}`);
    }
    return await response.json();
}

async function apiPut(endpoint, data) {
    // update request to the api
    const response = await fetch(`${API_BASE}${endpoint}`, {
	method: "PUT",
	headers: {"Content-Type": "application/json"},
	body: JSON.stringify(data)
    });

    if (!response.ok) {
	throw new Error(`API PUT error: ${response.status}`);
    }
    return await response.json();
}

async function apiDelete(endpoint) {
    // delete request
    const response = await fetch(`${API_BASE}${endpoint}`, {
	method: "DELETE"
    });

    if (!response.ok) {
	throw new Error(`API DELETE error: ${response.status}`);
    }
    return await response.json();
}
