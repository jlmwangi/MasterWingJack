async function loadStudents() {
    try {
	// fetch students list from API
	const students = await apiGet("/students");
	
	const container = document.getElementById("students");
	
	let html = "";

	// loop thru each student
	for (let i of students) {
	    html += `
	        <div class="student-card">
		    <!-- student name -->
		    <h3>${i.name}</h3>

		    <!-- Unique Id -->
		    <p>ID: ${i.id}</p>

		    <!-- Age -->
		    <p>Age: ${i.age}</p>

		    <!-- email -->
		    <p>Email: ${i.email}</p>

		    <!-- lessons -->
		    <p>Lessons: ${i.lessons || "N/A"}</p>
		</div>
	    `;
	}

	container.innerHTML = html;
    } catch (error) {
	console.error("Error loading students:", error);

	// flash error to users
	document.getElementById("students").innerHTML = `
	    <p>Failed to load students.</p>`;

    }
}

window.onload = loadStudents;
