async function loadLessons() {
    try {
	// fetch lessons list from API
	const lessons = await apiGet("/lessons");
	
	const container = document.getElementById("lessons");
	
	let html = "";

	// loop thru each lesson
	for (let i of lessons) {
	    html += `
	        <div class="lesson-card">
		    <!-- Lesson name -->
		    <h3>${i.name}</h3>

		    <!-- Unique Id -->
		    <p>ID: ${i.id}</p>

		    <!-- duration -->
		    <p>Duration: ${i.duration}</p>

		</div>
	    `;
	}

	container.innerHTML = html;
    } catch (error) {
	console.error("Error loading lessons:", error);

	// flash error to users
	document.getElementById("lessons").innerHTML = `
	    <p>Failed to load lessons.</p>`;

    }
}

window.onload = loadLessons;
