const form = document.getElementById("addInstructorForm");
const messageDiv = document.getElementById("message");

form.addEventListener("submit", async (e) => {
    e.preventDefault(); // prevent page reload
	
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    //const lesson = document.getElementById("lesson").value;

    try {
	const newInstructor = await apiPost('/instructors', { name, email, password });
	messageDiv.textContent = `Instructor ${newInstructor.name} added!`;

	loadInstructors(); // reload the list
	    //
	form.reset();
    } catch (error) {
	console.error(error);
	messageDiv.textContent = "Failed to add instructor";
    }
});


async function loadInstructors() {
    try {
	// fetch instructors list from API
	const instructors = await apiGet("/instructors");
	
	const container = document.getElementById("instructors");
	
	let html = "";

	// loop thru each instructor
	for (let i of instructors) {
	    html += `
	        <div class="instructor-card">
		    <!-- instructor name -->
		    <h3>${i.name}</h3>

		    <!-- Unique Id -->
		    <p>ID: ${i.id}</p>

		    <!-- email -->
		    <p>Email: ${i.email}</p>

		    <!-- lessons -->
		    <p>Lessons: ${i.lessons || "N/A"}</p>

		    <!-- update instructor -->
		    <button onclick="updateInstructor('${i.id}')">Update</button>

		    <!-- delete instructor -->
		    <button onclick="deleteInstructor('${i.id}')">Delete</button>

		</div>
	    `;
	}

	container.innerHTML = html;
    } catch (error) {
	console.error("Error loading instructors:", error);

	// flash error to users
	document.getElementById("instructors").innerHTML = `
	    <p>Failed to load instructors.</p>`;

    }
}

async function updateInstructor(id) {
    const newEmail = prompt("Enter new Email: ");
    const newLesson = prompt("Enter new Lesson: ");

    // exit if both are empty
    if (!newLesson && !newEmail) {
	return;
    }

    // only update using filled fields
    const updatedData = {};
    if (newLesson) updatedData.lesson = newLesson;
    if (newEmail) updatedData.email = newEmail;
    
    try {
	await apiPut(`/instructors/${id}`, updatedData);
	alert("Instructor updated!");
	loadInstructors();  // refreshes list
    } catch (error) {
	console.error(error);
	alert("failed to update instructor");
    }
}

async function deleteInstructor(id) {
    if (!confirm("Are you sure you want to delete this instructor?")) {
	return;
    }

    try {
	await apiDelete(`/instructors/${id}`);
	alert("Instructor deleted!");
	loadInstructors();
    } catch (error) {
	alert("Failed to delete instructor.");
    }
}

window.onload = loadInstructors;
